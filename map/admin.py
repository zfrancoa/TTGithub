from django.contrib import admin
from .models import WorldCountries, WorldCountriesUser


# Register your models here.


class WorldCountriesAdmin(admin.ModelAdmin):#AGREGAMOS UN BUSCAR AL MODELO WorldCountries
    # con esto muestras los campos que deses al mostrar la lista en admin
    list_display=['countries_tot']
    # con esto añades un campo de texto que te permite realizar la busqueda, puedes añadir mas de un atributo por el cual se filtrará
    search_fields = ['countries_tot', 'descripcion']
    # con esto añadiras una lista desplegable con la que podras filtrar (activo es un atributo booleano)
    list_filter = ['countries_tot']



admin.site.register(WorldCountries, WorldCountriesAdmin)

admin.site.register(WorldCountriesUser)