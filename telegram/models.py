from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
# Create your models here.






#ESTE MODELO SERA PARA ALMACENAR LOS MENSAJES:
class Chat_Message(models.Model):
    transmitter = models.ForeignKey(User,related_name='transmitter', on_delete=models.CASCADE)#quien transmite el mensaje.
    receiver = models.ForeignKey(User,related_name='receiver', on_delete=models.CASCADE)#quien recibe el mensaje.
    content = models.TextField(blank=True,null=True)#contenido del mensaje.
    created_at = models.DateTimeField(auto_now_add=True)#cuando fue creado.
    unread = models.BooleanField(default=False)#con este campo indicaremos si se ha leido el mensaje o no.




#ESTE MODELO TRATARA LA ELIMINACIÓN DE MENSAJES.
class Delete_Chat(models.Model):
    #QUIEN QUIERE ELIMINAR LOS MENSAJES:
    deleter = models.ForeignKey(User, related_name='deleter', on_delete=models.CASCADE)
    #CON QUIEN SE TIENE LA CONVERSACION:
    other = models.ForeignKey(User, related_name='other', on_delete=models.CASCADE)
    #FECHA DESDE LA CUAL SE ELIMINAN LOS MENSAJES.
    delete_at = models.DateTimeField(auto_now_add=True)
    


#ESTE MODELO ES PARA SABER LOS USUARIOS CON LOS QUE TENGAMOS CONVERSACIONES ACTIVAS.
class Active_Chat(models.Model):
    #QUIEN QUIERE ELIMINAR LOS MENSAJES:
    Tx = models.ForeignKey(User, related_name='Tx', on_delete=models.CASCADE)
    #CON QUIEN SE TIENE LA CONVERSACION:
    Rx = models.ForeignKey(User, related_name='Rx', on_delete=models.CASCADE)
    #FECHA DESDE LA CUAL SE ELIMINAN LOS MENSAJES.
    latest_activate = models.DateTimeField()
    