"""Travel_Try URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView

from .views import first_page

urlpatterns = [

    path('admin/', admin.site.urls),
    
    #Add Django site authentication urls (for login, logout, password management)
    path('accounts/', include('django.contrib.auth.urls')),#agregar la url de autenticacion nos dara acceso a otras urls que se proporcionan

    ## Las URLs de la aplicación publish fueron incluidas dentro del proyecto con un mapeador a publish/, entonces las URLs  que llegan a este mapeador deben empezar con publish/.::
    path('publish/', include('publish.urls')),#la app se llama publish

    ## Las URLs de la aplicación users fueron incluidas dentro del proyecto con un mapeador a publish/, entonces las URLs  que llegan a este mapeador deben empezar con publish/.::
    path('users/', include('users.urls')),#la app se llama publish

    ## Las URLs de la aplicación maps fueron incluidas dentro del proyecto con un mapeador a maps/, entonces las URLs  que llegan a este mapeador deben empezar con maps/.::
    path('maps/', include('map.urls')),#la app se llama map

    ## Las URLs de la aplicación maps fueron incluidas dentro del proyecto con un mapeador a maps/, entonces las URLs  que llegan a este mapeador deben empezar con maps/.::
    path('telegrams/', include('telegram.urls')),#la app se llama telegram
  
    ## Las URLs de la aplicación legals fueron incluidas dentro del proyecto con un mapeador a legals/, entonces las URLs  que llegan a este mapeador deben empezar con legals/.::
    path('legals/', include('legals.urls')),#la app se llama legals

    #url para que al ingresar traveltry.com.ar no sucedan errores, o sea que meustre una plantila:
    path('', first_page, name='first_page'),

    # path(
    #     "favicon.ico",
    #     RedirectView.as_view(url=staticfiles_storage.url("favicon.ico")),
    # ),
]



if settings.DEBUG:#si estamos en modo de desarrollo(depuración) entramos,y no en modo de producción
    urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)#los archivos cargados se guardaran en el directorio indicado por MEDIA_ROOT
