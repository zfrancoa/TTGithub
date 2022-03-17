"""
WSGI config for Travel_Try project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

#Ahora que cambiamos el archivo de configuración settings.py que trae Django por defecto a múltiples archivos de configuración por cada entorno, tenemos que actualizar los archivos asgi.py, wsgi.py y manage.py.
#La sigueinte linea quiere decir que ahora Django utilizará el archivo de configuración local.py
#cambair a os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Travel_Try.settings.local') cuando se vaya a utilizar django en producción.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Travel_Try.settings.production')

application = get_wsgi_application()
