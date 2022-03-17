from django.urls import path
from .views import chat, delete_all_conversation, active_list

urlpatterns = [

    path('chat/<str:username>/', chat, name='chat'),#url para la vista de la sala de chat.
    path('delete_all_conversation/<str:username>', delete_all_conversation, name='delete_all_conversation'),#url para la vista que elimina toda una conversación.
    path('active_list/', active_list, name='active_list'),#url para la vista que elimina toda una conversación.

]


