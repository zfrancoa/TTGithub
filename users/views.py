from django.shortcuts import render
from users.forms import UserForm, ProfileForm, NewUserForm, ChangeEmailForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth import login, authenticate
from django.views.generic import UpdateView, DeleteView, ListView
from django.urls.base import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from users.models import Profile, FollowersRequest
import random
from django.shortcuts import get_object_or_404
import json
from django.http import HttpResponse
from django.urls import reverse

from telegram.models import Chat_Message
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from publish.models import Post
# Create your views here.


#el id del modelo Profile puede ser distinto al del modelo user, por lo tanto, no trabajaremos con estos id.
#trabajaremos con el campo user del modelo Profile, que tiene el mismo id que tiene el usuario en el modelo user, estos id difieren de los que hablamos en la linea anterior, los id de las lineas anterior corresponden a las filas en la BBDD que a veces puede coincidir con los id de los modelos Profile y User.
#ahora que veo la BBDD el id del modelo User es el mismo que representa a las filas, asi que con este id podemos trabajar, con el que no podemos trabajar es con el id que representa a las filas del modelo Profile, eso trae varios problemas.
#QUE NO HACER:
#user=Profile.objects.filter(id=request.user.id)
#QUE HACER:
#user=Profile.objects.filter(user=request.user)
#en este primer ejemplo queremos obtener el objeto Profile del usuario logeado, el problema en el primer caso esta en que usamos el id(representa las filas) dle modelos Profile para filtrar, al cual le pasamos el id del usuario en el modelo User, esto puede generar problemas ya que estos id tal vez no sean iguales, en la segunda linea se ve la forma adecuada de realizar esto.

#TENER CUIDADO1:
#LA LISTA DE FOLLOWERS Y FOLLOWING SE GUARDAN CON LOS id DE LAS FILAS DEL MODELO Profile.
#ESTO SE DEBE A QUE EL CAMPO followers DEL MODELO Profile TIENE UN CAMPO ManyToManyField CON UNA RELACION 'self', QUE SIGNIFICA PROPIO AL MODELO Profie, POR ENDE LOS ID QUE SE GUARDAN SON LOS DEL MODELO Profile.

#TENER CUIDADO2:
#EL MODELO FollowerRequest, sus campos, tienen una relación ForeingKey con el modelo de usuario, por ende, el id que hay que usar aqui es el de EL MODELO User.


from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site



# from django.contrib.auth import get_user_model
# UserModel = get_user_model()



def register(request):#Vista que procesara el formulario para registrar usuarios.
    # If this is a POST request then process the Form data.
    if request.method == "POST":
        # Create a form instance and populate it with data from the request (binding):
        form = NewUserForm(request.POST)
        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required.
            human = True#parte del formulario del captcha

            user = form.save(commit=False)
            #user.is_active = False#esta linea descomentar solo si se quiere que el usuario no necesite activacion.
            user.save()

            #get_current_site(request): obtenemos la url de la web, por eje : TravelTry.com
            # current_site = get_current_site(request)

            # #ENCABEZADO DEL EMAIL:
            # mail_subject = 'Activate account.'

            
            # #para reducir la naturaleza repetitiva de cargar y renderizar plantillas, Django proporciona una función de acceso directo que automatiza el proceso.:
            # #render_to_string( nombre_plantilla , contexto = Ninguno , solicitud = Ninguno , usando = Ninguno ).
            # #render_to_string()carga una plantilla como get_template()y llama a su render()método inmediatamente.
            # #template_name:El nombre de la plantilla para cargar y renderizar. Si es una lista de nombres de plantillas, Django usa en select_template()lugar de get_template()buscar la plantilla.
            # #context:A dictque se utilizará como contexto de la plantilla para la representación.
            # message = render_to_string('users/acc_active_email.html', {
            #     'user': user,
            #     'domain': current_site.domain,
            #     #force_bytes: devuelve un str, una cadena
            #     #urlsafe_base64_encode: Codifica una cadena de bytes en una cadena base64 para su uso en URL, eliminando cualquier signo igual al final.
            #     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            #     'token': default_token_generator.make_token(user),
            # })
            # #obtenemos el campo email que se ingreso al formulario:
            # to_email = form.cleaned_data.get('email')
            # #creamos el mensaje y le decimos a que email corresponde enviarlo:
            # email = EmailMessage(
            #     mail_subject, message, to=[to_email]
            # )
            # #enviamos el email:
            # email.send()
            # return HttpResponse('We have sent an account confirmation email to the address provided.')

            login(request, user)#si se se registra exitosamente, el usuario se logea automaticamente.
            return redirect("home")
    else:# If this is a GET (or any other method) create the default form.
        form = NewUserForm()
    return render (request, "users/register.html", {"register_form":form})


            

# def activate(request, uidb64, token):
    # try:
    #     uid = urlsafe_base64_decode(uidb64).decode()
    #     user = UserModel._default_manager.get(pk=uid)
    # except(TypeError, ValueError, OverflowError, User.DoesNotExist):
    #     user = None
    # if user is not None and default_token_generator.check_token(user, token):
    #     user.is_active = True#activamos al usuario, le permitimos que pueda ingresar con el login
    #     user.save()#guardamos el campo recien cambiado.
    #     # return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    #     login(request, user)#si se se registra exitosamente, el usuario se logea automaticamente.
    #     return redirect("home")
    # else:
    #     return HttpResponse('Activation link is invalid!')








@login_required
def myprofile(request):#vista para perfil del usuario logeado
    

    #Tambien la cantidad de post:
    post_count = Post.objects.filter(user_post=request.user).count()

    #Nos fijamos si tenemos nuevos solicitudes de seguimiento, para luego indicarle al usuario de esto:
    received_follower_request=FollowersRequest.objects.filter(to_user=request.user).count()#buscamos las solicitudes recibidas.
        

    return render(request, 'users/myprofile.html', {'post_count':post_count, 'received_follower_request':received_follower_request})










@login_required
def update_username(request):#vista para cambiar el nombre de usuario.
   
    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        user_form = UserForm(request.POST, instance=request.user)

        # Check if the form is valid:
        if user_form.is_valid():
            # process the data in form.cleaned_data as required
            user_form.save()
            return redirect("update_profile")
     # If this is a GET (or any other method) create the default form.
    else:
        user_form = UserForm(instance=request.user)


    return render(request, 'users/update_username.html', {'user_form': user_form})






@login_required
def update_profile(request):#vista para cambiar bio, photo, privacidad.
   
    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        profile_form = ProfileForm(request.POST, instance=request.user.profile, files=request.FILES)#el argumento files=request.FILES indica que podremos  recibir archivos de nuestro usuario

        # Check if the form is valid:
        if profile_form.is_valid():
            # process the data in form.cleaned_data as required
            profile_form.save()
            return redirect("myprofile")

    # If this is a GET (or any other method) create the default form.
    else:
        profile_form = ProfileForm(instance=request.user.profile)


    return render(request, 'users/update_profile.html', {'profile_form': profile_form})







@method_decorator(login_required, name='dispatch')#en una vista basada en clases no se puede usar el @login_required directamente.
class ChangeEmailUpdateView(UpdateView):#vista basada en clase,por eso no es como las anteriores que son def(metodos)
    form_class=ChangeEmailForm
    success_url=reverse_lazy('home')
    template_name = 'users/change_email.html'#Django maneja el modelo User en esta app, por lo tanto debemos cambiar manualmente con el template_name, sino nos mostrara el siguiente error auth/user_form.html, ya que se busca la template en auth

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):#Lo usaremos para pasar el perfil del usuario del que vemos el perfil, esto para ver si estamos viendo nuestro perfil o otro perfil.
        ##Primero llamamos a la implementación base para obtener un contexto, o sea Primero obtenemos el contexto existente desde nuestra superclase, esto es lo que se hace con la siguiente linea.
        context = super(ChangeEmailUpdateView, self).get_context_data(**kwargs)

        #TAMBIEN VAMOS A PASAR LA CANTIDAD DE MENSAJES QUE TENEMOS SIN LEER.
        messages_unreaded=Chat_Message.objects.filter(receiver=self.request.user).exclude(unread=1)#Excluimos los mensaje leidos

        context['messages_unreaded'] = messages_unreaded.count()

        return context#Devolvemos el nuevo contexto (actualizado)


@login_required
def users_list(request):#vista que buscara personas para que el usuario pueda buscar.
    #Personas a excluir: a quien sigo, y a quien se le envio la solicitud de amistad.   
    #Usamos request.user.profile.id porque el campo followers del modelo Profile tiene una relacion con el modelo Profile no con el modelo User, si se elimina un usuario sin su perfil o su perfil sin su usuario habria problemas.
    #my_followers=request.user.profile.followers.all()#mis seguidores.
    followings = Profile.objects.filter(followers=request.user.profile.id)#a quienes sigo.
    sent_followers_requests = FollowersRequest.objects.filter(from_user=request.user)#Se almacenara los objetos del modelo FollowersRequest, que coincidn con el usuario activo(PERO SOLO EN EL CAMPO from_user), o sea, tendremos todos los objetos en los cuales el usuario logeado haya enviado una solicitud de Amistad.

   
    #TAMBIEN VAMOS A PASAR LA CANTIDAD DE MENSAJES QUE TENEMOS SIN LEER.
    messages_unreaded=Chat_Message.objects.filter(receiver=request.user).exclude(unread=1)#Excluimos los mensaje leidos
         


    users_list=[]#creamos una lista vacia que es donde guardaremos los posibles candidatos.
    follow_sent=[]#lista donde guardaremos los usuarios a los que enviamos la solicitud de follow

    eliminar=[]

    #NOS FIJAREMOS A QUIENES SIGUEN LAS PERSONAS QUE YO SIGO.
    #NO SE PUEDEN BUSCAR QUERYSET DENTRO DE QUERYSET, PERO AL RECORRERLO COMO UN FOR LOS QUERYSET DE UN SOLO OBJETO SI SE PUEDEN BUSCAR DENTRO DE UN QUERYSET.
    for f in followings:#RECORREMOS A QUIENES SEGUIMOS.
        f_followings=Profile.objects.filter(followers=f.id)#OBTENEMOS A QUIENES SIGUE f.
        for u in f_followings:#recorremos los followings(siguiendos) de mis followings(siguiendos)
            if u in followings:#nos fijamos si el usuario ya esta entre los que seguimos.
                #si entra es porque ya lo seguimos asi que lo descartamos
                f_followings=f_followings.exclude(user=u.user)#excluimos a este usuario
            else:#entra aca si el usuario no esta entre los que seguimos
                if u not in users_list:#si el usuario no esta la lista, lo guardamos, sino, no lo guardamos, no queremos que se repita.
                    users_list.append(u)#si no esta en la lista lo guardamos
    if request.user.profile in users_list:#Si el usuario actual(usuario logeado) esta en la lista entra al if.
        users_list.remove(request.user.profile)#se remueve al usuario logeado, o sea, nos removemos a nosotros mismos.
    #EL SIGUIENTE FOR ME QUITA DE LA LISTA LOS USUARIO A QUIENES LE ENVIE LA SOLICITUD DE FOLLOW, PERO ACCEDE A LA BASE DE DATOS EN CADA ITERACCION DEL FOR, TAL VEZ NO NOS CONBIENE HACER ESTO, ENTRAR A LA BBDD ES LENTO.
    #for r in sent_followers_requests:#Recorremos las solicitudes de seguir enviadas
    #     p=Profile.objects.get(user=r.to_user)#obtenemos el perfil del usuario a quien se le envio la solicitud 
    #     if p in users_list:#nos fijamos si el usuario esta en la lista
    #         users_list.remove(p)#lo quitamos
    #MEJOR PLANTEAREMOS LA IDEA DE QUE SI AL USUARIO SE LE ENVIO LA SOLICITUD DE FOLLOW, EN LA LISTA MOSTRARA QUE SE ENVIO LA SOLICITUD, POR ESO ES QUE SE CREO LA VARIABLE sent_followers_requests.
    for se in sent_followers_requests:#recorremos los usuarios a los que el usuario logeado le mando la solicitud.
        #Append(),Este método nos permite agregar nuevos elementos a una lista.
        #Podemos agregar cualquier tipo de elemento a una lista, pero tengan en cuenta lo que pasa cuando agregamos una lista dentro de otra, esta lista se agrega como uno y solo un elemento.
        follow_sent.append(se.to_user)#ESTAMOS AGREGANDO A LA LISTA sent_to el campo to_user de los usuarios a los que se envio la solicitud de amistad.
    #sample () es una función incorporada de módulo random.
    #una lista de longitud particular de elementos elegidos de la secuencia.
    # random.sample(sequence, k).
    #sequence : puede ser una lista, tupla, cadena o conjunto.
    #k : Un valor entero, especifica la longitud de una muestra.
    #Devuelve: k longitud nueva lista de elementos elegidos de la secuencia.
    random_list = random.sample(list(users_list), min(len(list(users_list)), 10))#ACA ESTAMOS TOMANDO 10 SE LOS USUARIOS TOTALES.
    if len(random_list) < 10:#entramos aca si la lista es bastante corta, aca dentro agregaremos usuarios aleatorios.
        users = Profile.objects.exclude(user=request.user)#Por lo tanto aca guardamos todos los objetos del modelo Profile que no sean el usuario activo actualmente.
        aleatory_list = random.sample(list(users), min(len(list(users)), 20))#ACA ESTAMOS TOMANDO 10 SE LOS USUARIOS TOTALES, SIN CONTAR EL LOGEADO.
        for r in followings:#recorremos nuestros followings
            if r in aleatory_list:#Si un following esta en la aleatory_list.
                aleatory_list.remove(r)#removemos el usuario de la aleatory_list, ya que ya lo estamos siguiendo.
        for p in random_list:#recorremos la lista de posiblkes followings
            if p in aleatory_list:#Si un usuario de la random_list esta en la aleatory_list entramos a este if.
                aleatory_list.remove(p)#removemos el usuario de la aleatory_list.
        random_list+=aleatory_list
    return render(request, 'users/users_list.html', {'users_list':random_list, 'follow_sent':follow_sent, 'messages_unreaded':messages_unreaded.count()})


@login_required
def send_or_delete_follower_request(request):#esta vista permite enviar solicitudes y cancelar las enviadas.
    #el id se envia por medio de la url que pertenece a esta vista
    #crear una nueva instancia de solicitud de amistad donde establecemos to_user = el usuario al que se enviará la solicitud,
    #from_user será el usuario que envía la solicitud, es decir request.user o usuario actual    
    #Esta función llama al modelo dado y obtiene el objeto de ese si ese objeto o modelo no existe, genera un error 404.
    received_id = request.GET.get("id")
    to_user = get_object_or_404(User, id=received_id)#LLAMAMOS AL MODELO USER Y OBTENEMOS EL USUARIO AL QUE SE LE ENVIO LA SOLICITUD(todos los datos id,nombre,username, etc) CON EL ID QUE RECIBA send_followers_request, el ID lo mandamos cuando damos click en seguir a traves de una url, esto se hace en la plantilla users_list.
    #get_or_create(defaults=None, **kwargs).
    #get_or_create() Es un método conveniente para buscar un objeto, creando uno si es necesario.
    #**kwargs en una función se usa para pasar, de forma opcional, un número variable de argumentos con nombre.
    # ** kwargs es un diccionario, o sea recibe un numero de argumentos clave/valor y los convierte a un diccionario llamado **kwargs(o el nombre que nosotros elijamos), luego se lo puede trabajar como diccionario. 
    #get_or_create()  Devuelve una tupla de (objeto, creado), donde objeto es el objeto recuperado o creado y creado es un valor booleano que especifica si se creó un nuevo objeto.
    #Si get_or_create encuentra varios objetos, generará una excepción MultipleObjectsReturned.
    #Cualquier argumento de palabra clave que se pase a get_or_create(), excepto uno opcional llamado defaults, se usará en una get()llamada.
    follow_request, created = FollowersRequest.objects.get_or_create(
        from_user=request.user,#
        to_user=to_user)
        #request.user devolviera el usuario actual(CREO QUE EL QUE INICIO SESIÓN).
        #request.user es un objeto de modelo de usuario. No puede acceder al objeto de solicitud en la plantilla si no pasa request explícitamente. Si desea acceder al objeto de usuario desde la plantilla, debe pasarlo a la plantilla o usar RequestContext.
        #ACA ESTAMOS BUSCANDO EN EL MODELO FollowersRequest,si se encuentra una "instancia" con los campos to_user y from_user igual a los datos que le pasamos.

    if not created:#si el objeto no fue creado, significa que se dio en delete request, por lo tanto eliminamos la solicitud enviada
        follow_request.delete()
    resp = {
        'created':created#pasamos la variable para indicar si la solicitud fue creada o ya existe.
    }#ACA CREAMOS UN DICCIONARIO.
    response = json.dumps(resp)#creamos una respuesta codificada en json.
    #HttpResponse ( código fuente ) proporciona una solicitud HTTP entrante a una aplicación web Django con una respuesta de texto. Esta clase se usa con mayor frecuencia como un objeto de retorno desde una vista de Django.
    return HttpResponse(response, content_type = "application/json")#devolvemos una respuesta codificada en JSON


@login_required
def accept_follower_request(request):#esta vista permite aceptar solicitudes recibidas
    received_id = request.GET.get("id")
    user_from = get_object_or_404(User, id=received_id)#Aca se guarda el usuario del cual se acepta la solicitud de seguir(O SEA DEL QUE ENVIA LA SOLICITUD), el id se pasara a traves de una url cuando se de al boton que diga "aceptar seguidor".
    #Abajo, Filtramos solo el primero objeto, porque sera el que tenga el id que le pasamos.
    frequest = FollowersRequest.objects.filter(from_user=user_from, to_user=request.user).first()
    user_to = frequest.to_user#ACA, DEL OBJETO GUARDADO EN "frequest" SOLO ALMACENAMOS EL CAMPO "to_user", que contiene el usuario al que se envio la solicitud.
    user_to.profile.followers.add(user_from.profile)#AGREGAMOS EL USUARIO QUE ENVIO LA SOLICITUD A LA LISTA DE SEGUIDORES DEL USUARIO QUE RECIBIO LA SOLICITUD(OBVIAMENTE SI ANTES LA ACEPTO SI NO NO VIENE A ESTA VISTA PORQUE NO RECIBE EL ID CORRESPONDIENTE).
    
    # #ESTE IF PARA VER EL CASO EN EL QUE EL USUARIO LOGEADO QUE RECIBIO LA SOLITUD DE SEGUIR, TAMBIEN LE HAYA MANDADO UNA SOLITUD AL OTRO USUARIO(DEL CUAL ACPETO LA SOLICITUD), PERO NO HARAI FALTA ACA.
    # if(FriendRequest.objects.filter(from_user=request.user, to_user=from_user).first()):#NOS FIJAMOS SI LA SOLICITUD DE AMISTAD SIGUE ACTIVA, SI SIGUE ACTIVA ENTRAMOS AL IF PARA ELIMINARLA.
    #     request_rev = FriendRequest.objects.filter(from_user=request.user, to_user=from_user).first()#FILTRAMOS SOLO LA SOLICITUD QUE PERTENECE AL PAR DE USUARIOS. 
    #     request_rev.delete()#ELIMINAMOS LA SOLICITUD.
    
    
    frequest.delete()#ELIMINAMOS LA SOLICITUD, YA QUE FUE ACEPTADA.
    accepted=True#dato que se pasa a ajax para indicar que la solicitud fue aceptada

    resp = {
        'accepted':accepted
    }#ACA CREAMOS UN DICCIONARIO.
    response = json.dumps(resp)#creamos una respuesta codificada en json.
    #HttpResponse ( código fuente ) proporciona una solicitud HTTP entrante a una aplicación web Django con una respuesta de texto. Esta clase se usa con mayor frecuencia como un objeto de retorno desde una vista de Django.
    return HttpResponse(response, content_type = "application/json")#devolvemos una respuesta codificada en JSON
    


@login_required
def reject_request_received(request):#esta vista permite rechazar solicitud recibida
    id_rechazada = request.GET.get("id")#obtenemos la id mandada por ajax
    from_user = get_object_or_404(User, id=id_rechazada)#Aca se guarda el usuario del cual se acepta la solicitud de seguir(O SEA DEL QUE ENVIA LA SOLICITUD), el id se pasara a traves de una url cuando se de al boton que diga "aceptar seguidor".
    #Abajo, Filtramos solo el primero objeto, porque sera el que tenga el id que le pasamos.
    frequest = FollowersRequest.objects.filter(from_user=from_user, to_user=request.user).first()
    frequest.delete()#ELIMINAMOS LA SOLICITUD, YA QUE FUE ACEPTADA.
    rechazada=True##dato que se pasa a ajax para indicar que la solicitud fue rechazada
    resp = {
        'rechazada':rechazada
    }#ACA CREAMOS UN DICCIONARIO.
    response = json.dumps(resp)#creamos una respuesta codificada en json.
    #HttpResponse ( código fuente ) proporciona una solicitud HTTP entrante a una aplicación web Django con una respuesta de texto. Esta clase se usa con mayor frecuencia como un objeto de retorno desde una vista de Django.
    return HttpResponse(response, content_type = "application/json")#devolvemos una respuesta codificada en JSON
    




@login_required
def user_profile(request, username):#vista para perfiles de todos los usuarios menos el logeado.
    
    view_user = get_object_or_404(User, username=username)
    view_profile = view_user.profile
    #Las siguiente lineas de codigo es para ver la relacion de este usuario con el logeado.
    #hay que ver quien sigue a quien, y si se envio la solicitud de follow o si el nos envio.
    followings = Profile.objects.filter(followers=request.user.profile.id)#a quienes sigue el usuario logeado.
    if view_profile in followings:#nos fijamos si seguimos a el usuario del que vemos el perfil.
        status='following'
    else:
        status='not_following'
        #nos fijamos si le hemos mandado la solicitud de Follow.
        instance=FollowersRequest.objects.filter(from_user=request.user, to_user=view_profile.user).first()
        if instance:
            status='sent_request'
    #NOS DEBEMOS FIJAR LA PRIVACIDAD DEL PERFIL QUE ESTAMOS VIENDO Y TAMBIEN SI LO SEGUIMOS.
    if view_profile.private == True:#entra si el perfil es privado.
        #AHORA NOS FIJAMOS SI EL USUARIO LOGEADO SIGUE AL PERFIL QUE ESTAMOS VIENDO.
        if status == 'following':#si el user loged sigue a este perfil entra.
            private='public'#hacemos publico el perfil para que el usuario logeado pueda verlo.
        else:
            private='private'#mantenemos en privado el perfil, ya que el usuario logeado no sigue a este perfil.
    else:#como la cuenta no es privada no nos interesa si lo seguimos a no.
        private='public'
    #SEPARATION    

    #Nos fijamos si tenemos nuevos solicitudes de seguimiento, para luego indicarle al usuario de esto:
    received_follower_request=FollowersRequest.objects.filter(to_user=request.user).count()#buscamos las solicitudes recibidas.
        
    #mandamos url para enviar y cancel solicitudes:
    url_send = reverse('send_or_delete_follower_request')
    
    #Tambien la cantidad de post:
    post_count = Post.objects.filter(user_post=view_user).count()


    #url de la que vine:

    referer = request.META.get('HTTP_REFERER')
    
    url_home = reverse('home')
    url_request_follow_sent = reverse('request_follow_sent')
    url_request_follow_received = reverse('request_follow_received')
    url_search_user = reverse('search_user')
    url_users_list = reverse('users_list')
    url_FeaturedPostListView = reverse('FeaturedPostListView', kwargs={'pk': view_user.id})
    url_map = reverse('index', kwargs={'pk': view_user.id})

    if referer:

        if url_home in referer:
            referer = url_home

        elif url_request_follow_sent in referer:
            referer = url_request_follow_sent

        elif url_request_follow_received in referer:
            referer = url_request_follow_received

        elif url_search_user in referer:
            referer = url_search_user

        elif url_users_list in referer:
            referer = url_users_list

        elif url_FeaturedPostListView in referer:
            referer = reverse('home')
            
        elif url_map in referer:
            referer = reverse('home')

        else:#esta opcion seria para cuando se llegue desde Galleryview, home, FeaturedCreateview
            referer = reverse('home')

    else:
        referer = reverse('home')



    return render(request, 'users/profiles.html', {'referer': referer,'post_count': post_count, 'url_send': url_send, 'received_follower_request': received_follower_request, 'view_profile':view_profile, 'status':status, 'private':private})

    


@login_required
def request_follow_sent(request):#esta vista mostrara las solicitudes enviadas del usuario logeado.
    
    my_user = get_object_or_404(Profile, user=request.user)#obtenemos perfil de usuario logeado.
    
    sent_follower_request=FollowersRequest.objects.filter(from_user=my_user.user)#buscamos las solicitudes enviadas.


    #lista donde guardaremos los usuarios a los que enviamos la solicitud de follow:
    follow_sent=[]
    #objetos en los cuales el usuario logeado haya enviado una solicitud de follow.
    sent_followers_requests = FollowersRequest.objects.filter(from_user=request.user)
    for se in sent_followers_requests:#recorremos los usuarios a los que el usuario logeado le mando la solicitud.
        #Append(),Este método nos permite agregar nuevos elementos a una lista.
        #Podemos agregar cualquier tipo de elemento a una lista, pero tengan en cuenta lo que pasa cuando agregamos una lista dentro de otra, esta lista se agrega como uno y solo un elemento.
        follow_sent.append(se.to_user)#ESTAMOS AGREGANDO A LA LISTA sent_to el campo to_user de los usuarios a los que se envio la solicitud de amistad.

    
    return render(request, 'users/request_follow_sent.html', {'follow_sent': follow_sent, 'sent_follower_request':sent_follower_request})





@login_required
def request_follow_received(request):#esta vista mostrara las solicitudes recibidas del usuario logeado.
    
    my_user = get_object_or_404(Profile, user=request.user)#obtenemos perfil de usuario logeado.
    received_follower_request=FollowersRequest.objects.filter(to_user=my_user.user)#buscamos las solicitudes enviadas.


    #lista de a quienes estamos siguiendo:
    followings = Profile.objects.filter(followers=my_user.id)#a quienes sigo.


    #lista donde guardaremos los usuarios a los que enviamos la solicitud de follow:
    follow_sent=[]
    #objetos en los cuales el usuario logeado haya enviado una solicitud de follow.
    sent_followers_requests = FollowersRequest.objects.filter(from_user=request.user)
    for se in sent_followers_requests:#recorremos los usuarios a los que el usuario logeado le mando la solicitud.
        #Append(),Este método nos permite agregar nuevos elementos a una lista.
        #Podemos agregar cualquier tipo de elemento a una lista, pero tengan en cuenta lo que pasa cuando agregamos una lista dentro de otra, esta lista se agrega como uno y solo un elemento.
        follow_sent.append(se.to_user)#ESTAMOS AGREGANDO A LA LISTA sent_to el campo to_user de los usuarios a los que se envio la solicitud de amistad.
    

    #mandamos url para enviar y cancel solicitudes:
    url_send = reverse('send_or_delete_follower_request')

    #mandamos url paraeliminar un seguidor:
    url_delete_following = reverse('delete_following')


    return render(request, 'users/request_follow_received.html', {'url_delete_following': url_delete_following, 'url_send': url_send, 'follow_sent': follow_sent, 'followings': followings, 'received_follower_request': received_follower_request})





#ListView:Una página que representa una lista de objetos.
class FollowersListView(LoginRequiredMixin, ListView):
    #NO HACE FALTA PONER model=Profile ya que vamos a pasar solo datos que nos interesean por eso usamos el metodo get_queryset
    context_object_name = 'followers'#nombre para manejar la lista como variable de plantilla, si no agregamos el nuestro propio la vista basada en ListView tiene su propio nombre.
    template_name = 'users/followers_list.html'#ESPECIFICAMOS NUESTRO propio nombre de templatename/location.
    paginate_by = 20#Cuantos objetos mostraremos por pagina.

    def get_queryset(self):#Obtenga la lista de elementos para esta vista. Debe ser iterable y puede ser un conjunto de consultas (en el que se habilitará el comportamiento específico del conjunto de consultas).
        #obtenemos solo los followers de quien miremos el perfil.
        pk_user=self.kwargs['pk']#OBTENEMOS EL PK que pasamos por url, pertenece al usuario ddel que vemos el eprfil.
        profile_user=get_object_or_404(Profile, user=pk_user)#obtenemos perfil del usuario de quein miramos sus seguidores.
        owner=profile_user.user
        followers=owner.profile.followers.all()#Seguidores del usuario
        return followers

    def get_context_data(self, **kwargs):#Lo usaremos para pasar el perfil del usuario del que vemos el perfil, esto para ver si estamos viendo nuestro perfil o otro perfil.
        ##Primero llamamos a la implementación base para obtener un contexto, o sea Primero obtenemos el contexto existente desde nuestra superclase, esto es lo que se hace con la siguiente linea.
        context = super(FollowersListView, self).get_context_data(**kwargs)
        
        #Usuario del que miramos los seguidores:
        user_pk=self.kwargs['pk']#OBTENEMOS EL PARAMETRO QUE PASAMOS POR URL  CON NOMBRE pk, este valor pertenece al id del pais donde estemos mirando las imagenes.
        user_profile=get_object_or_404(Profile, user=user_pk)#obtenemos perfil del usuario de quein miramos sus seguidores.
        owner=user_profile.user
        context['owner'] = owner# El fragmento muestra cómo añadir una variable llamada "id_user" al contexto (la misma estaría entonces disponible como una variable de plantilla).



        #lista donde guardaremos los usuarios a los que enviamos la solicitud de follow:
        follow_sent=[]
        #objetos en los cuales el usuario logeado haya enviado una solicitud de follow.
        sent_followers_requests = FollowersRequest.objects.filter(from_user=self.request.user)
        for se in sent_followers_requests:#recorremos los usuarios a los que el usuario logeado le mando la solicitud.
            #Append(),Este método nos permite agregar nuevos elementos a una lista.
            #Podemos agregar cualquier tipo de elemento a una lista, pero tengan en cuenta lo que pasa cuando agregamos una lista dentro de otra, esta lista se agrega como uno y solo un elemento.
            follow_sent.append(se.to_user)#ESTAMOS AGREGANDO A LA LISTA sent_to el campo to_user de los usuarios a los que se envio la solicitud de amistad.
        context['follow_sent'] = follow_sent
        
        #lista de a quienes estamos siguiendo:
        followings = Profile.objects.filter(followers=self.request.user.profile.id)#a quienes sigo.
        context['me_followings'] = followings

        #mandamos url para dejar de seguir a alguien:
        url_send = reverse('send_or_delete_follower_request')
        context['url_send'] = url_send

        url_delete_follower = reverse('delete_follower')
        context['url_delete_follower'] = url_delete_follower

        return context#Devolvemos el nuevo contexto (actualizado)






@login_required
def delete_follower(request):#vista para eliminar un seguidor, recibimos el id del seguidor.
    id_FDeleted = request.GET.get("FDeleted_id")#obtenemos la id mandada por ajax
    my_profile = request.user.profile#CARGAMOS EL USUARIO LOGEADO
    follower_profile = get_object_or_404(Profile, user=id_FDeleted)#EL id QUE USAMOS ACA CORRESPONDE AL id DEL USUARIO QUE NOS Sigue, SE RECIBE CUANDO SE DA EN "ELIMINAR SEGUIDOR, SI ES QUE NO QUERES QUE TE SIGA";
    my_profile.followers.remove(follower_profile)#ELIMINAMOS DE NUESTRO SEGUIDORES AL USUARIO CORRESPONDIENTE
    FDeleted=True
    resp = {
        'FDeleted':FDeleted
    }#ACA CREAMOS UN DICCIONARIO.
    response = json.dumps(resp)#creamos una respuesta codificada en json.
    #HttpResponse ( código fuente ) proporciona una solicitud HTTP entrante a una aplicación web Django con una respuesta de texto. Esta clase se usa con mayor frecuencia como un objeto de retorno desde una vista de Django.
    return HttpResponse(response, content_type = "application/json")#devolvemos una respuesta codificada en JSON.
    



#ListView:Una página que representa una lista de objetos.
class FollowingsListView(LoginRequiredMixin, ListView):
    #NO HACE FALTA PONER model=Profile ya que vamos a pasar solo datos que nos interesean por eso usamos el metodo get_queryset
    context_object_name = 'followings'#nombre para manejar la lista como variable de plantilla, si no agregamos el nuestro propio la vista basada en ListView tiene su propio nombre.
    template_name = 'users/followings_list.html'#ESPECIFICAMOS NUESTRO propio nombre de templatename/location.
    paginate_by = 20#Cuantos objetos mostraremos por pagina.

    def get_queryset(self):#Obtenga la lista de elementos para esta vista. Debe ser iterable y puede ser un conjunto de consultas (en el que se habilitará el comportamiento específico del conjunto de consultas).
        #obtenemos solo los followers de quien miremos el perfil.
        pk_user=self.kwargs['pk']#OBTENEMOS EL PK que pasamos por url, pertenece al usuario ddel que vemos el eprfil.
        user_profile=get_object_or_404(Profile, user=pk_user)#perfil usuario del que miramos a quien sigue
        followings = Profile.objects.filter(followers=user_profile.id)#a quienes sigo.
        return followings

    def get_context_data(self, **kwargs):#Lo usaremos para pasar el perfil del usuario del que vemos el perfil, esto para ver si estamos viendo nuestro perfil o otro perfil.
        ##Primero llamamos a la implementación base para obtener un contexto, o sea Primero obtenemos el contexto existente desde nuestra superclase, esto es lo que se hace con la siguiente linea.
        context = super(FollowingsListView, self).get_context_data(**kwargs)
        user_pk=self.kwargs['pk']#OBTENEMOS EL PARAMETRO QUE PASAMOS POR URL  CON NOMBRE pk, este valor pertenece al id del pais donde estemos mirando las imagenes.
        user_profile=get_object_or_404(Profile, user=user_pk)#obtenemos perfil del usuario de quein miramos sus sigueindos.
        owner=user_profile.user
        context['owner'] = owner# El fragmento muestra cómo añadir una variable llamada "id_user" al contexto (la misma estaría entonces disponible como una variable de plantilla).
        
        #mandamos url para enviar y cancel solicitudes:
        url_send = reverse('send_or_delete_follower_request')
        context['url_send'] = url_send


        #lista donde guardaremos los usuarios a los que enviamos la solicitud de follow:
        follow_sent=[]
        #objetos en los cuales el usuario logeado haya enviado una solicitud de follow.
        sent_followers_requests = FollowersRequest.objects.filter(from_user=self.request.user)
        for se in sent_followers_requests:#recorremos los usuarios a los que el usuario logeado le mando la solicitud.
            #Append(),Este método nos permite agregar nuevos elementos a una lista.
            #Podemos agregar cualquier tipo de elemento a una lista, pero tengan en cuenta lo que pasa cuando agregamos una lista dentro de otra, esta lista se agrega como uno y solo un elemento.
            follow_sent.append(se.to_user)#ESTAMOS AGREGANDO A LA LISTA sent_to el campo to_user de los usuarios a los que se envio la solicitud de amistad.
        context['follow_sent'] = follow_sent
        
        #lista de a quienes estamos siguiendo:
        followings = Profile.objects.filter(followers=self.request.user.profile.id)#a quienes sigo.
        context['me_followings'] = followings       



        return context#Devolvemos el nuevo contexto (actualizado)







@login_required
def delete_following(request):#vista para dejar de seguir a alguien, recibimos el id del seguidor.
    id_Following_Deleted = request.GET.get("id")#obtenemos la id mandada por ajax
    my_profile = request.user.profile#CARGAMOS EL USUARIO LOGEADO
    following_profile = get_object_or_404(Profile, user=id_Following_Deleted)#EL id del usuario al que dejamos de seguir.
    following_profile.followers.remove(my_profile)#Nos removemos de la lista de seguidores del usuario.
    Following_Deleted_ajax=True
    resp = {
        'Following_Deleted_ajax':Following_Deleted_ajax
    }#ACA CREAMOS UN DICCIONARIO.
    response = json.dumps(resp)#creamos una respuesta codificada en json.
    #HttpResponse ( código fuente ) proporciona una solicitud HTTP entrante a una aplicación web Django con una respuesta de texto. Esta clase se usa con mayor frecuencia como un objeto de retorno desde una vista de Django.
    return HttpResponse(response, content_type = "application/json")#devolvemos una respuesta codificada en JSON
    

@login_required
def search_user(request):
 
    search_user = request.GET.get('search_user')#Lo que está haciendo esta linea es decir, "Obtenga el valor de una variable POST con el nombre 'ACountry', que pertenece al input que enviamos, con el atributo name='ACountry'.
    if search_user:#para que no busque nada si la variable esta vacia, o sea si el usuario no ingreso nada para buscar
        #i__contains no distingue entre mayusculas y minusculas, pero si search_user es none hay problemas, por eso ponemos este if
        list_found = Profile.objects.filter(slug__icontains=search_user)#obtenemos perfil de usuario logeado.
        user_found=list_found.exclude(user=request.user)#Excluimos al usuario logeado de la lista
    else:
        user_found=False#si no se encontraron usuarios, ponemos esta variable en False



    #Nos fijamos si tenemos nuevos solicitudes de seguimiento, para luego indicarle al usuario de esto:
    received_follower_request=FollowersRequest.objects.filter(to_user=request.user).count()#buscamos las solicitudes recibidas.
        
 
    #lista donde guardaremos los usuarios a los que enviamos la solicitud de follow:
    follow_sent=[]
    #objetos en los cuales el usuario logeado haya enviado una solicitud de follow.
    sent_followers_requests = FollowersRequest.objects.filter(from_user=request.user)
    for se in sent_followers_requests:#recorremos los usuarios a los que el usuario logeado le mando la solicitud.
        #Append(),Este método nos permite agregar nuevos elementos a una lista.
        #Podemos agregar cualquier tipo de elemento a una lista, pero tengan en cuenta lo que pasa cuando agregamos una lista dentro de otra, esta lista se agrega como uno y solo un elemento.
        follow_sent.append(se.to_user)#ESTAMOS AGREGANDO A LA LISTA sent_to el campo to_user de los usuarios a los que se envio la solicitud de amistad.
        ##
    #lista de a quienes estamos siguiendo:
    followings = Profile.objects.filter(followers=request.user.profile.id)#a quienes sigo.

    #url para crear y cancelar solicitudes de seguimiento:
    url_send = reverse('send_or_delete_follower_request')

    return render(request, 'users/search_user.html', {'url_send': url_send, 'user_found':user_found, 'received_follower_request': received_follower_request, 'follow_sent': follow_sent, 'me_followings': followings})





#DeleteView:Una vista que muestra una página de confirmación y elimina un objeto existente.El objeto dado solo se eliminará si el método de solicitud es POST. Si esta vista se obtiene a través de GET, mostrará una página de confirmación que debe contener un formulario que se envía a la misma URL. 
class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):#vista para eliminar una publicación.
    model = User
    template_name = 'users/detele_user.html'#ESPECIFICAMOS NUESTRO propio nombre de templatename/location.
    


    #Limitar el acceso a los usuarios registrados que pasan una prueba ¶
    #Para limitar el acceso según ciertos permisos o alguna otra prueba, haría esencialmente lo mismo que se describe en la sección anterior
    #user_passes_test()toma un argumento requerido: un invocable que toma un Userobjeto y regresa Truesi el usuario tiene permiso para ver la página. Tenga en cuenta que user_passes_test()no comprueba automáticamente que Userno sea anónimo.
    #user_passes_test() es un decorador que se usa para vistas basadas en funciones, para vistas basadas en clsaes se usa el mixin UserPassesTestMixin.
    #test_func() :Debe anular el test_func()método de la clase para proporcionar la prueba que se realiza. Además, puede configurar cualquiera de los parámetros de AccessMixinpara personalizar el manejo de usuarios no autorizados:
    def test_func(self):
        #self.get_object(): Buscamos EL USUARIO que nos interesa.
        user = self.get_object()
        if self.request.user == user:#si el usurio logeado es el usuario que hizo la publicacion entra a este if.
            return True
        return False
    
    def get_context_data(self, **kwargs):#Lo usaremos para pasar el perfil del usuario del que vemos el perfil, esto para ver si estamos viendo nuestro perfil o otro perfil.
        ##Primero llamamos a la implementación base para obtener un contexto, o sea Primero obtenemos el contexto existente desde nuestra superclase, esto es lo que se hace con la siguiente linea.
        context = super(UserDeleteView, self).get_context_data(**kwargs)

        #TAMBIEN VAMOS A PASAR LA CANTIDAD DE MENSAJES QUE TENEMOS SIN LEER.
        messages_unreaded=Chat_Message.objects.filter(receiver=self.request.user).exclude(unread=1)#Excluimos los mensaje leidos

        context['messages_unreaded'] = messages_unreaded.count()

        return context#Devolvemos el nuevo contexto (actualizado)


    success_url = reverse_lazy('register')#SI COMENTAMOS ESTA LINEA SE REDIRIGIRA AL get_absolute_url DEL MODELO Post segun caracteristicas de una CreateView.






#vista para que el usuario pueda volver a ver los tutoriales
@login_required
def search_user_2(request):


    #Nos fijamos si tenemos nuevos solicitudes de seguimiento, para luego indicarle al usuario de esto:
    received_follower_request=FollowersRequest.objects.filter(to_user=request.user).count()#buscamos las solicitudes recibidas.
        

    return render(request, 'users/search_user_2.html', {'received_follower_request': received_follower_request})





@login_required
def list_notification(request):
    
    #SOLICITUDES DE SEGUIMIENTO RECIBIDAS:

    #Nos fijamos si tenemos nuevos solicitudes de seguimiento, para luego indicarle al usuario de esto:
    received_follower_request=FollowersRequest.objects.filter(to_user=request.user).count()#buscamos las solicitudes recibidas.
        
    #Agarramos la ultima solicitud que hayamos recibido:
    last_received_follower_request=FollowersRequest.objects.filter(to_user=request.user).last()

    #SOLICITUDES DE SEGUIMIENTO ENVIADAS:

    #Nos fijamos si HEMOS ENVIADO solicitudes de seguimiento, para luego indicarle al usuario de esto:
    sent_follower_request=FollowersRequest.objects.filter(from_user=request.user).count()#buscamos las solicitudes recibidas.
        
    #Agarramos la ultima solicitud que hayamos ENVIADO:
    last_sent_follower_request=FollowersRequest.objects.filter(from_user=request.user).last()

    return render(request, 'users/list_notification.html', {'received_follower_request': received_follower_request, 'last_received_follower_request': last_received_follower_request, 'sent_follower_request':sent_follower_request, 'last_sent_follower_request':last_sent_follower_request})



def login_anfitrion(request):
    user = authenticate(request, username='anfitrion', password='h3#As9@0')
    login(request, user)
    return redirect("home")