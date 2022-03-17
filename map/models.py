from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.


#EN EL MODELO WorldCountries ALMACENAREMOS TODOS LOS PAISES DEL PLANETA.
class WorldCountries(models.Model):
    #countries:
    countries_tot = models.CharField(max_length=60, null=True)  

    def __str__(self):#ESTO ES PARA QUE DJANGO NOS MUESTRE el modelo(OBJETO) como especificamos en el str.
        return self.countries_tot



#EN EL MODELO WorldCountriesUser ALMACENAREMOS LOS PAISES DEL USUARIO
class WorldCountriesUser(models.Model):
    #countries:Se almacenaran los paises del usuario.
    countries_user = models.CharField(max_length=60, null=True)  
    #user_name: es una relacion uno a muchos, ya que un usuario puede tener muchos paises del mapa, pero un pais solo puede pertenecer a un usuario.
    #ForeignKey es una relación uno a muchos,estos campos requieren que el primer argumento sea la clase del modelo al que se relacionan.
    #El uso de on_delete = models.CASCADE se usa para que cuando se elimine el usuario tambien se elimine la publicacion.
    username = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):#el str que decide cómo Django mostrará nuestro modelo en el panel de administración.
        return "Country {}, from {}".format(self.countries_user, self.username)

