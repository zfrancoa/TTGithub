#base.py: Todas las configuraciones en común entre entornos.

"""
Django settings for Travel_Try project.

Generated by 'django-admin startproject' using Django 3.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
from decouple import config
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True#ESTA VARIABLE SE PUEDE ELIMINAR.

# ALLOWED_HOSTS = []#ESTA VARIABLE SE PUEDE ELIMINAR.

######-----------------######################
#modularizamos las apps
# Application definition

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'channels',
    'crispy_forms',
    'captcha',
    'whitenoise.runserver_nostatic',
    
]

LOCAL_APPS = [  
    'users',#app para tratar el tema de los usuario, logeo, followers, etc.
    'publish',#publicaciones de los usuarios.
    'map',#mapa de cada usuario.
    'telegram',#mensajes entre usuarios.
    'legals',#cosas legales como licencias, condiciones y terminos, politica de privacidad, etc.
]

INSTALLED_APPS = THIRD_PARTY_APPS + DJANGO_APPS + LOCAL_APPS
######-----------------######################


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # Add whitenoise middleware here
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = f'{config("PROJECT_NAME")}.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['./templates',],#ESTAMOS INDICANDO A DONDE DEBE IR A BUSCAR LAS PLANTILLAS, EN ESTE CASO EL PUNTO INDICA EL DIRCTORIO RAIZ DEL PROYECTO, DENTOR DE LA CARPETA templates.
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


WSGI_APPLICATION = f'{config("PROJECT_NAME")}.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
#la variable de configuración DATABASES que contiene las configuraciones para todas las bases de datos usadas con Django:
#En un entorno local nos interesa manejar datos de prueba para verificar el funcionamiento de la aplicación, Django trae por defecto la configuración con una base de datos SQLite, que no es más que un simple archivo donde son guardados los datos.
# DATABASES = {#YA SE PUEDE EIMINAR ESTA VARIABLE.
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True



# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


CRISPY_TEMPLATE_PACK = 'bootstrap4'#Además, dado que crispy_forms usa Bootstrap 3 por defecto, nos encantaría configurarlo para usar Bootstrap 4. Para hacerlo, agregue esta línea


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/
#Por último tenemos la variable de configuración STATIC_URL que es la URL a usar para hacer referencia a los archivos estáticos, puede tener diferentes valores dependiendo del entorno, pero por ahora usaremos el mismo valor para los archivos local.py y production.py.


# STATICFILES_DIRS = ((os.path.join(BASE_DIR, 'static')), )
# STATIC_URL = '/static/'


#---1----lo siguiente es para poder trabajar con las imagenes, y que estas se guarden en la carpeta media----
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
#STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


######°°°°°°°°°°°°°°°°°°°°°#############
#A donde nos direccionaremos despues de hacer login
LOGIN_REDIRECT_URL = "home"#ESTA URL PERTENECERA A LA APP publish, porque en este template se mostraran las ultimas publicaciones de las personas que seguimos.
#A donde nos direccionaremos despues de hacer logout
#LOGOUT_REDIRECT_URL = "login"
LOGOUT_REDIRECT_URL = "login"
######°°°°°°°°°°°°°°°°°°°°°#############

#ENVIO DE EMAILS:
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config('EMAIL_HOST_USER')#a partir de la libreria decouple protegemos el nombre email, el verdade se encuentra en el archivo .env en el directorio raiz del proyecto.
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')#a partir de la libreria decouple protegemos la contraseña, el verdade se encuentra en el archivo .env en el directorio raiz del proyecto.



# Channels
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#configuramos ASGI_APPLICATION para que apunte a ese objeto de enrutamiento como su aplicación raíz:
#apuntamos los canales a la configuración de enrutamiento raíz:

ASGI_APPLICATION = f'{config("PROJECT_NAME")}.routing.application'




#Antes de que podamos usar una capa de canal, debemos configurarla.:
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!