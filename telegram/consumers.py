#LOS CONSUMIDORES SON PARECIDAS A LAS VISTAS DE DJANGO.
#cuando Channels acepta una conexión WebSocket(SIMILAR A Cuando Django acepta una solicitud HTTP,), consulta la configuración de enrutamiento raíz para buscar un consumidor(similar a consulta la URLconf raíz para buscar una función de vista) y luego llama a varias funciones en el consumidor para manejar los eventos de la conexión.


# mensajes/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from telegram.models import Chat_Message, Active_Chat
from django.contrib.auth.models import User
from asgiref.sync import sync_to_async
from datetime import datetime


usernames_list=[]
times_list=[]


#Cada protocolo diferente tiene diferentes tipos de eventos que suceden, y cada tipo está representado por un método diferente, en este caso los eventos son: disconnect, receive, connect.
#AsyncWebsocketConsumer: tiene exactamente los mismos métodos y firma que, WebsocketConsumerpero todo es asíncrono, y las funciones que necesita escribir también deben ser.
#WebsocketConsumer: esto envuelve el envío y la recepción de mensajes ASGI simples y detallados en un manejo que solo trata con texto y marcos binarios.
class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        if self.scope['user'].is_anonymous:
            #  Refuse an anonymous user connection
            await self.close()
        else:
            #  Join the chat group, named the user name of the current login user, namely self.scope ['user']. Username
            #nos unimos  a un grupo individual, cada usuario tendra su propio grupo, de nombre, cual username tengan.
            await self.channel_layer.group_add(self.scope['user'].username, self.channel_name)
            #print('se conecto:'+self.scope['user'].username)
            #print('QUE USERNAME ES EL QUE TENEMOS EN EL routing.py QUE PERTENECE A ESTE CONSUMIDOR'+self.scope['url_route']['kwargs']['username'])
            await self.accept()


            #aceptada la conexion enviamos mensaje indicando al otro usuario que estamos conectados:
            #tambien enviamos los id de los mensajes no leidos , y los marcamos como leidos:


            results = await get_message_unread(self.scope['url_route']['kwargs']['username'] , self.scope['user'].id)


            
            #cuando nos conectamos, enviamos un mensaje indicandole al otro usuario que nos conectamos.
            await self.channel_layer.group_send(
                self.scope['url_route']['kwargs']['username'],#grupo al que se envia el mensaje, grupo del usuario con el que queremos hablar.
                {
                    'type': 'status.chat',#función a ejecutarse, esta sera la que envie el mensaje, esta función esta mas abajo.
                    'status_user': 'connected',#PARA INDICAR QUE NOS CONECTAMOS
                    'results': results,#id de los mensajes no leidos, estos id se usaran para cambiar los mensajes no leidos a leidos, obviamente, del lado del usuario con quien estamos hablando.
                    'other_UserName': self.scope['user'].username#nombre de usuario de quien envia el mensaje.
                }
            )


    async def disconnect(self, code):
        
        '''Leave chat group'''
        #ANTES DE DEJAR EL GRUPO MANDAMOS UN MENSAJE INDICANDO DESCONECCIÓN:
        #NECESITAMOS EL USERNAME DEL USUARIO CON QUIEN HABLAMOS:
        # Send message to room group
        UserName=self.scope['url_route']['kwargs']['username']
        results='unnecessary'#mandamos un result, ya que el async def status_chat(self, event): se comparte para tres envio de mensajes, y en los tres casos se deben pasar las mismas variables.
       
        await self.channel_layer.group_send(
            UserName,#grupo al que se envia el mensaje, grupo del usuario con el que queremos hablar.
            {
                'type': 'status.chat',#función a ejecutarse, esta sera la que envie el mensaje, esta función esta mas abajo. Esta funcion es la que se comparte.
                'status_user': 'disconnect',#PARA INDICAR QUE NOS CONECTAMOS
                'results': results,#en otra llamada, el results contiene los ids, pero como se usa la misma funcion para enviar distintos mensajes, se debe pasar el mismo contenido a esta funcion.
                'other_UserName':self.scope['user'].username#nombre de usuario de quien envia el mensaje.
            }
        )
        #print('se envio UN MENSAJE de desconexion DESDE el consumer hacia javascript')

        
        #como nos desconectamos de la interfaz, eliminamos al usuario de la lista:
        if UserName in usernames_list:#primero nos fijamos si el usuario esta en la lista
            ############
            #antes de desconectarnos actualizaremos las instancias del modelo Active_Chat:
            await active_chat( UserName, self.scope['user'].id)




        #AHORA SI, DEJAMOS EL GRUPO.
        # '''Leave chat group'''
        await self.channel_layer.group_discard(
            self.scope['user'].username,
            self.channel_name
        )
        #print('se desconecto:'+self.scope['user'].username)

    # Receive message from WebSocket
    async def receive(self, text_data):# en text_data viene lo que enviamos en javascript a traves del websocket. 
        
        text_data_json = json.loads(text_data)#cargamos los datos recibidos en la variable text_data_json.
        #print(text_data)#se imprime en la consola de windows el mensaje recibido.
        UserName=self.scope['url_route']['kwargs']['username']#nombre del usuario con el que queremos hablar.
        action=text_data_json['action']#uno de los valores particulares que se envia con JS, action contiene la accion que se ejecutara, un envio de mensaje  de chat, indicar que estamos conectado, etc.

        ##---------------------------------------------##
        #GUARDAMOS LOS MENSAJES EN LA BBDD:

        #Obtenemos el usuario al que le enviaremos el mensaje
        receiver_user = await database_sync_to_async(User.objects.get)(username=UserName)

        if action == "message":#Si la accion se debe al envio de un mensaje al chat.

            message = text_data_json['message']#mensaje.
            state_other_user = text_data_json['state_other_user']#estado del usuario con el que hablamos.


            ##ANTES DE DESCONCTARNOS, ACTUALIZAREMOS LA INSTANCIA DEL MODELO active_chat:
            #await active_chat(self.scope['url_route']['kwargs']['username'] , self.scope['user'].id)



            ##############################################################
            #BLOQUE DE CODIGO QUE NOS SIRVE PARA LUEGO CREAR O ACTUALIZAR LA INSTANCIA DEL MODELO Active_Chat. 
            #Nos fijamos si el usuario(no yo) ya esta en la lista, si no esta lo agregamos, y no importa la opción, agregamos el neuvo horario:
            if UserName in usernames_list:#primero nos fijamos si el usuario esta en la lista
                #.index() genera una excepción si el valor no esta en la lista, por eso, conviene primero ver si esta.
                position = usernames_list.index(UserName)#obtenemos la posición de donde esta.
                #agregamos el tiempo en la lista correspondiente, en la posición antes calculada:
                times_list.insert(position, datetime.now())
            else:#si no esta, lo agregamos
                usernames_list.append(UserName)
                position = usernames_list.index(UserName)#obtenemos la posición de donde esta.
                #agregamos el tiempo en la lista correspondiente, en la posición antes calculada:
                times_list.insert(position, datetime.now())
            ############################################################## 









            #creamos una instancia del mensaje enviado.
            if  state_other_user== "Connect":#si el otro usuario esta conectado
                #print("entramos aca 1")
                #Creamos un nuevo objeto del modelo Chat_Message
                chat = Chat_Message(
                    transmitter=self.scope['user'],#quien transmite el mensaje
                    receiver=receiver_user,#quien lo recibe
                    content=message,#contenido
                    unread=1#marcamos como leido el mensaje
                )
            else:#si el otro usuario no esta conectado
                #print("entramos aca 2")
                #Creamos un nuevo objeto del modelo Chat_Message
                chat = Chat_Message(
                    transmitter=self.scope['user'],#quien transmite el mensaje
                    receiver=receiver_user,#quien lo recibe
                    content=message#contenido
                )



            
            await database_sync_to_async(chat.save)()#guardamos los mensajes

            ##---------------------------------------------##

            # Send message to my group
            ##probemos enviando el mensaje a nuestor propio grupo, pero con el id del mensaje:
            await self.channel_layer.group_send(
                self.scope['user'].username,#grupo al que se envia el mensaje, nuestro propio grupo.
                {
                    'type': 'my_idmessage',
                    'id_message': chat.id,#enviamos id del mensaje
                    'message': message,#enviamos contenido del mensaje
                    'other_UserName':UserName#nombre de usuario de con quien estamos hablando
                }

            )

            # Send message to their group
            #print('GRUPO AL QUE SE ENVIA EL MENSAJE:' + UserName).
            await self.channel_layer.group_send(
                UserName,#grupo al que se envia el mensaje, grupo del usuario con el que queremos hablar.
                {
                    'type': 'their_idmessage',
                    'id_message': chat.id,#enviamos id del mensaje.
                    'message': message,#contenido del mensaje.
                    'other_UserName':self.scope['user'].username#nombre de usuario de quien envia el mensaje, o sea para que el otro usuario que es el que recibe este mensaje, se fije si esta en la interfaz de chat con nosotros o con otro, y asi no mostrar información "clasificada".
                }
            )
        elif action == 'delete':#cuando el mensje recibido es debido a la eliminacion de un mensaje.

            id_message_delete=text_data_json['id_message_delete']#obtenemos el id(que se envio por JS) del mensaje que se eliminara.

            #debemos eliminar el mensaje de la BBDD:
            #obtenemos el mensaje a eliminar:
            message_deleted = await database_sync_to_async(Chat_Message.objects.get)(id=id_message_delete)
            #eliminamos el mensaje:
            await database_sync_to_async(message_deleted.delete)()



            #Send message to room group
            #print('GRUPO AL QUE SE ENVIA EL MENSAJE:' + UserName).
            await self.channel_layer.group_send(
                UserName,#grupo al que se envia el mensaje, grupo del usuario con el que queremos hablar.
                {
                    'type': 'delete.message',
                    'id_message_delete': id_message_delete,#id del mensaje eliminado, con el fin que el otro usuario que no elimino el mensaje, tambien se elimine de su interfaz de chat.
                    'user_delete_message':self.scope['user'].username#nombre de usuario de quien envia el mensaje.
                }
            )


        elif action == 'connect':#cuando el mensaje recibido es debido a la conexión de un usuario
            # Send message to room group

            results='unnecessary'#mandamos un result, ya que el async def status_chat(self, event): se comparte para dos envio de mensajes, y en los dos casos se deben pasar las mismas variables.
            #print("se recibio mensaje de conexion dese JS")
            await self.channel_layer.group_send(#este mensaje es enviado para indicar que recibimos mensaje del otro usuario, diciendo que esta conectado, con este mensaje le decimos que recibimos su mensaje y que tambien estamos conectados.
                UserName,#grupo al que se envia el mensaje, grupo del usuario con el que queremos hablar.
                {
                    'type': 'status.chat',
                    'results':results,
                    'status_user': 'connected',#PARA INDICAR QUE NOS CONECTAMOS
                    'other_UserName':self.scope['user'].username#nombre de usuario de quien envia el mensaje.
                }
            )




    # Receive message from room group
    async def status_chat(self, event):
        status_user = event['status_user']
        results = event['results']
        other_UserName = event['other_UserName']#nombre de usuario de quien envia el mensaje
        # Send message to WebSocket
        #print("se envia mensaje de conexion de consumer a js")
        await self.send(text_data=json.dumps({
            'status_user': status_user,#contenido del mensaje.
            'action_consumer':'connect_user',#con esto veremos de que mensaje se trata
            'results':results,
            'other_UserName':other_UserName#nombre de usuario de quien envia el mensaje.
        }))



    # Receive message from room group
    async def delete_message(self, event):
        id_message_delete = event['id_message_delete']
        user_delete_message = event['user_delete_message']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'id_message_delete': id_message_delete,#id del mensaje
            'other_UserName': user_delete_message,#usuario con quien nos comunicacmos
            'action_consumer':'delete_message'#con esto veremos de que mensaje se trata
        }))



    # Receive message from room group
    async def my_idmessage(self, event):#aca enviaremos a JS para el mismo que envio el mensaje a el consumer, o sea el que escribio un mensaje al chat
        id_message = event['id_message']
        message = event['message']
        other_UserName = event['other_UserName']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'id_message': id_message,#id del mensaje
            'message': message,#contenido del mensaje.
            'other_UserName': other_UserName,#usuario con quien nos comunicacmos
            'action_consumer':'my_message'#con esto veremos de que mensaje se trata
        }))
        

    # Receive message from room group
    async def their_idmessage(self, event):#mensaje que enviamos para que lo reciba el JS del "receptor del mensaje."
        message = event['message']
        id_message = event['id_message']
        other_UserName = event['other_UserName']#nombre de usuario de quien envia el mensaje
        #print('se deberia mandar el mensaje')
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,#contenido del mensaje.
            'id_message':id_message,#id del mensaje que se envio por chat
            'other_UserName':other_UserName,#nombre de usuario de quien envia el mensaje.
            'action_consumer':'their_message'#con esto veremos de que mensaje se trata

        }))





@sync_to_async
def get_message_unread(UserName, my_id):#Esta función es llamada cuando un usuario se conecta, lo que hace es obtener los id de los mensajes que no ha visto y tambien los marca como leidos en la BBDD.

    #Obtenemos el usuario al que le enviaremos el mensaje
    receiver_user = User.objects.get(username=UserName)
    
    #obtenemos los mensajes no leidos.
    message_unread = Chat_Message.objects.filter(transmitter=receiver_user.id, receiver=my_id, unread=0)
    

    # #PASAMOS LOS MENSAJES QUE NO HEMOS VISTO AUN.
    message_list=[]#lista de los id de mensajes no leidos
    for item in message_unread:
        message_list.append(item.id)#sGUARDAMOS EL ID EN LA LISTA  

    #LOS MENSAJES SE MARCAN COMO LEIDOS EN LA VISTA 'chat'.-->NO, porque si se marcan como leidos en la vista no se encontraran aca, o sea, todos estaran como vistos, ningun sera no visto.
    #POR LO TANTO, LOS MARCAMOS COMO LEIDOS ACA.
    if message_unread.exists():#si hay mensajes sin leer los leemos
        message_unread.update(unread=1)
        for item in message_unread:
            item.save()


    return list(#lo que devolvemos
        message_list
    )






@sync_to_async
def active_chat(UserName, my_id):#Esta función actualiza el modelo Active_Chat.
    

    ###########################
    #.index() genera una excepción si el valor no esta en la lista, por eso, conviene primero ver si esta.
    position = usernames_list.index(UserName)#obtenemos la posición de donde esta.
    #agregamos el tiempo en la lista correspondiente, en la posición antes calculada:
    time_to_add=times_list[position]


    #Obtenemos el usuario al que le enviaremos el mensaje
    receiver_user = User.objects.get(username=UserName)
    I_am = User.objects.get(id=my_id)#nosotros

    active_instance = Active_Chat.objects.filter(Tx=I_am, Rx=receiver_user).first()
    if active_instance:
        #print("existe una instancia de Active_Chat")
        #le actualizamos la fecha a esta instancia
        active_instance.latest_activate=datetime.now()
        #print("actualizamos una instancia de Active_Chat")
        active_instance.save()#guardamos la instancia actualizada.
        #print("guardamos una instancia de Active_Chat")
    else:#creamos la isntancia
        #print("no existe una instancia de Active_Chat")
        active = Active_Chat(
            Tx=I_am,#quien transmite el mensaje
            Rx=receiver_user,#quien lo recibe
            latest_activate=time_to_add#le agregamos nosotros el valor, porque si no se pone otro horario si usamos el que viene por defecto con el modelo(auto_now_add=True).
        )
        active.save()#guardamos la instancia actualizada.
        #print("creamos y guardamos una instancia de Active_Chat")

    #eliminamos valores de las listas
    #print(usernames_list)
    usernames_list.remove(UserName)
    #print(usernames_list)
    #tambien eliminamos el tiempo:
    #eliminamos el elemento en esa posición de indice
    #print(times_list)
    times_list.pop(position)
    #print(times_list)



    #print("se termino de ejecutar el metodo active_chat -->2")