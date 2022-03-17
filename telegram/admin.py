from django.contrib import admin

from  .models import Chat_Message, Delete_Chat, Active_Chat

# Register your models here.

admin.site.register(Delete_Chat)#para que podamos manejar las tablas de Profile en el admin

admin.site.register(Chat_Message)

admin.site.register(Active_Chat)
