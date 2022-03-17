from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import TextField
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings


#
import os#como vamos a haceder al sistema de archivos importamos 'os'.
from django.dispatch import receiver
# Create your models here.


def delete_old_image(instance, filename): #ESTA FUNCION ES PARA BORRAR LA IMAGEN ANTERIOR DEL USUARIO, O SEA CUANDO SUBE NUEVA IMAGEN SE BORRA LA ANTERIOR, Y ASI RATONEAR MEMORIA,creo que debe ir antes del modelo Profile que es quien le pasa la instancia(creo).
    old_instance=Profile.objects.get(pk=instance.pk)
    if old_instance.photo != 'profiles/defaultuser.png':#este if es para que no se elimine la defaultuser.png que es la foto default cuando un usuario inicia sesion.
        old_instance.photo.delete()
    return 'profiles/' + filename #Devolvemos la ruta nueva, se devuelve a upload_to que es quien llama a esta función.


class Profile(models.Model):#modelo que tiene una relacion uno a uno con el modelo User, usaremos ese modelo para extender el modelo de usuario.
    # el campo OneToOneField quiere decir que un usuario tendra un perfil, y un perfil tendra solo un usuario. 
    user = models.OneToOneField(User, on_delete=models.CASCADE)#ESTE SERA UN ID, EN PARTICULAR EL ID QUE TENGA EL USUARIO.
    bio = models.TextField(max_length=500, blank=True, null=True)#pequenia bibliografia para que el usuario ponga lo que guste.
    #AutoSlugField no acepta campos que no sean ascci.
    #slug = AutoSlugField(populate_from='user')#este será el campo de slug. Usamos AutoSlugField y lo configuraremos para hacer slug desde el campo de usuario.
    slug = models.TextField(max_length=100)
    photo = models.ImageField(upload_to=delete_old_image, default='profiles/defaultuser.png')#upload_to indica a donde se enviara la imagen, en este caso la queremos enviar a la carpeta profile dentro de la carpeta media que tiene que estar en el directorio raiz del proyecto.
    #campo para que el usuario pueda indicar si quiere un perfil privado o publico.
    private=models.BooleanField(default=False)
    #Un followers tiene(podra seguir a) varios profile(usuarios) y un profile(usuario) tiene varios followers.
    #El 'self'argumento to ManyToManyFielddeclara una relación recursiva y symmetrical=Falseestablece que la relación inversa es diferente, lo que significa que si te sigo, no me sigues a mí.
    followers = models.ManyToManyField('self', symmetrical=False, related_name='related_name_followers', blank=True)#Cada usuario podra tener varios seguidores y seguir a varios usuarios.

    def count_followers(self):
        return self.followers.count()
    
    def count_following(self):
        return Profile.objects.filter(followers=self).count()

    #post_save es una señal, que se envia luego que ocurre un guardado.
    #señales : Django incluye un "despachador de señales" que ayuda a las aplicaciones desacopladas a recibir notificaciones cuando ocurren acciones en otra parte del marco. En pocas palabras, las señales permiten que ciertos remitentes notifiquen a un conjunto de receptores que se ha llevado a cabo alguna acción. Son especialmente útiles cuando muchas piezas de código pueden estar interesadas en los mismos eventos.
    #Para recibir señales se puede usar el decorador receiver( señal ):
    #Parámetros:señal : una señal o una lista de señales a las que conectar una función.
    #Conexión a señales enviadas por remitentes específicos, como se da en este caso, el remitente es el modleo User, que se guarda cuando se crea un usuario.
    #sintaxis: @receiver(señal, sender=MyModel)..
    @receiver(post_save, sender=User)
    # Los parámetros significan lo siguiente:
    # sender: La clase de modelo con la que se llamó a la señal.
    # instance: La instancia de a User, ya sea que se haya creado o actualizado.
    # created: Un valor booleano para determinar si Userse actualizó o creó.
    # Cuando se llama a la señal, ninguno de los parámetros estará vacío.
    def create_user_profile(sender, instance, created, **kwargs):
        if created:#si se actualiza no hace falta crear
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):#si se actualiza el metodo de arriba no se usa, o sea no entra al if, directamente se viene a este metodo y se guarda la instancia.
        instance.profile.slug=instance.username#guardamos en el campo slug el nombre de usuario que agrego la persona que se acaba de registrar
        instance.profile.save()


    #get_absolute_url() método para decirle a Django cómo calcular la URL canónica de un objeto.
    # Una URL canónica es la URL "oficial" de una determinada página.
    #LA VENTAJA ES TENER UN CODIGO MAS LIMPIO SI LO SUCEDE EL CASO EN EL QUE LAS URL SE CAMBIAN, ACA SE GENERAN AUTOMATICAMENTE.
    def get_absolute_url(self):
        return "/users/profile/{}/".format(self.user.username)#PARA PRODUCCION.
        #return "/users/profile/{}".format(self.user.username)#PARA DESARROLLO.

    #El str que decide cómo Django mostrará nuestro modelo en el panel de 
    #administración. Lo hemos configurado para mostrar el nombre de usuario como el objeto Consulta.
    def __str__(self):#ESTE METODO NOS SERA UTIL PARA VER ESTE MODELO EN ADMIN CON EL NOMBRE QUE LE PASEMOS
        return str(self.user.username)



#post_delete es una señal, que se envia luego que ocurre una eliminacion.
#señales : Django incluye un "despachador de señales" que ayuda a las aplicaciones desacopladas a recibir notificaciones cuando ocurren acciones en otra parte del marco. En pocas palabras, las señales permiten que ciertos remitentes notifiquen a un conjunto de receptores que se ha llevado a cabo alguna acción. Son especialmente útiles cuando muchas piezas de código pueden estar interesadas en los mismos eventos.
#Para recibir señales se puede usar el decorador receiver( señal ):
#Parámetros: señal : una señal o una lista de señales a las que conectar una función.
#Conexión a señales enviadas por remitentes específicos, como se da en este caso, el remitente es el modleo Profile, que se guarda cuando se elimina cuando se elimina un usuario.
#sintaxis: @receiver(señal, sender=MyModel)..
# Los parámetros significan lo siguiente:
# sender: La clase de modelo con la que se llamó a la señal.
# instance: La instancia de a Profile, ya sea que se haya eliminado.
# Cuando se llama a la señal, ninguno de los parámetros estará vacío.
@receiver(post_delete, sender=Profile)#cada vez que se recibe una señal post_delete del modelo  Profile entrara aca.
#esta funcion-metodo se utiliza para eliminar las imagenes de perfil del sistema de archivos cuando un usuairo sea eliminado, por cascada tambien se elimina su Profile.
def delete_profilefile(sender, instance, **kwargs):
    #Se elimina el archivo del sistema de archivos cuando un objeto Profile se elimina..
    if instance.photo != 'profiles/defaultuser.png':#este if es para que no se elimine la defaultuser.png que es la foto default cuando un usuario inicia sesion.
        instance.photo.delete(save=False)#USAR EN PRODUCCION
        #if os.path.isfile(instance.photo.path):#usar en desarrollo
            #os.remove(instance.photo.path)#usar en desarrollo









class FollowersRequest(models.Model):#Este modelo representara los campos que tendria el campo followers del modelo Profile en la app users.
    #ForeignKey es una relación uno a muchos,estos campos requieren que el primer argumento sea la clase del modelo al que se relacionan.
    #Cuando define una clave externa o relaciones de muchos a muchos con el modelo de usuario, debe especificar el modelo personalizado mediante la AUTH_USER_MODELconfiguración.
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='to_user', on_delete=models.CASCADE)#indica el usuario al que se enviará la solicitud de seguir. Tendrá el mismo parámetro on_delete que decide cuándo se elimina el usuario, también eliminamos la solicitud de amistad.
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='from_user', on_delete=models.CASCADE)#indica el usuario que envía la solicitud de seguir. También se eliminará si se elimina el usuario.

    def __str__(self):#el str que decide cómo Django mostrará nuestro modelo en el panel de administración.
        return "From {}, to {}".format(self.from_user.username, self.to_user.username)

