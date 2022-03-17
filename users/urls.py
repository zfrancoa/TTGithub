from django.urls import path, include
from .views import login_anfitrion, update_profile, register, ChangeEmailUpdateView, users_list, send_or_delete_follower_request, user_profile, accept_follower_request, myprofile, request_follow_sent, request_follow_received, reject_request_received, FollowersListView, delete_follower, delete_following, FollowingsListView, search_user, update_username, UserDeleteView, search_user_2, list_notification


#from .views import activate#para validación de email.




urlpatterns = [
    #Add Django site authentication urls (for login, logout, password management)
    #SI DEJAMOS ESTA URL ACA SOLO PODREMOS USAR EL SISTEMA DE AUTENTICACIÓN EN LA APLICACIÓN users, por eso lo pondremo en el url del proyecto.
    #path('accounts/', include('django.contrib.auth.urls')),#agregar la url de autenticacion nos dara acceso a otras urls que se proporcionan
    path('update_profile/',update_profile, name="update_profile"),
    path("register/", register, name="register"),
    path("change_email/", ChangeEmailUpdateView.as_view(), name = "ChangeEmailUpdateView"),
    path("users_list/", users_list, name="users_list"),#url para la vista que mostrara una lista de usuarios recomendada para mostrar y poder comenzar a seguir.
    path("send_or_delete_follower_request/", send_or_delete_follower_request, name="send_or_delete_follower_request"),#url para enviar el id del usuario al que le enviamos la solicitud de amistad O LA ELIMINAMOS.
    path("profile/<username>/", user_profile, name="user_profile"),#url paramostrar perfil de usuario no logeado.
    path("accept_follower_request/", accept_follower_request, name="accept_follower_request"),#url para aceptar la solicitud de follow
    path('myprofile/', myprofile, name='myprofile'),#no hace falta pasar el username como parametro, porque ya sabemos que esta vista es para el usuario logeado, representa al eprfil del usuario logeado.
    path('request_follow_sent/', request_follow_sent, name='request_follow_sent'),#no hace falta pasar el username como parametro, porque ya sabemos que esta vista es para el usuario logeado, representa a las solicitudes enviadas por el usuario logeado.
    path('request_follow_received/', request_follow_received, name='request_follow_received'),#no hace falta pasar el username como parametro, porque ya sabemos que esta vista es para el usuario logeado, representa a las solicitudes recibidas  por el usuario logeado.
    path('reject_request_received/', reject_request_received, name='reject_request_received'),#rechazar solicitud recibida
    path('FollowersListView/<int:pk>/', FollowersListView.as_view(), name='FollowersListView'),#para ver seguidores de un usuario.
    path('FollowingsListView/<int:pk>/', FollowingsListView.as_view(), name='FollowingsListView'),#para ver seguidores de un usuario.
    path('delete_follower/', delete_follower, name='delete_follower'),#elimina un seguidor
    path('delete_following/', delete_following, name='delete_following'),#elimina al usuario logeado de la lista de seguidores de un usuario, particularmente del que dejemos de seguir.
    path('search_user', search_user, name='search_user'),#Busca un usuario.
    path('update_username', update_username, name='update_username'),#edita el nomrbe de usuario.
    path('UserDeleteView/<int:pk>/', UserDeleteView.as_view(), name='UserDeleteView'),#edita el nomrbe de usuario.
    path('search_user_2/', search_user_2, name='search_user_2'),
    path('list_notification/', list_notification, name='list_notification'),


    path('login_anfitrion/', login_anfitrion, name='login_anfitrion'),

    #PARA VALIDACIÓN DE EMAIL:
    #path('activate/<uidb64>/<token>/', activate, name='activate'),

    ###--------------------####




]


urlpatterns += [
    path('captcha/', include('captcha.urls')),
]