from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings
from django.utils import timezone

from django.db.models.signals import post_delete, pre_save
import os#como vamos a haceder al sistema de archivos importamos 'os'.
from django.dispatch import receiver

# Create your models here.

class Post(models.Model):#Este modelo sera el que contre los campos de una publicacion
    user_post = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)#quien hace la publicacion.
    time_post = models.DateTimeField(default=timezone.now)#Almacena la hora en que se hizo la publicacion.
    tags = models.CharField(max_length=100, blank=True)#tags puede estar en blanco, pero en el caso de las publicaciones en los paises, esta etiqueta tendra el nombre del pais, esto es con el fin de luego poder buscarlas con facilidad.
    body = models.CharField(max_length=255, blank=True)
    pic = models.ImageField(upload_to='publish')
    

    # def delete(self, *args, **kwargs):#este metodo se ejecuta a la hora de eliminar un post, cuando se acceda a la vista que elimina los post y si luego se da que si, entrara aca y se eliminara el archivo correspondiente.
    #     #el metodo delete se usa en la DeleteView que usamos para borrar el post.
    #     #cuando se ejecute esa vista se stara ejecutando ese metodo, por ende, se ejecutara este de igual manera.
    #     if os.path.isfile(self.pic.path):#si existe este archivo entra al if
    #         os.remove(self.pic.path)#pasamos el path del archivo y lo elimina.
    #     super(Post, self).delete(*args, **kwargs)#pasamos el Post, la instancia(self), y luego eliminamos.

    
    #El str que decide cómo Django mostrará nuestro modelo en el panel de administracion
    def __str__(self):#ESTO ES PARA QUE DJANGO NOS MUESTRE, EN ESTE CASO, EL MODELO SE MUESTRE CON LA DESCRIPCION QUE SE AGREGE.
        return self.body


    #get_absolute_url() método para decirle a Django cómo calcular la URL canónica de un objeto.
    # Una URL canónica es la URL "oficial" de una determinada página.
    #LA VENTAJA ES TENER UN CODIGO MAS LIMPIO SI LO SUCEDE EL CASO EN EL QUE LAS URL SE CAMBIAN, ACA SE GENERAN AUTOMATICAMENTE.
    def get_absolute_url(self):
        #reverse: ejemplo :reverse('url_name'), Esto busca en todas las URL definidas en su proyecto la URL definida con el nombre url_name y devuelve la URL real(o sea el primer argumento de la funcion path).
        #Esto significa que se refiere a la URL solo por su nameatributo; si desea cambiar la URL en sí o la vista a la que se refiere, puede hacerlo editando un solo lugar urls.py.
        #reverse( viewname , urlconf = None , args = None , kwargs = None , current_app = None ).
        #viewname puede ser un nombre de patrón de URL o el objeto de vista invocable.
        #argsy kwargs no se puede pasar al reverse() mismo tiempo
        #kwargs es una cantidad de argumentos con valor, en este caso hay uno solo, luego se transforma a diccionario.
        

        #Cuando se invoca el método get_absolute_url, devuelve un enlace inverso a la URL en post-detail'(EN ESTE CASO),y esto pasará argumentos adicionales a la URL, en este caso pk, Esto se habrá configurado en urls.py, de tal manera que por medio de url se pueda mandar un dato.
        #EL pk ES PARA IDENTIFICAR A CADA PUBLICACION, ya que puede haber docenas o cientos de páginas de este tipo(O SEA MUCHAS PUBLICACIONES), CADA UNA ESTA IDENTIFICADA POR EL PK.
        #SI NO ME EQUIVOCO EL pk es el id DE CADA PUBLICACIÓN.
        return reverse('post-detail', kwargs={'pk': self.pk})


#post_delete es una señal, que se envia luego que ocurre una eliminacion.
#señales : Django incluye un "despachador de señales" que ayuda a las aplicaciones desacopladas a recibir notificaciones cuando ocurren acciones en otra parte del marco. En pocas palabras, las señales permiten que ciertos remitentes notifiquen a un conjunto de receptores que se ha llevado a cabo alguna acción. Son especialmente útiles cuando muchas piezas de código pueden estar interesadas en los mismos eventos.
#Para recibir señales se puede usar el decorador receiver( señal ):
#Parámetros: señal : una señal o una lista de señales a las que conectar una función.
#Conexión a señales enviadas por remitentes específicos, como se da en este caso, el remitente es el modleo User, que se guarda cuando se crea un usuario.
#sintaxis: @receiver(señal, sender=MyModel)..
# Los parámetros significan lo siguiente:
# sender: La clase de modelo con la que se llamó a la señal.
# instance: La instancia de a Post, ya sea que se haya eliminado.
# Cuando se llama a la señal, ninguno de los parámetros estará vacío.
@receiver(post_delete, sender=Post)#cada vez que se recibe una señal post_delete del modelo  Post entrara aca.
#funciona tanto para eliminar una publicacion en particular y cuando se elimina un usuario se eliminan todas las fotos, no hay problemas al actualizar un post.
def delete_postfile(sender, instance, **kwargs):
    #Se elimina el archivo del sistema de archivos cuando un objeto Post se elimina..
    if instance.pic:
        instance.pic.delete(save=False)#USAR EN PRODUCCION
        #if os.path.isfile(instance.pic.path):#usar en desarrollo
            #os.remove(instance.pic.path)#USAR EN DESARROLLO







class Comments(models.Model):#ESTE MODELO CORRESPONDE A LOS COMENTARIOS QUE LOS USUARIOS HAGAN EN LAS PUBLICACIONES.
    #post: es una relacion uno a muchos(ForeignKey), ya que una publicacion puede tener muchos comentarios, pero un comentario solo puede pertenecer a una publicacion.
    #ForeignKey es una relación uno a muchos, estos campos requieren que el primer argumento sea la clase del modelo al que se relacionan.
    #El uso de on_delete = models.CASCADE se usa para que cuando se elimine el usuario tambien se elimine la publicacion.
    #eliminar la publicación también eliminará los comentarios(on_delete=models.CASCADE).
    #related_name: Es el nombre que se utilizará para la relación del objeto relacionado con este.
    #related_name en ForeignKeyFields. Esto le permitirá hacer referencia a la misma tabla, pero dará Django nombres especiales para la relación(LOS QUE NOSOTROS SELECCIONEMOS EN related_name).
    post_comment = models.ForeignKey(Post, related_name='details', on_delete=models.CASCADE)
    #username: Relaciona un comentario con el usuario. Cuando se elimina el usuario, el comentario también se eliminará.
    user_comment = models.ForeignKey(User, related_name='details', on_delete=models.CASCADE)
    #comment: contendrá el comentario relevante que el usuario haga en la publicación.
    comment = models.CharField(max_length=255)
    #comment_date: establecerá la marca de tiempo para cada comentario. Usaremos la hora predeterminada como hora actual.
    time_comment = models.DateTimeField(default=timezone.now)

    #Model Meta se utiliza básicamente para cambiar el comportamiento de los campos de su modelo, como cambiar las opciones de orden, verbose_name y muchas otras opciones. Es completamente opcional agregar la clase Meta en su modelo.
    class Meta:
        ordering = ('-time_comment',)

    #El str que decide cómo Django mostrará nuestro modelo en el panel de administracion
    def __str__(self):
        return '{}, Comment by {}'.format(self.comment, self.user_comment)


class Like(models.Model):#este modelo corresponde a los likes que los usuarios hagan.
    #user: representa al usuario al que le ha gustado la publicación. Eliminar el usuario elimina el me gusta.
    user_like = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='likes', on_delete=models.CASCADE)
    #post:Es el post en el que se da el me gusta. Al eliminar la publicación, también se eliminan todos sus Me gusta.
    post_like = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)




class Sharing_Post(models.Model):#Modelo para compartir Posts
    #CAMPO QUE GUARDE QUE POST FUE COMPARTIDO.:
    the_post =  models.ForeignKey(Post, related_name='SharingPost', on_delete=models.CASCADE)
    #CAMPO QUE GUARDE QUE USUARIO LO COMPARTIO:
    the_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='SharingPost', on_delete=models.CASCADE)
    
    #Al campo de la fecha le ponemos el mismo nombre que en el modelo Post, ya que lo usaremos para compararlos y listarlos segun la fecha mas proxima
    time_post = models.DateTimeField(default=timezone.now)#Almacena la hora en que se hizo la sharing.






class report_post(models.Model):#modelo para almacenar post reportados
    #CAMPO QUE GUARDE QUE POST FUE COMPARTIDO.:
    post_reported =  models.ForeignKey(Post, related_name='ReportPost', on_delete=models.CASCADE)
    #CAMPO QUE GUARDE QUE USUARIO LO COMPARTIO:
    who_reported = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='Whoreport', on_delete=models.CASCADE)
    #Porque se reporta el post:
    Why_reported = models.CharField(max_length=255)
    #A QUE HORA FUE REPORTADO:
    time_reported = models.DateTimeField(default=timezone.now)#Almacena la hora en que se hizo el report.

    #El str que decide cómo Django mostrará nuestro modelo en el panel de administracion
    def __str__(self):#ESTO ES PARA QUE DJANGO NOS MUESTRE, EN ESTE CASO, EL MODELO SE MUESTRE CON LA DESCRIPCION QUE SE AGREGE.
        return self.post_reported.body






@receiver(pre_save, sender=Post)#cada vez que se recibe una señal pre_save del modelo  Post entrara aca.
#esta funcion-metodo se utiliza para eliminar las imagenes de publicacion anteriores cuando se actualizan por una nueva
def delete_postfile(sender, instance, **kwargs):
  
    if instance.pk:

        old_post = Post.objects.get(pk=instance.pk).pic
        # print("se viene la url 2:")
        # print(old_post.url)
        # print(old_post.path)

        

        old_post.delete(save=False)#USAR EN PRODUCCION
        # if os.path.isfile(old_post.path):#usar en desarrollo
        #   os.remove(old_post.path)#usar en desarrollo
            # print('supuestamente se elimino:')
            # print(old_post.path)
