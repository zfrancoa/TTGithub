from .base import *#importar todas las variables de configuración del archivo base.py a local.py(LAS QUE NO CAMBIAMOS ACA DENTRO)


#local.py: Contiene todas las configuraciones de tu entorno local (que incluyen las de base.py).

# SECURITY WARNING: don't run with debug turned on in production!
# En un entorno local tener el modo DEBUG activado te facilitará visualizar una página detallada de errores a la hora de codear. En un entorno de producción no queremos mostrarle a nuestros usuarios esos errores detallados, ya que contiene datos sensibles del servidor, por lo que estaríamos expuestos a detalles de seguridad.

# La variable de configuración ALLOWED_HOSTS es una lista de hosts/nombres de dominio que nuestro sitio de Django puede servir. Si la variable DEBUG es True y ALLOWED_HOSTS es una lista vacía se proporcionará acceso solamente a ['.localhost', '127.0.0.1', '[::1]'].

DEBUG = True

ALLOWED_HOSTS=['127.0.0.1', '192.168.0.14', '192.168.0.8']#Dejar ALLOWED_HOSTS vacia, esta ip es de la net del gob y la agregamos para poder acceder desde el celular.

###-----------------#####



###!!!!!!!!!!!!!!!!!#####
# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
#la variable de configuración DATABASES que contiene las configuraciones para todas las bases de datos usadas con Django:
#En un entorno local nos interesa manejar datos de prueba para verificar el funcionamiento de la aplicación, Django trae por defecto la configuración con una base de datos SQLite, que no es más que un simple archivo donde son guardados los datos.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
###!!!!!!!!!!!!!!!!!######



