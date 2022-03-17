from django.contrib import admin
from  users.models import Profile, FollowersRequest

# Register your models here.

admin.site.register(Profile)#para que podamos manejar las tablas de Profile en el admin

admin.site.register(FollowersRequest)