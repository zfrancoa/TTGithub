from .base import *#importar todas las variables de configuración del archivo base.py a local.py(LAS QUE NO CAMBIAMOS ACA DENTRO)
from pathlib import Path
from decouple import config

#production.py: Configuraciones para el entorno de producción.

###----------------#####
# SECURITY WARNING: don't run with debug turned on in production!
# En un entorno local tener el modo DEBUG activado te facilitará visualizar una página detallada de errores a la hora de codear. En un entorno de producción no queremos mostrarle a nuestros usuarios esos errores detallados, ya que contiene datos sensibles del servidor, por lo que estaríamos expuestos a detalles de seguridad.

# La variable de configuración ALLOWED_HOSTS es una lista de hosts/nombres de dominio que nuestro sitio de Django puede servir. Si la variable DEBUG es True y ALLOWED_HOSTS es una lista vacía se proporcionará acceso solamente a ['.localhost', '127.0.0.1', '[::1]'].

DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = ["127.0.0.1", "rocky-stream-90067.herokuapp.com",".herokuapp.com", "traveltry.com.ar", "www.traveltry.com.ar",]


###-----------------#####


#####°°°°°°°°°°°°°°°#########
#Para el entorno de producción, Django soporta múltiples motores de base de datos para usar, como MariaDB, MySQL, Oracle o PostgreSQL. El siguiente es un ejemplo para PostgreSQL (Recuerda tener instalado el driver correspondiente con el motor de base de datos):

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': config("DB_NAME"),
#         'USER': config("DB_USER"),
#         'PASSWORD': config("DB_PASSWORD"),
#         'HOST': 'localhost',
#         'PORT': '',
#     }
# }
#####°°°°°°°°°°°°°°###########
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        #Estamos utilizando sqlite3, que para las pruebas, se ejecuta como una base de datos en memoria y, por lo tanto, las pruebas no se ejecutarán correctamente. Necesitamos decirle a nuestro proyecto que la sqlite3base de datos no necesita estar en la memoria para ejecutar las pruebas, esto es lo que hacemos con la siguiente linea:
        'TEST': {
            'NAME': os.path.join(BASE_DIR, 'db_test.sqlite3')
        }
    }
}


import dj_database_url
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)