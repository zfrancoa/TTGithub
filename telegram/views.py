from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Chat_Message, Delete_Chat, Active_Chat



# Create your views here.

@login_required
def active_list(request):

    users_list=[]
    count_unread=[]
    delete_user=0#variable que usaremos como una bandera.

    #Nos fijamos todos los usuarios con quienes tenemos conversaciones:
    all_conversations_I_Tx = Active_Chat.objects.filter(Tx=request.user)
    all_conversations_I_Rx = Active_Chat.objects.filter(Rx=request.user)
    all_conversation=all_conversations_I_Tx.union(all_conversations_I_Rx).order_by('-latest_activate')
    #print(all_conversation)

    #guardamos en una lista los nombres de los usuarios:    
    for item in all_conversation:#recorreremos las conversaciones activas
        if  request.user != item.Rx:#si el usuario logeado no es el Rx.
            if item.Rx not in users_list:#si el Rx no esta en la lista
                users_list.append(item.Rx)
        elif request.user != item.Tx:#si el usuario logeado no es el Tx.
            if item.Tx not in users_list:#si el Tx no esta en la lista
                users_list.append(item.Tx)
            
    #print(users_list)
    


    #Nos fijamos con cuales tenemos mensajes:
    #Con los que no hay mensajes los eliminamos de la vista
    for u in users_list:
        #print("vuelta")
        #OBTENEMOS DESDE QUE FECHA EL USUARIO NO QUIERE VER MENSAJES:
        intance_not_view = Delete_Chat.objects.filter(deleter=request.user, other=u).first()
        if intance_not_view:#si existe esta instancia significa que el usuario ha "eliminado mensajes"
            #excluimos los mensajes que no queremos ver:
            chat_option_1=Chat_Message.objects.filter(transmitter=request.user, receiver=u).exclude(created_at__lt=intance_not_view.delete_at)
            #excluimos los mensajes que no queremos ver:
            chat_option_2=Chat_Message.objects.filter(transmitter=u, receiver=request.user).exclude(created_at__lt=intance_not_view.delete_at) 
            #print("existe instancia")
            if not chat_option_1:
                #print("chat_option_1")
                if not chat_option_2:
                    #print("chat_option_2")
                    #si no existe ninguna de las dos opciones, entonces no hay mensajes que mostrar, por ende este usuario no debe estar en la lista.
                    users_list.remove(u)
                    #tambien podriamos borrar la intancia del modelo Active_chat, indicando que no hay coversación
                    Active_Chat_instance = Active_Chat.objects.filter(Tx=request.user, Rx=u)
                    Active_Chat_instance.delete()
                    delete_user=1

            if delete_user == 0:
                #print("entro aca")
                #Nos fijamos con cuales tenemos mensajes sin leer:
                #contamos la cantidad de mensajes sin leer con cada usuario
                message_unread=Chat_Message.objects.filter(transmitter_id=u.id, receiver_id=request.user).exclude(unread=1)#Excluimos los mensaje leidos
                many=message_unread.count()
                count_unread.append(many)



        else:#si no se han "eliminado" mensajes el usuario querra ver todos
            #print("no existe instancia")
            #obtenemos los mensajes.:
            chat_option_1=Chat_Message.objects.filter(transmitter=request.user, receiver=u)
            #obtenemos el resto de los mensajes.
            chat_option_2=Chat_Message.objects.filter(transmitter=u, receiver=request.user)

            if not chat_option_1:
                if not chat_option_2:
                    #si no existe ninguna de las dos opciones, entonces no hay mensajes que mostrar, por ende este usuario no debe estar en la lista.
                    users_list.remove(u)
                    #tambien podriamos borrar la intancia del modelo Active_chat, indicando que no hay coversación
                    instance = Active_Chat.objects.filter(Tx=request.user, Rx=u)
                    instance.delete()
                    delete_user=1


            if delete_user == 0:
                #print("entro aca")
                #Nos fijamos con cuales tenemos mensajes sin leer:
                #contamos la cantidad de mensajes sin leer con cada usuario
                message_unread=Chat_Message.objects.filter(transmitter=u, receiver=request.user).exclude(unread=1)#Excluimos los mensaje leidos
                many=message_unread.count()
                count_unread.append(many)



    return render(request, 'telegram/list.html', {'users_list':users_list, 'count_unread':count_unread})





@login_required
def chat(request, username):

    #Obtenemso el objeto User que pertenezca a "username":
    user_object=User.objects.get(username=username)
    #TENEMOS QUE ENCONTRAR LOS MENSAJES CORRESPONDIENTES A LA SALA.
    #VAMOS A TENER DOS OPCIONES, UNA DONDE EL request.user es el transmitter y el username(parametro que pasamos por url) es el receiver.
    #LA OTRA OPCION ES LA VICEVERSA A LA ANTERIOR.
    #DE IGUAL MODO NO QUEREMOS TODOS LOS MENSAJES, SOLO LOS QUE EL USUARIO NO HAYA "ELIMINADO"

    #OBTENEMOS DESDE QUE FECHA EL USUARIO NO QUIERE VER MENSAJES:
    intance_not_view = Delete_Chat.objects.filter(deleter=request.user, other=user_object).first()

    if intance_not_view:#si existe esta instancia significa que el usuario ha "eliminado mensajes"
        chat_option_1=Chat_Message.objects.filter(transmitter=request.user, receiver=user_object).exclude(created_at__lt=intance_not_view.delete_at)#excluimos los mensajes que no queremos ver.
        #antes de juntarlos en una sola lista y ordenarlos, los marcamos como leidos, pero no todos , solo la opción 2, que son los mensajes que ha enviado el otro usuario.
        #primero nos fijamos si hay mensajes sin leer:
        message_unread=Chat_Message.objects.filter(transmitter=user_object, receiver=request.user).exclude(unread=1)#Excluimos los mensaje leidos
        #el siguiente if no hace falta si los websocket no fallan, por ejemplo, si la conexion es lenta y entramos a un chat donde recibimos un mensaje, pero en el websocket no se lelga a actualizar el campo unread de este mensaje y en este momento eliminamos la conversación, quedara un mensaje dando vueltas sin leer y nunca nos aparecera el chat de a quien pertenece.
        # if message_unread:#si hay mensajes sin leer los leemos
        #     message_unread.update(unread=1)
        #     for item in message_unread:
        #         item.save()
        ##
        chat_option_2=Chat_Message.objects.filter(transmitter=user_object, receiver=request.user).exclude(created_at__lt=intance_not_view.delete_at)#excluimos los mensajes que no queremos ver. 
        
        chats=chat_option_1.union(chat_option_2).order_by('created_at')#guardamos y ordenamos todos los mensaje sque si queremos.     
        ##
        ##
    else:#si no se han "eliminado" mensajes el usuario querra ver todos
        chat_option_1=Chat_Message.objects.filter(transmitter=request.user, receiver=user_object)#obtenemos los mensajes.
        #antes de juntarlos en una sola lista y ordenarlos, los marcamos como leidos, pero no todos , solo la opción 2, que son los mensajes que ha enviado el otro usuario.
        message_unread=Chat_Message.objects.filter(transmitter=user_object, receiver=request.user).exclude(unread=1)#Excluimos los mensaje leidos
        #el siguiente if no hace falta si los websocket no fallan, por ejemplo, si la conexion es lenta y entramos a un chat donde recibimos un mensaje, pero en el websocket no se lelga a actualizar el campo unread de este mensaje y en este momento eliminamos la conversación, quedara un mensaje dando vueltas sin leer y nunca nos aparecera el chat de a quien pertenece.
        # if message_unread:#si hay mensajes sin leer los leemos
        #     message_unread.update(unread=1)
        #     for item in message_unread:
        #         item.save()
        ##
        chat_option_2=Chat_Message.objects.filter(transmitter=user_object, receiver=request.user)#obtenemos el resto de los mensajes.

        chats=chat_option_1.union(chat_option_2).order_by('created_at')

    #PASAMOS LOS MENSAJES QUE NO HEMOS VISTO AUN.
    message_list=[]#lista de los id de mensajes no leidos
    #json_list = [1,2,3,'String1']
    for item in message_unread:
        message_list.append(item.id)#sGUARDAMOS EL ID EN LA LISTA    


    #TAMBIEN VAMOS A PASAR LA CANTIDAD DE MENSAJES QUE TENEMOS SIN LEER.
    messages_unreaded=Chat_Message.objects.filter(receiver=request.user).exclude(unread=1)#Excluimos los mensaje leidos
         

    return render(request, 'telegram/chat.html', {'user_object':user_object, 'chats':chats, 'message_list':message_list, 'messages_unreaded':messages_unreaded.count()})
   



@login_required
def delete_all_conversation(request, username):#nombre de usuario de con quien estemos hablando.
   
    I_am=request.user#yo
    other_user=User.objects.get(username=username)#la otra persona de la conversación.

    #Vamos a almacenar desde cuando queremos eliminar mensajes, para esto creamos una instancia de modelo Delete_Chat:
    delete_conversation = Delete_Chat.objects.filter(deleter=I_am, other=other_user).first()
    
    #si delete_conversation existe, entonces lo actualizamos con la fecha actual.
    if delete_conversation:
        delete_conversation.delete()#borramos el objeto antiguo.

    #Creamos un nuevo objeto con la nueva fecha, tanto para el caso de que delete_conversation existe(ya que fue eliminado en el if anterior) y cuando no exista:
    new_instance = Delete_Chat(deleter=I_am, other=other_user)
    new_instance.save()

    #Nos fijamos si el otro usuario ha eliminado mensajes y desde que fecha:
    delete_other_conversation = Delete_Chat.objects.filter(deleter=other_user, other=I_am).first()

    if delete_other_conversation:#SI EL OTRO USUARIO HA ELIMINADO MENSAJES ENTRAMOS ACA.
        #si entra aca significara que el otro usuario ya ha eliminado mensajes, por ende como la fecha del otro usuario va a ser antes eliminamos de la bbdd los mensajes anteriores a esa fecha
        #__lt:"ANTES QUE ..." -->ESTAMOS BUSCANDO LOS MENSAJES CUYAS FECHAS SEAN MENORES A LA QUE PASAMOS.
        #HAY QUE AGREGAR .delete() AL FINAL, PARA QUE LOS MENSAJES SE BORREN.
        Chat_Message.objects.filter(transmitter= I_am, receiver=other_user, created_at__lt=delete_other_conversation.delete_at).delete()
        Chat_Message.objects.filter(transmitter=other_user , receiver=I_am, created_at__lt=delete_other_conversation.delete_at).delete()

        #SE PODRIA ELIMINAR LA INTANCIA DESDE CUANDO QUEREMOS ELIMINAR MENSAJES, YA QUE LOS MENSAJES SE ELIMINARON Y CUANDO SE CARGUEN LOS MENSAJES SE MOSTRARAN LOS QUE NO SE ELIMINARON.
        delete_other_conversation.delete()
    else:#este else se puede eliminar
        pass

    return redirect('chat', username = username)







