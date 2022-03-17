from django.urls import path, include
from .views import HomeListView, PostCreateView, PostDetailView, PostUpdateView, PostDeleteView, PostFormView, like, FeaturedPostCreateView, FeaturedPostListView, LikesListView, SharingPostDeleteView, Share_Post, delete_comment, Report_Post, upload_photo


urlpatterns = [

    path('', HomeListView.as_view(), name="home"),#aca es donde se retorna al usuario luego de logearse, aca se mostrara una lista de publicaciones de nuestros following.
    path("PostCreateView/", PostCreateView.as_view(), name = "PostCreateView"),#vista para crear una publicacion.
    path("post-detail/<int:pk>/", PostDetailView.as_view(), name="post-detail"),#vista para mostrar detalles de una publicación, tambien recibe el get del formulario para los comentarios..
    path("PostUpdateView/<int:pk>/", PostUpdateView.as_view(), name = "PostUpdateView"),#vista para actualizar una publicacion.
    path("PostDeleteView/<int:pk>/", PostDeleteView.as_view(), name = "PostDeleteView"),#vista para eliminar una publicacion.
    path("PostFormView/<int:pk>/", PostFormView.as_view(), name = "PostFormView"),#vista para solicitud post del formulario de comentario.
    path("like/", like, name = "like"),#vista para dar like
    path("FeaturedPostCreateView/", FeaturedPostCreateView.as_view(), name = "FeaturedPostCreateView"),#vista para crear una Featured photos.
    path("FeaturedPostListView/<int:pk>/", FeaturedPostListView.as_view(), name = "FeaturedPostListView"),#vista para listar las Featured photos.
    path("Share_Post/", Share_Post, name = "Share_Post"),#vista para compartir post
    path("SharingPostDeleteView/<int:pk>/", SharingPostDeleteView.as_view(), name = "SharingPostDeleteView"),#vista para eliminar una sharing publicacion.
    path("delete_comment/", delete_comment, name = "delete_comment"),#vista para eliminar comentario
    path("Report_Post/<int:id>/", Report_Post, name = "Report_Post"),#vista para Reportar Post
    path("upload_photo/", upload_photo, name = "upload_photo"),#vista para elegir una opcion para subir una foto
    path("LikesListView/<int:pk>/", LikesListView.as_view(), name = "LikesListView"),#vista para listar las Featured photos.

]
