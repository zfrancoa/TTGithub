#que hace este archivo: Necesitamos crear una configuración de enrutamiento para la chataplicación que tenga una ruta hacia el consumidor..
#O SEA, SIMILAR AL urls.py de django, que enlaza a vistas, este routing.py enlaza a consumidores.



# chat/routing.py


from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    #Llamamos al as_asgi()método de clase para obtener una aplicación ASGI que instanciará una instancia de nuestro consumidor para cada conexión de usuario.
    #o sea, para cada conexión se creara una instancia de consumidor que la manejara.
    re_path(r'chat/(?P<username>\w+)/$', consumers.ChatConsumer.as_asgi()),
    # re_path(r'ws/status/(?P<username>\w+)/$', consumers.StatusConsumer.as_asgi()),
]











