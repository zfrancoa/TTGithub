from django.shortcuts import get_object_or_404, render
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post, Like, Sharing_Post, Comments
from django.urls import reverse_lazy
from .forms import CommentForm, ReportPostForm

from django.contrib.auth.models import User

from users.models import Profile, FollowersRequest

from map.models import WorldCountriesUser, WorldCountries

from django.http import HttpResponseForbidden
from django.urls import reverse
from django.views.generic.detail import SingleObjectMixin

from django.views import View

from django.http import HttpResponse
import json


from telegram.models import Chat_Message

from .models import Sharing_Post

from django.shortcuts import redirect

from django.contrib.auth.decorators import login_required


# Create your views here.


#ListView:Una página que representa una lista de objetos.
class HomeListView(LoginRequiredMixin, ListView):
    model = Post
    context_object_name = 'postings'#nombre para manejar la lista como variable de plantilla, si no agregamos el nuestro propio la vista basada en ListView tiene su propio nombre.
    template_name = 'publish/home.html'#ESPECIFICAMOS NUESTRO propio nombre de templatename/location.
    ordering = ['-time_post']#ORDENAREMOS LA LISTA DE PUBLICACIONES OBTENIDA POR FECHA DE PUBLICACIÓN, LAS ULTIMAS EN PUBLICARSE SERAN LAS PRIMERAS EN MOSTRARSE.
    paginate_by = 10#Cuantos objetos mostraremos por pagina.


    def get_queryset(self):#Obtenga la lista de elementos para esta vista. Debe ser iterable y puede ser un conjunto de consultas (en el que se habilitará el comportamiento específico del conjunto de consultas).
        followings = Profile.objects.filter(followers=self.request.user.profile.id)#a quienes sigo.
        #OBTENEMOS LOS OBJETOS QUE SOLO NOS INTERESAN.
        followings_post=[]
        for i in followings:
            #agregamos los post publicados de cada usuario:
            followings_post+=Post.objects.filter(user_post=i.user)#RETORNAMOS LO QUE NOSOTROS QUEREMOS, IMAGENES CORRESPONDIENTES A PAIS Y USUARIO.
            #agregamos los post compartidos por cada usuario:
            followings_post+=Sharing_Post.objects.filter(the_user=i.user)
        #agregamos los post del propio usuario:
        followings_post+=Post.objects.filter(user_post=self.request.user)
        #agregamos los psot compartidos del propio usuario:
        followings_post+=Sharing_Post.objects.filter(the_user=self.request.user)

        #LLAMAR AL METODO get_queryset anula a ordering, POR LO TANTO DEBEMOS ORDENARLO NOSOTROS, HAY OTRA FORMA, USANDO LA CLASE super CUANDO SE LLAMA AL METODO get_queryset NO SE ANULA EL METODO ordering.
        #COMO followings_post es una lista y no un queryset no podemos hacer imgs = followings_post.order_by('-time_post') para ordenar los post.
        #followings_post ES UNA LISTA DE OBJETOS, POR ENDE SE UTILIZA LA SIGUIENTE LINEA:
        imgs=sorted(followings_post, key=lambda x: x.time_post, reverse=True)
        #order_by no esta disponible para una lista.

        return imgs


    #ACA SobreescribiMoS métodos en vistas basadas en clases:
    #EN ESTE CASO SOBREESCRIBIMOS EL METODO get_context_data(), que tiene por objeto pasar variables de contexto adicionales a la plantilla.
    def get_context_data(self, **kwargs):
        ##Primero llamamos a la implementación base para obtener un contexto, o sea Primero obtenemos el contexto existente desde nuestra superclase, esto es lo que se hace con la siguiente linea.
        context = super(HomeListView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:#entra aca si el usuario esta autenticado, o sea si esta logeado.
            liked = [i for i in Post.objects.all() if Like.objects.filter(user_like = self.request.user, post_like=i)]#se recorren y se filtran los post en los cuales el usuario logeado dio me gusta.
            #EN LA SIGUIENTE LINEA añadimos al contexto la información extra que queremos.
            context['liked_post'] = liked# El fragmento muestra cómo añadir una variable llamada "liked_post" al contexto (la misma estaría entonces disponible como una variable de plantilla).
            #TAMBIEN VAMOS A PASAR LA CANTIDAD DE MENSAJES QUE TENEMOS SIN LEER.
            messages_unreaded=Chat_Message.objects.filter(receiver=self.request.user).exclude(unread=1)#Excluimos los mensaje leidos
            context['messages_unreaded'] = messages_unreaded.count()



        #Nos fijamos si tenemos nuevos solicitudes de seguimiento, para luego indicarle al usuario de esto:
        received_follower_request=FollowersRequest.objects.filter(to_user=self.request.user).count()#buscamos las solicitudes recibidas.
        context['received_follower_request'] = received_follower_request


        return context#Devolvemos el nuevo contexto (actualizado)


    #SOLO FILTRAREMOS LOS Post PERSONALES Y LOS QUE PERTENEZCAN A NUESTROS FOLLOWINGS.




#¿Cuándo usar CreateView?
#CreateView debe usarse cuando necesite un formulario en la página y necesite hacer una inserción de base de datos al enviar un formulario válido.
#En vistas basada en clase no se puede usar el decorador @login_required, por eso se usa LoginRequiredMixin.
#CreateView:Una vista que muestra un formulario para crear un objeto, volver a mostrar el formulario con errores de validación (si los hay) y guardar el objeto.
class PostCreateView(LoginRequiredMixin, CreateView):#vista para crear una publicación.
    model = Post
    fields = ['tags', 'body', 'pic']#estos tres campos nos apareceran en el formulario, user_post y time_post se agregaran automaticamente ya que sabemos que el usuario que crea una publicaicon es el logeado, el tiempo ya tiene un default.
    #template_name indica donde la vista buscara el formulario que se usa para la creacion del post.
    template_name = 'publish/create_post.html'#ESPECIFICAMOS NUESTRO propio nombre de templatename/location.

    #El formulario permitira cargar los campos pic, body y tags, pero falta agregar el usuario, el cual es el logeado.
    #esto es lo que se hace con el metodo form_valid
    def form_valid(self, form):
        form.instance.user_post = self.request.user#agregamos el nombre del usuario dueño
        return super().form_valid(form)
    

    #Ni siquiera es necesario que proporciones un success_url para CreateView o UpdateView, se usarán get_absolute_url()en el objeto de modelo si está disponible.
    #success_url: La URL a la que se redireccionará cuando el formulario se procese correctamente.
    #pero aca como luego de crear el post queremos redireccionar home si pones el success_url.
    success_url = reverse_lazy('home')#SI COMENTAMOS ESTA LINEA SE REDIRIGIRA AL get_absolute_url DEL MODELO Post segun caracteristicas de una CreateView.


#--------------------------------------------------------------------------------#

#VAMOS A usar dos vistas basadas en clases diferentes desde la misma URL.
#Tenemos una división muy clara aquí: las solicitudes GET deben obtener DetailView (con el Form ulario agregado a los datos de contexto) y las solicitudes POST deben obtener FormView . Primero configuremos esas vistas.
class PostDetailView(LoginRequiredMixin, DetailView):#vista para crear una publicación.
    model = Post
    template_name = 'publish/post_detail.html'#ESPECIFICAMOS NUESTRO propio nombre de templatename/location.
    #tenemos que escribir nuestro propio get_context_data() para que CommentForm esté disponible para la plantilla
    #get_context_data:Devuelve un diccionario que representa el contexto de la plantilla . Los argumentos de palabra clave proporcionados formarán el contexto devuelto.
    #en este caso lo usaremos para pasar el form en una consulta get
    def get_context_data(self, **kwargs):
        #¿QUE HACE context = super().get_context_data(**kwargs)?:Aquí, por lo tanto, hacemos una llamada a la función siguiente en el orden de resolución del método (MRO) . Este suele ser el padre de una clase, aunque las reglas del MRO son un poco más complejas en el caso de herencia múltiple . La razón es que estos padres también pueden agregar datos al contexto. Entonces, al llamar al get_context_datadel padre, el padre devuelve un diccionario que podría contener algunos datos, y luego el niño (s) puede, a su vez, agregar más datos al context(o cambiarlo), en orden MRO inverso . Sin embargo, esto solo sucederá si cada niño realiza una super().get_context_data(**kwargs)llamada y parchea el resultado (y por lo tanto no construye un nuevo diccionario).
        #EN OTRAS PALABRAS NOS PERMITE AGREGAR CONTEXTO SIN ELIMINAR EL QUE YA ENTREGA EL PADRE(DetailView).
        context = super(PostDetailView, self).get_context_data(**kwargs)#llamamos el contexto que ya teemos para luego agregarle extra y asi no borrar el contexto que ya tenemos.
        context['form'] = CommentForm()#aca agregamos el formulario al contexto que ya entrega la DetailView
        #LAS SIGUEINTES LINEAS SON PARA VER SI SE DIO LIKE AL POST QUE ESTAMOS VIENDO.
        pk_received=self.kwargs['pk']#obtenemos el dato que mandamos por la url.
        post = get_object_or_404(Post, pk=pk_received) #LLAMAMOS AL MODELO Post Y OBTENEMOS EL post(todos sus campos) AL QUE SE LE dio click en la imagen(lo que nos redirige a la pagina post-detail).
        if Like.objects.filter(user_like=self.request.user, post_like=post):
            is_liked=True#la publiccaion tiene like
        else:
            is_liked=False#la publicacion no tiene like
        context['is_liked'] = is_liked#agregamos este objeto al contexto para saber si se dio like al post que estamos viendo
        
        #Nos fijamos si tenemos nuevos solicitudes de seguimiento, para luego indicarle al usuario de esto:
        received_follower_request=FollowersRequest.objects.filter(to_user=self.request.user).count()#buscamos las solicitudes recibidas.
        context['received_follower_request'] = received_follower_request

        
        #DATOS PARA ARMAR EL COMENTARIO DINAMICACMENTE:
        url_delete_comment = reverse('delete_comment')
        context['url_delete_comment'] = url_delete_comment
        url_myprofile = reverse('myprofile')
        context['url_myprofile'] = url_myprofile
        url_photo = self.request.user.profile.photo.url
        context['url_photo'] = url_photo
        user_name = self.request.user.username
        context['user_name'] = user_name



        #URL DESDE LA QUE LLEGUE:
        referer = self.request.META.get('HTTP_REFERER')

        #obtendremos el usuario a traves de la publicacion:
        post_pk=self.kwargs['pk']
        post=Post.objects.filter(id=post_pk).first()


        url_home = reverse('home')
        url_FeaturedPostListView = reverse('FeaturedPostListView', kwargs={'pk': post.user_post.id})
        

        if referer:

            if url_FeaturedPostListView in referer:
                context['referer'] = url_FeaturedPostListView

            elif url_home in referer:
                context['referer'] = url_home

            else:#esta opcion seria para cuando se llegue desde Galleryview.
                context['referer'] = referer
        else:
            context['referer'] = reverse('home')


        return context



#Tenemos que traer SingleObjectMixin para que podamos encontrar la publicacion que estamos mirando, y debemos recordar establecer template_name para asegurarnos de que los errores de formulario generarán la misma plantilla que PostDetailView está usando en GET :
class PostFormView(LoginRequiredMixin, SingleObjectMixin, FormView):
    template_name = 'publish/post_detail.html'
    form_class = CommentForm
    model = Post

    #el metodo def post(self, request, *args, **kwargs): es como la linea if request.method == "POST": de una vista basada en funciones.
    #Self se refiere a la clase en sí y se usa en los métodos GET y POST para pasar la plantilla y el formulario como contexto. request es el mismo objeto de solicitud HTTP que se usa normalmente en FBV que contiene metadatos en la ruta / usuario / método / etc. * Args y * kwargs representan cualquier argumento o argumento de palabra clave pasado como parámetros de URL
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:#entra aca si el usuario no esta autenticado.
            return HttpResponseForbidden()
        form = CommentForm(request.POST)
        self.object = self.get_object()
        if form.is_valid():
            #Para guardar un objeto en la base de datos, llame a save().
            #Si llama save()con commit=False, devolverá un objeto que aún no se ha guardado en la base de datos. En este caso, depende de usted llamar save()a la instancia del modelo resultante. Esto es útil si desea realizar un procesamiento personalizado en el objeto antes de guardarlo, o si desea utilizar una de las opciones especializadas para guardar modelos .
            data = form.save(commit=False)
            #CON LO DICHO ARRIBA, VEMOS QUE ANTES DE GUARDAR EL OBJETO EN LA BASE DE DATOS, RELLENAMOS ALGUNOS CAMPOS(EN ESTE CASO post y username), luego lo guardamos en la base de datos(guardamos el nuevo objeto(instancia de formulario) en la base de datos).
            post = get_object_or_404(Post, pk=self.object.pk)#obtenemos el post que estamos mirando.
            data.post_comment = post
            data.user_comment = request.user
            #AHORA GUARDAMOS EL OBJETO EN LA BBDD.
            data.save()
            resp = {
                'id': data.id,#id del comment almacenado en la bbdd.
                'comment_created':True
            }#ACA CREAMOS UN DICCIONARIO.
            response = json.dumps(resp)#creamos una respuesta codificada en json.
            #HttpResponse ( código fuente ) proporciona una solicitud HTTP entrante a una aplicación web Django con una respuesta de texto. Esta clase se usa con mayor frecuencia como un objeto de retorno desde una vista de Django.
            return HttpResponse(response, content_type = "application/json")#devolvemos una respuesta codificada en JSON
        

    def get_success_url(self):
        form = CommentForm(self.request.POST)
        if form.is_valid():
            resp = {
                'comment_created':True
            }#ACA CREAMOS UN DICCIONARIO.
            response = json.dumps(resp)#creamos una respuesta codificada en json.
            #HttpResponse ( código fuente ) proporciona una solicitud HTTP entrante a una aplicación web Django con una respuesta de texto. Esta clase se usa con mayor frecuencia como un objeto de retorno desde una vista de Django.
            return HttpResponse(response, content_type = "application/json")#devolvemos una respuesta codificada en JSON
        else:
            resp = {
                'comment_created':False
            }#ACA CREAMOS UN DICCIONARIO.
            response = json.dumps(resp)#creamos una respuesta codificada en json.
            #HttpResponse ( código fuente ) proporciona una solicitud HTTP entrante a una aplicación web Django con una respuesta de texto. Esta clase se usa con mayor frecuencia como un objeto de retorno desde una vista de Django.
            return HttpResponse(response, content_type = "application/json")#devolvemos una respuesta codificada en JSON
        

# #Tenemos que traer SingleObjectMixin para que podamos encontrar la publicacion que estamos mirando, y debemos recordar establecer template_name para asegurarnos de que los errores de formulario generarán la misma plantilla que PostDetailView está usando en GET :
# class PostFormView(LoginRequiredMixin, SingleObjectMixin, FormView):
#     template_name = 'publish/post_detail.html'
#     form_class = CommentForm
#     model = Post

#     #el metodo def post(self, request, *args, **kwargs): es como la linea if request.method == "POST": de una vista basada en funciones.
#     #Self se refiere a la clase en sí y se usa en los métodos GET y POST para pasar la plantilla y el formulario como contexto. request es el mismo objeto de solicitud HTTP que se usa normalmente en FBV que contiene metadatos en la ruta / usuario / método / etc. * Args y * kwargs representan cualquier argumento o argumento de palabra clave pasado como parámetros de URL
#     def post(self, request, *args, **kwargs):
#         if not request.user.is_authenticated:#entra aca si el usuario no esta autenticado.
#             return HttpResponseForbidden()
#         form = CommentForm(request.POST)
#         self.object = self.get_object()
#         if form.is_valid():
#             #Para guardar un objeto en la base de datos, llame a save().
#             #Si llama save()con commit=False, devolverá un objeto que aún no se ha guardado en la base de datos. En este caso, depende de usted llamar save()a la instancia del modelo resultante. Esto es útil si desea realizar un procesamiento personalizado en el objeto antes de guardarlo, o si desea utilizar una de las opciones especializadas para guardar modelos .
#             data = form.save(commit=False)
#             #CON LO DICHO ARRIBA, VEMOS QUE ANTES DE GUARDAR EL OBJETO EN LA BASE DE DATOS, RELLENAMOS ALGUNOS CAMPOS(EN ESTE CASO post y username), luego lo guardamos en la base de datos(guardamos el nuevo objeto(instancia de formulario) en la base de datos).
#             post = get_object_or_404(Post, pk=self.object.pk)#obtenemos el post que estamos mirando.
#             data.post_comment = post
#             data.user_comment = request.user
#             #AHORA GUARDAMOS EL OBJETO EN LA BBDD.
#             data.save()
#         return super().post(request, *args, **kwargs)

#     def get_success_url(self):
#         return reverse('post-detail', kwargs={'pk': self.object.pk})


class PostView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):#para el metodo get del formulario se usa la vista PostDetailView. 
        view = PostDetailView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):#para el metodo post del formulario se usa la vista PostFormView.
        view = PostFormView.as_view()
        return view(request, *args, **kwargs)


#--------------------------------------------------------------------------------#

#UpdateView:Una vista que muestra un formulario para editar un objeto existente, volver a mostrar el formulario con errores de validación (si los hay) y guardar los cambios en el objeto. Esto utiliza un formulario generado automáticamente a partir de la clase de modelo del objeto (a menos que se especifique manualmente una clase de formulario).
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):#vista para actualizar una publicacón.
    model = Post
    fields = ['body', 'pic']#estos dos campos nos apareceran en el formulario, user_post y time_post se agregaran automaticamente ya que sabemos que el usuario que crea una publicaicon es el logeado, el tiempo ya tiene un default.
    #template_name indica donde la vista buscara el formulario que se usa para la creacion del post.
    template_name = 'publish/update_post.html'#ESPECIFICAMOS NUESTRO propio nombre de templatename/location.

    #El formulario permitira cargar los campos pic, body y tags, pero falta agregar el usuario, el cual es el logeado.
    #esto es lo que se hace con el metodo form_valid
    def form_valid(self, form):
        form.instance.user_post = self.request.user#agregamos el nombre del usuario dueño
        return super().form_valid(form)


    #Limitar el acceso a los usuarios registrados que pasan una prueba ¶
    #Para limitar el acceso según ciertos permisos o alguna otra prueba, haría esencialmente lo mismo que se describe en la sección anterior
    #user_passes_test()toma un argumento requerido: un invocable que toma un Userobjeto y regresa Truesi el usuario tiene permiso para ver la página. Tenga en cuenta que user_passes_test()no comprueba automáticamente que Userno sea anónimo.
    #user_passes_test() es un decorador que se usa para vistas basadas en funciones, para vistas basadas en clsaes se usa el mixin UserPassesTestMixin.
    #test_func() :Debe anular el test_func()método de la clase para proporcionar la prueba que se realiza. Además, puede configurar cualquiera de los parámetros de AccessMixinpara personalizar el manejo de usuarios no autorizados:
    def test_func(self):
        #self.get_object(): Buscamos la publicacion que nos interesa.
        post = self.get_object()
        if self.request.user == post.user_post:#si el usurio logeado es el usuario que hizo la publicacion entra a este if.
            return True
        return False

    def get_context_data(self, **kwargs):#Lo usaremos para pasar el perfil del usuario del que miramos la sección Featured photo 
        ##Primero llamamos a la implementación base para obtener un contexto, o sea Primero obtenemos el contexto existente desde nuestra superclase, esto es lo que se hace con la siguiente linea.
        context = super(PostUpdateView , self).get_context_data(**kwargs)

        post = self.get_object()

        context['post'] = post

        return context#Devolvemos el nuevo contexto (actualizado)





#DeleteView:Una vista que muestra una página de confirmación y elimina un objeto existente. El objeto dado solo se eliminará si el método de solicitud es POST. Si esta vista se obtiene a través de GET, mostrará una página de confirmación que debe contener un formulario que se envía a la misma URL.
#UserPassesTestMixin: le permite definir una función de prueba(en este caso, test_func) que debe devolver True si el usuario actual puede acceder a la vista.

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):#vista para eliminar una publicación.
    model = Post
    template_name = 'publish/detele_post.html'#ESPECIFICAMOS NUESTRO propio nombre de templatename/location.
    


    #Limitar el acceso a los usuarios registrados que pasan una prueba ¶
    #Para limitar el acceso según ciertos permisos o alguna otra prueba, haría esencialmente lo mismo que se describe en la sección anterior
    #user_passes_test()toma un argumento requerido: un invocable que toma un Userobjeto y regresa Truesi el usuario tiene permiso para ver la página. Tenga en cuenta que user_passes_test()no comprueba automáticamente que Userno sea anónimo.
    #user_passes_test() es un decorador que se usa para vistas basadas en funciones, para vistas basadas en clsaes se usa el mixin UserPassesTestMixin.
    #test_func() :Debe anular el test_func()método de la clase para proporcionar la prueba que se realiza. Además, puede configurar cualquiera de los parámetros de AccessMixinpara personalizar el manejo de usuarios no autorizados:
    def test_func(self):
        #self.get_object(): Buscamos la publicacion que nos interesa.
        post = self.get_object()
        if self.request.user == post.user_post:#si el usurio logeado es el usuario que hizo la publicacion entra a este if.
            return True
        return False
    
    def get_context_data(self, **kwargs):#Lo usaremos para pasar el perfil del usuario del que miramos la sección Featured photo 
        ##Primero llamamos a la implementación base para obtener un contexto, o sea Primero obtenemos el contexto existente desde nuestra superclase, esto es lo que se hace con la siguiente linea.
        context = super(PostDeleteView, self).get_context_data(**kwargs)
        
        
        post = self.get_object()

        context['post'] = post

        return context#Devolvemos el nuevo contexto (actualizado)


    success_url = reverse_lazy('home')#SI COMENTAMOS ESTA LINEA SE REDIRIGIRA AL get_absolute_url DEL MODELO Post segun caracteristicas de una CreateView.



def like(request):#recibimos el pk del post, ya que el usuario que de me gusta estara logeado.
    post_id = request.GET.get("id_post_like", "")
    post = get_object_or_404(Post, id=post_id)
    new_like, created = Like.objects.get_or_create(user_like=request.user, post_like=post)
    if not created:#si no fue creado significa que ya existe y se dio en dislike o hubo un error, por ende borramos el like.
        new_like.delete()#borramos el objeto que obtenemos.
    resp = {
        'created':created
    }#ACA CREAMOS UN DICCIONARIO.
    response = json.dumps(resp)#creamos una respuesta codificada en json.
    #HttpResponse ( código fuente ) proporciona una solicitud HTTP entrante a una aplicación web Django con una respuesta de texto. Esta clase se usa con mayor frecuencia como un objeto de retorno desde una vista de Django.
    return HttpResponse(response, content_type = "application/json")#devolvemos una respuesta codificada en JSON







#¿Cuándo usar CreateView?
#CreateView debe usarse cuando necesite un formulario en la página y necesite hacer una inserción de base de datos al enviar un formulario válido.
#En vistas basada en clase no se puede usar el decorador @login_required, por eso se usa LoginRequiredMixin.
#CreateView:Una vista que muestra un formulario para crear un objeto, volver a mostrar el formulario con errores de validación (si los hay) y guardar el objeto.
class FeaturedPostCreateView(LoginRequiredMixin, CreateView):#vista para crear una Featured photos.
    model = Post
    fields = ['body', 'pic']#estos dos campos nos apareceran en el formulario, user_post, time_post y tags se agregaran automaticamente ya que sabemos que el usuario que crea una publicaicon es el logeado, el tiempo ya tiene un default y tags sera Featured.
    #template_name indica donde la vista buscara el formulario que se usa para la creacion del post.
    template_name = 'publish/create_featuredpost.html'#ESPECIFICAMOS NUESTRO propio nombre de templatename/location.

    #El formulario permitira cargar los campos pic, body y tags, pero falta agregar el usuario, el cual es el logeado.
    #esto es lo que se hace con el metodo form_valid
    def form_valid(self, form):
        form.instance.user_post = self.request.user#agregamos el nombre del usuario dueño
        form.instance.tags = 'Featured'
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):#Lo usaremos para pasar el perfil del usuario del que miramos la sección Featured photo 
        ##Primero llamamos a la implementación base para obtener un contexto, o sea Primero obtenemos el contexto existente desde nuestra superclase, esto es lo que se hace con la siguiente linea.
        context = super(FeaturedPostCreateView, self).get_context_data(**kwargs)

     

        #URL DESDE LA QUE LLEGUE:
        referer = self.request.META.get('HTTP_REFERER')

        #POSIBLES LUGARES DESDE DONDE SE PUEDE LLEGAR A ESTA VISTA:
        #URL de mi perfil:
        url_upload_photo = reverse('upload_photo')
        #URL de home:
        url_FeaturedPostListView = reverse('FeaturedPostListView', kwargs={'pk': self.request.user.id})
        
        if referer:#primero nos fijamos de donde venimos, y si existe una url
            if url_upload_photo in referer:#nos fijamos si venimos de url_upload_photo 
                context['referer'] = url_upload_photo
            else:#si no venimos de  url_upload_photo
                if url_FeaturedPostListView in referer:#si venimos de url_FeaturedPostListView
                    context['referer'] = url_FeaturedPostListView
                else:#sino venimos de ninguna de las dos anteriores:
                    context['referer'] = reverse('home')
        else:#url fuera de traveltry, o estando en traveltry escribir la url a mano
            context['referer'] = reverse('home')


        return context

    #Ni siquiera es necesario que proporciones un success_url para CreateView o UpdateView, se usarán get_absolute_url()en el objeto de modelo si está disponible.
    #success_url: La URL a la que se redireccionará cuando el formulario se procese correctamente.
    #pero aca como luego de crear el post queremos redireccionar home si pones el success_url.
    #success_url = reverse_lazy('home')#SI COMENTAMOS ESTA LINEA SE REDIRIGIRA AL get_absolute_url DEL MODELO Post segun caracteristicas de una CreateView.
    #get_success_url solo debe devolver la URL a la que redireccionar, no la respuesta de redireccionamiento.
    def get_success_url(self, **kwargs):
        id_user = self.request.user.id
        return '{}'.format(reverse('FeaturedPostListView', kwargs={'pk': id_user}))








class FeaturedPostListView(LoginRequiredMixin, ListView):#esta vista maneja la visualización de todas las publicaciones en un orden que coloca las publicaciones más nuevas en primer lugar. Cada página muestra 10 publicaciones y luego debemos pasar a la página siguiente para ver más. Además, si el usuario no está autenticado, no le damos la opción de dar me gusta en la publicación. Si el usuario está autenticado, mostramos si al usuario le ha gustado o no.
    #ES IMPORTANTE SABER QUE ESTA VISTA TIENE QUE RECIBIR DOS DATOS, EL ID DEL PAIS Y EL NOMBRE DE USUARIO, CON EL FIN DE PODER FILTRAR LAS IMAGENES CORREPONDIENTES.
    
    model = Post
    #SI solo definimos esto, lo siguiente es lo que ocurre:
    #La vista genérica consultará a la base de datos para obtener todos los registros del modelo especificado (Post) y renderizará una plantilla ubicada en /librodedeportes/publish/templates/publish/post_list.html. Dentro de la plantilla puedes acceder a la lista de post mediante la variable de plantilla llamada object_list O post_list (esto es, genéricamente, "nombre_del_modelo_list").
    #Esta ruta complicada para la ubicación de la plantilla no es un error de digitación -- las vistas genéricas buscan plantillas en /application_name/the_model_name_list.html (publish/post_list.html en este caso) dentro del directorio de la aplicación /application_name/templates/ (/publish/templates/).
    ######################
    #Se Pueden añadir atributos para cambiar el comportamiento por defecto explicado arriba, y es lo que hacemos abajo.
    template_name = 'publish/FeaturedPost_List.html'#ESPECIFICAMOS NUESTRO propio nombre de templatename/location.
    context_object_name = 'images'#ACA CAMBIAMOS LA VARIABLE DE PLANTILLA(QUE ORIGINALMENTE ERA post_list) QUE SE USA PARA ACCEDER A LA LISTA DE LAS PUBLICACIONES.
    #ordering = ['-date_posted']#ORDENAREMOS LA LISTA DE PUBLICACIONES OBTENIDA POR FECHA DE PUBLICACIÓN, LAS ULTIMAS EN PUBLICARSE SERAN LAS PRIMERAS EN MOSTRARSE.
    #paginate_by:agrega un paginator y page_obj al context. Para permitir que sus usuarios naveguen entre páginas.
    paginate_by = 10#MOSTRAREMOS DE A 10 PUBLICACIONES.

    def get_queryset(self):#Obtenga la lista de elementos para esta vista. Debe ser iterable y puede ser un conjunto de consultas (en el que se habilitará el comportamiento específico del conjunto de consultas).
        #OBTENEMOS LOS OBJETOS QUE SOLO NOS INTERESAN.
        featured_pk=self.kwargs['pk']#OBTENEMOS EL PARAMETRO QUE PASAMOS POR URL  CON NOMBRE pk, este valor pertenece al id del usuario al que miramos sus Featured photos.
        #para buscar los post adecuados, lo hacemos por medio del campo tags del metodo post, pero este tags en un char, por lo tanto vmaos a  encontrar el nombre del pais al cual corresponde el id recibido:
        featured_user = get_object_or_404(Profile, user=featured_pk)#obtenemos el objeto o un error 404.

        Post_Featured=Post.objects.filter(user_post=featured_user.user_id, tags='Featured')#RETORNAMOS LO QUE NOSOTROS QUEREMOS, IMAGENES CORRESPONDIENTES A PAIS Y USUARIO.
        #LLAMAR AL METODO get_queryset anula a ordering, POR LO TANTO DEBEMOS ORDENARLO NOSOTROS, HAY OTRA FORMA, USANDO LA CLASE super CUANDO SE LLAMA AL METODO get_queryset NO SE ANULA EL METODO ordering.
        Post_Featured = Post_Featured.order_by('-time_post')
        return Post_Featured


    def get_context_data(self, **kwargs):#Lo usaremos para pasar el perfil del usuario del que miramos la sección Featured photo 
        ##Primero llamamos a la implementación base para obtener un contexto, o sea Primero obtenemos el contexto existente desde nuestra superclase, esto es lo que se hace con la siguiente linea.
        context = super(FeaturedPostListView, self).get_context_data(**kwargs)

        user_pk=self.kwargs['pk']#OBTENEMOS EL PARAMETRO QUE PASAMOS POR URL  CON NOMBRE pk, este valor pertenece al id del pais donde estemos mirando las imagenes.
        data_user=get_object_or_404(User, id=user_pk)
        context['data_user'] = data_user# El fragmento muestra cómo añadir una variable llamada "id_user" al contexto (la misma estaría entonces disponible como una variable de plantilla).
        
        #publicaciones a las que se le dio like:
        liked = [i for i in Post.objects.all() if Like.objects.filter(user_like = self.request.user, post_like=i)]#se recorren y se filtran los post en los cuales el usuario logeado dio me gusta.
        #EN LA SIGUIENTE LINEA añadimos al contexto la información extra que queremos.
        context['liked_post'] = liked# El fragmento muestra cómo añadir una variable llamada "liked_post" al contexto (la misma estaría entonces disponible como una variable de plantilla).
        
        #URL DESDE LA QUE LLEGUE:
        referer = self.request.META.get('HTTP_REFERER')

        #POSIBLES LUGARES DESDE DONDE SE PUEDE LLEGAR A ESTA VISTA:
        #URL de mi perfil:
        url_myprofile = reverse('myprofile')
        #URL de home:
        url_profile = reverse('user_profile', kwargs={'username': data_user.username})
        url_home = reverse('home')

        if referer:#primero nos fijamos de donde venimos, y si existe una url
            if url_myprofile in referer:#nos fijamos si venimos de url_upload_photo 
                context['referer'] = url_myprofile
            else:#si no venimos de  url_upload_photo
                if url_profile in referer:#si venimos de url_FeaturedPostListView
                    context['referer'] = url_profile
                else:#sino venimos de ninguna de las dos anteriores:
                    if url_home in referer:
                       context['referer'] = url_home 
                    else:
                        if self.request.user == data_user:
                            context['referer'] = url_myprofile
                        else:
                            context['referer'] = url_profile
                            
        else:#url fuera de traveltry, o estando en traveltry escribir la url a mano
            context['referer'] = reverse('home')


        return context#Devolvemos el nuevo contexto (actualizado




#ListView:Una página que representa una lista de objetos.
class LikesListView(LoginRequiredMixin, ListView):
    model = Like
    context_object_name = 'List'#nombre para manejar la lista como variable de plantilla, si no agregamos el nuestro propio la vista basada en ListView tiene su propio nombre.
    template_name = 'publish/likes_list.html'#ESPECIFICAMOS NUESTRO propio nombre de templatename/location.
    paginate_by = 20#Cuantos objetos mostraremos por pagina.


    def get_queryset(self):#Obtenga la lista de elementos para esta vista. Debe ser iterable y puede ser un conjunto de consultas (en el que se habilitará el comportamiento específico del conjunto de consultas).
        
        pk = self.kwargs['pk']#OBTENEMOS EL PARAMETRO QUE PASAMOS POR URL  CON NOMBRE pk, este valor pertenece al id del usuario al que miramos sus Featured photos.

        List=Like.objects.filter(post_like=pk).only('user_like')#obtenemos todos los objetos likes que pertenescan a la publicación
    

        return List


    #ACA SobreescribiMoS métodos en vistas basadas en clases:
    #EN ESTE CASO SOBREESCRIBIMOS EL METODO get_context_data(), que tiene por objeto pasar variables de contexto adicionales a la plantilla.
    def get_context_data(self, **kwargs):
        ##Primero llamamos a la implementación base para obtener un contexto, o sea Primero obtenemos el contexto existente desde nuestra superclase, esto es lo que se hace con la siguiente linea.
        context = super(LikesListView, self).get_context_data(**kwargs)
        
        #Nos fijamos si tenemos nuevos solicitudes de seguimiento, para luego indicarle al usuario de esto:
        received_follower_request=FollowersRequest.objects.filter(to_user=self.request.user).count()#buscamos las solicitudes recibidas.
        context['received_follower_request'] = received_follower_request


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




        #URL DESDE LA QUE LLEGUE:
        referer = self.request.META.get('HTTP_REFERER')

        #obtendremos el usuario a traves de la publicacion:
        post_pk=self.kwargs['pk']
        post=Post.objects.filter(id=post_pk).first()


        url_home = reverse('home')
        url_FeaturedPostListView = reverse('FeaturedPostListView', kwargs={'pk': post.user_post.id})
        

        if referer:

            if url_FeaturedPostListView in referer:
                context['referer'] = url_FeaturedPostListView

            elif url_home in referer:
                context['referer'] = url_home

            else:#esta opcion seria para cuando se llegue desde Galleryview.
                context['referer'] = referer
        else:
            context['referer'] = reverse('home')



        #mandamos url para enviar y cancel solicitudes:
        url_send = reverse('send_or_delete_follower_request')
        context['url_send'] = url_send




        return context#Devolvemos el nuevo contexto (actualizado)







#esta vista es para compartir publicaciónes:
@login_required
def Share_Post(request):
    #ACA TRATAREMOS EL FORMULARIO
    if request.method == 'POST':

        #TAMBIEN VAMOS A PASAR LA CANTIDAD DE MENSAJES QUE TENEMOS SIN LEER.
        messages_unreaded=Chat_Message.objects.filter(receiver=request.user).exclude(unread=1)#Excluimos los mensaje leidos

        Post_to_share = request.POST.get('sharing_post')#Lo que está haciendo esta linea es decir, "Obtenga el valor de una variable POST con el nombre 'sharing_post', que pertenece al input que enviamos, con el atributo name='sharing_post', este input es parte del formulario.
        
        #ahora que tenemos el id del post, vamos a crear una isntancia sharing post:
        #pero primero obtenemos el post
        Post_to_share_2 = Post.objects.filter(id=Post_to_share).first()
        #ahora creamos el sharing post:
        Sharing_Post.objects.create(the_post=Post_to_share_2, the_user=request.user)
        return redirect('home')






#DELETE SHARING_POST:



#DeleteView:Una vista que muestra una página de confirmación y elimina un objeto existente. El objeto dado solo se eliminará si el método de solicitud es POST. Si esta vista se obtiene a través de GET, mostrará una página de confirmación que debe contener un formulario que se envía a la misma URL.
#UserPassesTestMixin: le permite definir una función de prueba(en este caso, test_func) que debe devolver True si el usuario actual puede acceder a la vista.

class SharingPostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):#vista para eliminar una sharing publicación.
    model = Sharing_Post
    template_name = 'publish/unshared_post.html'#ESPECIFICAMOS NUESTRO propio nombre de templatename/location.
    


    #Limitar el acceso a los usuarios registrados que pasan una prueba ¶
    #Para limitar el acceso según ciertos permisos o alguna otra prueba, haría esencialmente lo mismo que se describe en la sección anterior
    #user_passes_test()toma un argumento requerido: un invocable que toma un Userobjeto y regresa Truesi el usuario tiene permiso para ver la página. Tenga en cuenta que user_passes_test()no comprueba automáticamente que Userno sea anónimo.
    #user_passes_test() es un decorador que se usa para vistas basadas en funciones, para vistas basadas en clsaes se usa el mixin UserPassesTestMixin.
    #test_func() :Debe anular el test_func()método de la clase para proporcionar la prueba que se realiza. Además, puede configurar cualquiera de los parámetros de AccessMixinpara personalizar el manejo de usuarios no autorizados:
    def test_func(self):
        #self.get_object(): Buscamos la publicacion que nos interesa.
        sharing_post = self.get_object()
        if self.request.user == sharing_post.the_user:#si el usurio logeado es el usuario que hizo la publicacion entra a este if.
            return True
        return False
    

    def get_context_data(self, **kwargs):#Lo usaremos para pasar el perfil del usuario del que miramos la sección Featured photo 
        ##Primero llamamos a la implementación base para obtener un contexto, o sea Primero obtenemos el contexto existente desde nuestra superclase, esto es lo que se hace con la siguiente linea.
        context = super(SharingPostDeleteView, self).get_context_data(**kwargs)
       
        return context#Devolvemos el nuevo contexto (actualizado)

    
    success_url = reverse_lazy('home')#SI COMENTAMOS ESTA LINEA SE REDIRIGIRA AL get_absolute_url DEL MODELO Post segun caracteristicas de una CreateView.








@login_required
def delete_comment(request):

    #obtenemos el id enviado por ajax:
    id_comment = request.GET.get("id_comment", "")
    #obtenemos el comentario:
    Comment_to_delete = Comments.objects.filter(id = id_comment)
    #eliminamo el comentario:
    if Comment_to_delete:
        Comment_to_delete.delete()
        deleted = True
    else:
        deleted = False

    resp = {
        'deleted':deleted
    }#ACA CREAMOS UN DICCIONARIO.
    response = json.dumps(resp)#creamos una respuesta codificada en json.
    #HttpResponse ( código fuente ) proporciona una solicitud HTTP entrante a una aplicación web Django con una respuesta de texto. Esta clase se usa con mayor frecuencia como un objeto de retorno desde una vista de Django.
    return HttpResponse(response, content_type = "application/json")#devolvemos una respuesta codificada en JSON






@login_required
def Report_Post(request, id):#Vista para reportar Post
    post = get_object_or_404(Post, id=id)
    user = request.user
    if request.method == 'POST':
        form = ReportPostForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.post_reported = post
            data.who_reported = user
            data.save()
            return redirect('home')
    else:

        form = ReportPostForm()


        #URL DESDE LA QUE LLEGUE:
        referer = request.META.get('HTTP_REFERER')

        #obtendremos el usuario a traves de la publicacion:
        post=Post.objects.filter(id=id).first()


        url_home = reverse('home')
        url_FeaturedPostListView = reverse('FeaturedPostListView', kwargs={'pk': post.user_post.id})
        

        if referer:

            if url_FeaturedPostListView in referer:
                referer = url_FeaturedPostListView

            elif url_home in referer:
                referer = url_home

            else:#esta opcion seria para cuando se llegue desde Galleryview.
                referer = referer
        else:
            referer = reverse('home')

    return render(request, 'publish/report_post.html', {'form':form, 'referer': referer})





@login_required
def upload_photo(request):#aca solo accede el usuario logeado, o sea, el usuario puede agregar fotos solo a su cuenta.

    #URL DESDE LA QUE LLEGUE:
    referer = request.META.get('HTTP_REFERER')


    url_myprofile = reverse('myprofile')
    url_list_notification = reverse('list_notification')
    url_search_user_2 = reverse('search_user_2')
    

    if referer:

        if url_myprofile in referer:
            referer = url_myprofile

        elif url_list_notification in referer:
            referer = url_list_notification

        elif url_search_user_2 in referer:
            referer = url_search_user_2

        else:#esta opcion seria para cuando se llegue desde Galleryview, home, FeaturedCreateview
            referer = reverse('home')

    else:
        referer = reverse('home')


    #vamos a obtener los paises que el usuario tiene agregado:
    added_countries = WorldCountriesUser.objects.filter(username=request.user)

    #Ahora que tenemos los nombres de los paises, buscamos los id:
    #lista donde guardaremos los objetos que contiene id y nombre del pais:
    country_list = []
    for i in added_countries :
        c_f = WorldCountries.objects.get(countries_tot = i.countries_user)
        country_list.append(c_f)

    return render(request, 'publish/upload_photo.html', {'referer':referer, 'country_list':country_list})
