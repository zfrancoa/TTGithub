from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.contrib.auth.models import User

from django.urls import reverse_lazy

from django.contrib.auth.decorators import login_required
from .models import WorldCountries, WorldCountriesUser

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, DeleteView

import json
from django.http import HttpResponse
from django.http import JsonResponse

from users.models import Profile

from django.shortcuts import redirect


from publish.models import Post, Like

from telegram.models import Chat_Message


from .forms import AddCountryForm

from django.contrib import messages


# Create your views here.

@login_required
def index(request, pk):#en pk recibimos el id del usuario al que vemos su mapa
    m_name=get_object_or_404(Profile, user_id=pk)#obtenemos el nombre de usuario del que miramos el mapa.
    
    countries_added_list = []#lista donde se guardaran los paises agregados por el usuario.
    #aca abajo buscamos los paises que pertenezcan al usuario del que estemos viendo su perfil
    user_countries = WorldCountriesUser.objects.filter(username=m_name.user_id)

    for item in user_countries:#recorremos y guardamos en una lista los paises
        countries_added_list.append(item.countries_user)

    #Ahora que tenemos los nombres de los paises, buscamos los id:
    #lista donde guardaremos los objetos que contiene id y nombre del pais:
    country_list = []
    for i in user_countries :
        c_f = WorldCountries.objects.get(countries_tot = i.countries_user)
        country_list.append(c_f)



    #sesion que nos indica si debemos mostrar el tutorial o no:
    view_tutorial = request.session.get('view_tutorial', 'True')

    url_session_tutorial = reverse('tutorial_add_photo_to_country_session')


    #URL DESDE LA QUE LLEGUE:
    referer = request.META.get('HTTP_REFERER')

    url_home = reverse('home')

    url_myprofile = reverse('myprofile')

    url_user_profile = reverse('user_profile', kwargs={'username': m_name.slug})

    if referer:

        if url_home in referer:
            referer = url_home

        elif url_myprofile in referer:
            referer = url_myprofile

        elif url_user_profile in referer:
            referer = url_user_profile

        else:#esta opcion seria para cuando se llegue desde Galleryview, home, FeaturedCreateview
            referer = reverse('home')
    else:
        referer = reverse('home')



    return render(request, 'maps/index.html', {'referer': referer, 'country_list': country_list, 'm_name':m_name, 'countries_added_list':countries_added_list, 'view_tutorial':view_tutorial, 'url_session_tutorial': url_session_tutorial})





#¿Cuándo usar CreateView?
#CreateView debe usarse cuando necesite un formulario en la página y necesite hacer una inserción de base de datos al enviar un formulario válido.
#En vistas basada en clase no se puede usar el decorador @login_required, por eso se usa LoginRequiredMixin.
#CreateView:Una vista que muestra un formulario para crear un objeto, volver a mostrar el formulario con errores de validación (si los hay) y guardar el objeto.
class AddPhotoCreateView(LoginRequiredMixin, CreateView):#vista para crear una publicación.
    model = Post
    fields = ['body', 'pic']#estos tres campos nos apareceran en el formulario, user_post y time_post se agregaran automaticamente ya que sabemos que el usuario que crea una publicaicon es el logeado, el tiempo ya tiene un default.
    #template_name indica donde la vista buscara el formulario que se usa para la creacion del post.
    template_name = 'maps/add_photo.html'#ESPECIFICAMOS NUESTRO propio nombre de templatename/location.


    #get_success_url solo debe devolver la URL a la que redireccionar, no la respuesta de redireccionamiento.
    def get_success_url(self, **kwargs):
        id_country = self.kwargs['pk']
        user_loged=self.request.user.username
        return '{}'.format(reverse('GalleryView', kwargs={'pk': id_country, 'username': user_loged}))



    #El formulario permitira cargar los campos pic, body, pero falta agregar el usuario, el cual es el logeado.
    #esto es lo que se hace con el metodo form_valid
    def form_valid(self, form):
        #OBTENEMOS LOS OBJETOS QUE SOLO NOS INTERESAN.
        pk_received=self.kwargs['pk']#OBTENEMOS EL PARAMETRO QUE PASAMOS POR URL  CON NOMBRE pk, este valor pertenece al id del pais donde estemos mirando las imagenes.
        #para buscar los post adecuados, lo hacemos por medio del campo tags del metodo post, pero este tags en un char, por lo tanto vmaos a  encontrar el nombre del pais al cual corresponde el id recibido:
        name_country = WorldCountries.objects.get(id=pk_received)
        form.instance.tags=name_country
        form.instance.user_post = self.request.user#agregamos el nombre del usuario dueño
        return super().form_valid(form)
    

    #ACA SobreescribiMoS métodos en vistas basadas en clases:
    #EN ESTE CASO SOBREESCRIBIMOS EL METODO get_context_data(), que tiene por objeto pasar variables de contexto adicionales a la plantilla.
    def get_context_data(self, **kwargs):
        ##Primero llamamos a la implementación base para obtener un contexto, o sea Primero obtenemos el contexto existente desde nuestra superclase, esto es lo que se hace con la siguiente linea.
        context = super(AddPhotoCreateView, self).get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']#pasamos el id del pais.
       
       
        #URL DESDE LA QUE LLEGUE:
        referer = self.request.META.get('HTTP_REFERER')

        if referer:
            context['referer'] = referer
        else:
            context['referer'] = reverse('home')
        
        return context


    #Ni siquiera es necesario que proporciones un success_url para CreateView o UpdateView, se usarán get_absolute_url()en el objeto de modelo si está disponible.
    #success_url: La URL a la que se redireccionará cuando el formulario se procese correctamente.
    #pero aca como luego de crear el post queremos redireccionar home si pones el success_url.
    #success_url = reverse_lazy('GalleryView', self.kwargs['pk'], self.request.user.username)#SI COMENTAMOS ESTA LINEA SE REDIRIGIRA AL get_absolute_url DEL MODELO Post segun caracteristicas de una CreateView.


#--------------------------------------------------------------------------------#







#Vista genérica basadas en clases.
#Esta vista será en realidad implementada como una clase. Heredaremos desde una función de vista genérica existente que ya hace la mayoría de lo que queremos que esta función de vista haga, en lugar de escribir la nuestra propia desde el inicio.
#ListView: vista de lista genérica basada en clases (ListView).
# (ListView) -- una clase que hereda desde una vista existente. Debido a que la vista genérica ya implementa la mayoría de la funcionalidad que necesitamos, y sigue la práctica adecuada de Django, seremos capaces de crear una vista de lista más robusta con menos código, menos repetición, y por último menos mantenimiento. 
class GalleryView(LoginRequiredMixin, ListView):#esta vista maneja la visualización de todas las publicaciones en un orden que coloca las publicaciones más nuevas en primer lugar. Cada página muestra 10 publicaciones y luego debemos pasar a la página siguiente para ver más. Además, si el usuario no está autenticado, no le damos la opción de dar me gusta en la publicación. Si el usuario está autenticado, mostramos si al usuario le ha gustado o no.
    #ES IMPORTANTE SABER QUE ESTA VISTA TIENE QUE RECIBIR DOS DATOS, EL ID DEL PAIS Y EL NOMBRE DE USUARIO, CON EL FIN DE PODER FILTRAR LAS IMAGENES CORREPONDIENTES.
    
    model = Post
    #SI solo definimos esto, lo siguiente es lo que ocurre:
    #La vista genérica consultará a la base de datos para obtener todos los registros del modelo especificado (Post) y renderizará una plantilla ubicada en /librodedeportes/publish/templates/publish/post_list.html. Dentro de la plantilla puedes acceder a la lista de post mediante la variable de plantilla llamada object_list O post_list (esto es, genéricamente, "nombre_del_modelo_list").
    #Esta ruta complicada para la ubicación de la plantilla no es un error de digitación -- las vistas genéricas buscan plantillas en /application_name/the_model_name_list.html (publish/post_list.html en este caso) dentro del directorio de la aplicación /application_name/templates/ (/publish/templates/).
    ######################
    #Se Pueden añadir atributos para cambiar el comportamiento por defecto explicado arriba, y es lo que hacemos abajo.
    template_name = 'maps/gallery.html'#ESPECIFICAMOS NUESTRO propio nombre de templatename/location.
    context_object_name = 'images'#ACA CAMBIAMOS LA VARIABLE DE PLANTILLA(QUE ORIGINALMENTE ERA post_list) QUE SE USA PARA ACCEDER A LA LISTA DE LAS PUBLICACIONES.
    #ordering = ['-date_posted']#ORDENAREMOS LA LISTA DE PUBLICACIONES OBTENIDA POR FECHA DE PUBLICACIÓN, LAS ULTIMAS EN PUBLICARSE SERAN LAS PRIMERAS EN MOSTRARSE.
    #paginate_by:agrega un paginator y page_obj al context. Para permitir que sus usuarios naveguen entre páginas.
    paginate_by = 10#MOSTRAREMOS DE A 10 PUBLICACIONES.

    def get_queryset(self):#Obtenga la lista de elementos para esta vista. Debe ser iterable y puede ser un conjunto de consultas (en el que se habilitará el comportamiento específico del conjunto de consultas).
        #OBTENEMOS LOS OBJETOS QUE SOLO NOS INTERESAN.
        received_pk=self.kwargs['pk']#OBTENEMOS EL PARAMETRO QUE PASAMOS POR URL  CON NOMBRE pk, este valor pertenece al id del pais donde estemos mirando las imagenes.
        #para buscar los post adecuados, lo hacemos por medio del campo tags del metodo post, pero este tags en un char, por lo tanto vmaos a  encontrar el nombre del pais al cual corresponde el id recibido:
        name_country = WorldCountries.objects.get(id=received_pk)#usamos get y no filter porque cuando se sabe que solo habra un objeto coincidente es mas eficiente usar get, ademas se obtiene el valor del registro y no un query set, en el caso en que solo haya un reigstro.

        name_user_received=self.kwargs['username']#OBTENEMOS EL OTRO PARAMETRO PASADO POR URL, EN ESTE CASO ES EL NOMBRE DE USUARIO DEL CUAL ESTEMOS MIRANDO EL MAPA.
        #DE ESTE USUARIO NECESITAMOS SU ID NO SU NOMBRE, YA QUE EN EL MODELO POST, CADA POST SE GUARDA CON EL ID DEL USUARIO NO CON SU NOMBRE DE USUARIO.
        received_id_user = Profile.objects.get(slug=name_user_received)

        imgs=Post.objects.filter(user_post=received_id_user.user_id, tags=name_country)#RETORNAMOS LO QUE NOSOTROS QUEREMOS, IMAGENES CORRESPONDIENTES A PAIS Y USUARIO.
        #LLAMAR AL METODO get_queryset anula a ordering, POR LO TANTO DEBEMOS ORDENARLO NOSOTROS, HAY OTRA FORMA, USANDO LA CLASE super CUANDO SE LLAMA AL METODO get_queryset NO SE ANULA EL METODO ordering.
        imgs = imgs.order_by('-time_post')
        return imgs

    #ACA SobreescribiMoS métodos en vistas basadas en clases:
    #EN ESTE CASO SOBREESCRIBIMOS EL METODO get_context_data(), que tiene por objeto pasar variables de contexto adicionales a la plantilla.
    def get_context_data(self, **kwargs):
        ##Primero llamamos a la implementación base para obtener un contexto, o sea Primero obtenemos el contexto existente desde nuestra superclase, esto es lo que se hace con la siguiente linea.
        context = super(GalleryView, self).get_context_data(**kwargs)

        user_name_received=self.kwargs['username']#Recibimos el nombre de usuario, que lo pasamos a traves de la url.
        pk_received=self.kwargs['pk']#OBTENEMOS EL PARAMETRO QUE PASAMOS POR URL  CON NOMBRE pk, este valor pertenece al id del pais donde estemos mirando las imagenes.

        user_obj = User.objects.get(username=user_name_received)#como sabemos que solo habra un usuario que coincida con slug=username usamos el metodo get, lo que queremos es el id de este usuario par aluego buscar las imagenes correspondientes.


        name_country = WorldCountries.objects.get(id=pk_received)#usamos get y no filter porque cuando se sabe que solo habra un objeto coincidente es mas eficiente usar get, ademas se obtiene el valor del registro y no un query set, en el caso en que solo haya un reigstro.

        #EN LA SIGUIENTE LINEA añadimos al contexto la información extra que queremos.
        context['pk_received'] = pk_received# El fragmento muestra cómo añadir una variable llamada "id_user" al contexto (la misma estaría entonces disponible como una variable de plantilla).
        context['user_obj'] = user_obj.profile# El fragmento muestra cómo añadir una variable llamada "id_user" al contexto (la misma estaría entonces disponible como una variable de plantilla).
        context['name_country'] = name_country# El fragmento muestra cómo añadir una variable llamada "id_user" al contexto (la misma estaría entonces disponible como una variable de plantilla).
        
        #publicaciones a las que se le dio like:
        liked = [i for i in Post.objects.all() if Like.objects.filter(user_like = self.request.user, post_like=i)]#se recorren y se filtran los post en los cuales el usuario logeado dio me gusta.
        #EN LA SIGUIENTE LINEA añadimos al contexto la información extra que queremos.
        context['liked_post'] = liked# El fragmento muestra cómo añadir una variable llamada "liked_post" al contexto (la misma estaría entonces disponible como una variable de plantilla).
        #

        #URL DESDE LA QUE LLEGUE:
        referer = self.request.META.get('HTTP_REFERER')

        #POSIBLES LUGARES DESDE DONDE SE PUEDE LLEGAR A ESTA VISTA:
        #URL de mi perfil:
        url_upload_photo = reverse('upload_photo')
        #URL de home:
        url_map = reverse('index', kwargs={'pk': user_obj.id})
        if referer:#primero nos fijamos de donde venimos, y si existe una url
            if url_upload_photo in referer:#nos fijamos si venimos de url_upload_photo 
                context['referer'] = url_upload_photo
            else:#si no venimos de  url_upload_photo
                if url_map in referer:#si venimos de url_FeaturedPostListView
                    context['referer'] = url_map
                else:#sino venimos de ninguna de las dos anteriores:
                   context['referer'] = reverse('home')
        else:#url fuera de traveltry, o estando en traveltry escribir la url a mano
            context['referer'] = reverse('home')

        
        return context#Devolvemos el nuevo contexto (actualizado)



@login_required
def Add_Country(request):

    #ACA TRATAREMOS EL FOMRULARIO
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        #pasamos el usuario que llama al formulario, con el fin de que lo podamos usar en el metodo clean de form.py, y asi poder validar el campo de pais:
        form = AddCountryForm(request.user, request.POST)
        # check whether it's valid:
        if form.is_valid():
            #nootros cargamos el campo del pais, pero no que usuario agrega el pais, esto lo haremos aca dentro.
            # process the data in form.cleaned_data as required
            #Para guardar un objeto en la base de datos, llame a save().
            #Si llama save()con commit=False, devolverá un objeto que aún no se ha guardado en la base de datos. En este caso, depende de usted llamar save()a la instancia del modelo resultante. Esto es útil si desea realizar un procesamiento personalizado en el objeto antes de guardarlo, o si desea utilizar una de las opciones especializadas para guardar modelos .
            data = form.save(commit=False)
            #CON LO DICHO ARRIBA, VEMOS QUE ANTES DE GUARDAR EL OBJETO EN LA BASE DE DATOS, RELLENAMOS ALGUNOS CAMPOS(en este caso el nombre usuario de quien agrego el pais), luego lo guardamos en la base de datos(guardamos el nuevo objeto(instancia de formulario) en la base de datos).
            data.username = request.user
            #AHORA GUARDAMOS EL OBJETO EN LA BBDD.
            data.save()

            # return HttpResponseRedirect('/thanks/')
            #obtenemos id del usuario logeado:
            id_logued=request.user.id
            return redirect('index', pk=id_logued)

    # if a GET (or any other method) we'll create a blank form
    else:
        #pasamos el usuario que llama al formulario, con el fin de que lo podamos usar en el metodo clean de form.py, y asi poder validar el campo de pais:
        form = AddCountryForm(request.user, request.GET)


        #URL DESDE LA QUE LLEGUE:
        referer = request.META.get('HTTP_REFERER')

        url_upload_photo = reverse('upload_photo')

        url_map = reverse('index', kwargs={'pk': request.user.id})

        if referer:

            if url_upload_photo in referer:
                referer = url_upload_photo

            elif url_map in referer:
                referer = url_map

            else:#esta opcion seria para cuando se llegue desde Galleryview, home, FeaturedCreateview
                referer = reverse('home')
        else:
            referer = reverse('home')

    

    return render(request, 'maps/add_country.html', {'referer': referer, 'form': form})






@login_required
def search_country_ajax(request):#para el ajax
    #obtenemos lo enviado por ajax:
    written = request.GET.get("written", "")
    #obtenemos los paises coincidentes:
    if written:#nos fijamos si se escribio algo
        #i__contains no distingue entre mayusculas y minusculas, pero si lo que se ingresa al input es none hay problemas, por eso ponemos este if
        #obtenemos solo los primeros 10 objetos, para que no haya sobrecarga.
        countries_found = WorldCountries.objects.filter(countries_tot__icontains=written)[:10]
        created=True
        countries_list=[]#lista de los id de mensajes no leidos
        #json_list = [1,2,3,'String1']
        for item in countries_found:
            countries_list.append(item.countries_tot)#sGUARDAMOS EL ID EN LA LISTA  
    else:
        created=False
        countries_list=[]
    resp = {
        'created':created,
        'countries_list':countries_list
    }#ACA CREAMOS UN DICCIONARIO.
    response = json.dumps(resp)#creamos una respuesta codificada en json.
    #HttpResponse ( código fuente ) proporciona una solicitud HTTP entrante a una aplicación web Django con una respuesta de texto. Esta clase se usa con mayor frecuencia como un objeto de retorno desde una vista de Django.
    return HttpResponse(response, content_type = "application/json")#devolvemos una respuesta codificada en JSON




#########------------------------------------------#########

#esta vista le pasa el id del objeto a la vista CountryDeleteView, la cual se encarga de eliminar el objeto.
@login_required
def Delete_Country(request):

    #ACA TRATAREMOS EL FORMULARIO
    if request.method == 'POST':

        #vamos a obtener los paises que el usuario tiene agregado:
        added_countries = WorldCountriesUser.objects.filter(username=request.user)

        #TAMBIEN VAMOS A PASAR LA CANTIDAD DE MENSAJES QUE TENEMOS SIN LEER.
        messages_unreaded=Chat_Message.objects.filter(receiver=request.user).exclude(unread=1)#Excluimos los mensaje leidos


        country_delete = request.POST.get('country_delete')#Lo que está haciendo esta linea es decir, "Obtenga el valor de una variable POST con el nombre 'country_delete', que pertenece al input que enviamos, con el atributo name='country_delete', este input es parte del formulario.
        #nos fijamos si este pais existe y el usuario no ingreso cualquier cosa:
        exist_country = WorldCountries.objects.filter(countries_tot=country_delete)
        if exist_country:#si entra, significa que el pais existe
            #nos fijamos si el usuario tiene al pais agregado:
            exist_country_user=WorldCountriesUser.objects.filter(countries_user=country_delete, username=request.user).first()
            if exist_country_user:#entra si el usuario ya ha agregado el pais
                return redirect('CountryDeleteView', pk=exist_country_user.id)
            else:
                messages.add_message(request, messages.INFO, 'You do not have the country added.')#Este mensaje lo podremos llamar en el template, no hace falta agregarlo al contexto.
    
        else:
            messages.add_message(request, messages.INFO, 'The country entered does not exist.')#Este mensaje lo podremos llamar en el template, no hace falta agregarlo al contexto.    
    # if a GET (or any other method) we'll create a blank form
    else:
        #vamos a obtener los paises que el usuario tiene agregado:
        added_countries = WorldCountriesUser.objects.filter(username=request.user)

        #TAMBIEN VAMOS A PASAR LA CANTIDAD DE MENSAJES QUE TENEMOS SIN LEER.
        messages_unreaded=Chat_Message.objects.filter(receiver=request.user).exclude(unread=1)#Excluimos los mensaje leidos


    return render(request, 'maps/what_country_delete.html', {'messages_unreaded':messages_unreaded.count(), 'added_countries':added_countries})




#DeleteView:Una vista que muestra una página de confirmación y elimina un objeto existente. El objeto dado solo se eliminará si el método de solicitud es POST. Si esta vista se obtiene a través de GET, mostrará una página de confirmación que debe contener un formulario que se envía a la misma URL.
#UserPassesTestMixin: le permite definir una función de prueba(en este caso, test_func) que debe devolver True si el usuario actual puede acceder a la vista.
class CountryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):#vista para eliminar una publicación.
    model = WorldCountriesUser
    template_name = 'maps/DeleteCountry_View.html'#ESPECIFICAMOS NUESTRO propio nombre de templatename/location.
    


    #Limitar el acceso a los usuarios registrados que pasan una prueba ¶
    #Para limitar el acceso según ciertos permisos o alguna otra prueba, haría esencialmente lo mismo que se describe en la sección anterior
    #user_passes_test()toma un argumento requerido: un invocable que toma un Userobjeto y regresa Truesi el usuario tiene permiso para ver la página. Tenga en cuenta que user_passes_test()no comprueba automáticamente que Userno sea anónimo.
    #user_passes_test() es un decorador que se usa para vistas basadas en funciones, para vistas basadas en clsaes se usa el mixin UserPassesTestMixin.
    #test_func() :Debe anular el test_func()método de la clase para proporcionar la prueba que se realiza. Además, puede configurar cualquiera de los parámetros de AccessMixinpara personalizar el manejo de usuarios no autorizados:
    def test_func(self):
        #self.get_object(): Buscamos la publicacion que nos interesa.
        country = self.get_object()
        if self.request.user == country.username:#si el usurio logeado es el usuario que hizo la publicacion entra a este if.
            return True
        return False


    #ACA SobreescribiMoS métodos en vistas basadas en clases:
    #EN ESTE CASO SOBREESCRIBIMOS EL METODO get_context_data(), que tiene por objeto pasar variables de contexto adicionales a la plantilla.
    def get_context_data(self, **kwargs):
        ##Primero llamamos a la implementación base para obtener un contexto, o sea Primero obtenemos el contexto existente desde nuestra superclase, esto es lo que se hace con la siguiente linea.
        context = super(CountryDeleteView, self).get_context_data(**kwargs)
        
        messages_unreaded=Chat_Message.objects.filter(receiver=self.request.user).exclude(unread=1)#Excluimos los mensaje leidos
        context['messages_unreaded'] = messages_unreaded.count()
        
        return context#Devolvemos el nuevo contexto (actualizado)



    def get_success_url(self):
        return reverse('index', kwargs={'pk': self.request.user.id})


    
#########------------------------------------------#########





@login_required
def give_name_get_id(request):

    country_name = request.GET.get("name", "")
    
    # print("nombre encontrado")
    # print(country_name)

    country_found = WorldCountries.objects.filter(countries_tot = country_name).first()
    #print(country_found.id)

    if country_found:
        Created = True
        country_f = country_found.id
    else:
        Created = False
        country_f = False

    resp = {
        'Created': Created,
        'country_found': country_f,
    }#ACA CREAMOS UN DICCIONARIO.

    response = json.dumps(resp)#creamos una respuesta codificada en json.
    #HttpResponse ( código fuente ) proporciona una solicitud HTTP entrante a una aplicación web Django con una respuesta de texto. Esta clase se usa con mayor frecuencia como un objeto de retorno desde una vista de Django.
    
    return HttpResponse(response, content_type = "application/json")#devolvemos una respuesta codificada en JSON




#Vista para agregar sesion cuando un usuario aprete en no volver a mostrar el tutorial
@login_required
def tutorial_add_photo_to_country_session(request):

    # El False significa que no queremos ver el tutorial:
    #view_tutorial = request.session.get('view_tutorial', 'True')
    request.session['view_tutorial'] = False

    resp = {
        'state': 'success',
    }#ACA CREAMOS UN DICCIONARIO.

    response = json.dumps(resp)#creamos una respuesta codificada en json.
    #HttpResponse ( código fuente ) proporciona una solicitud HTTP entrante a una aplicación web Django con una respuesta de texto. Esta clase se usa con mayor frecuencia como un objeto de retorno desde una vista de Django.
    
    return HttpResponse(response, content_type = "application/json")#devolvemos una respuesta codificada en JSON




