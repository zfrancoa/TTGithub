from django.urls import path
from .views import index, AddPhotoCreateView, GalleryView, Add_Country, search_country_ajax, Delete_Country, CountryDeleteView, give_name_get_id, tutorial_add_photo_to_country_session



urlpatterns = [

    path('<int:pk>/',index, name='index'), #aca se pasara el id del usuario al que le querramos mirar el mapa.
    #EL pk QUE SE PASA ACA DEBAJO ES EL id QUE CORRESPONDE AL PAIS QUE SE AGREGARA.
    #path('addall/', add_all, name='add_all'),
    # path('gallery/<int:pk>/<username>/', gallery, name='gallery'),#aca se pasa el id del pais donde hemos clickeado y el nombre de usuario del que estemos mirando el mapa.
    path('AddPhotoCreateView/<int:pk>/', AddPhotoCreateView.as_view(), name='AddPhotoCreateView'),#URL Y VISTA PARA AGREGAR FOTOS.
    path('GalleryView/<int:pk>/<username>/', GalleryView.as_view(), name='GalleryView'),
    path("Add_Country/", Add_Country, name = "Add_Country"),#vista para agregar pais
    path("search_country_ajax/", search_country_ajax, name = "search_country_ajax"),#vista para buscar paises, enlazada con ajax
    path("Delete_Country/", Delete_Country, name = "Delete_Country"),#vista para elegir que pais eliminar.
    path('CountryDeleteView/<int:pk>/', CountryDeleteView.as_view(), name='CountryDeleteView'),#URL Y VISTA PARA AGREGAR FOTOS.
    path("give_name_get_id/", give_name_get_id, name = "give_name_get_id"),#vista para obtener id de un pais.
    path("tutorial_add_photo_to_country_session/", tutorial_add_photo_to_country_session, name = "tutorial_add_photo_to_country_session"),#vista para agregar sesion que indica que no se muestre el formulario.

]    


