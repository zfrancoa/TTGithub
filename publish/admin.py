from django.contrib import admin
from  .models import Post, Comments, Like, Sharing_Post, report_post

# Register your models here.

#admin.site.register(Post)#para que podamos manejar las tablas de Post en el admin
admin.site.register(Comments)#para que podamos manejar las tablas de Comments en el admin
admin.site.register(Like)#para que podamos manejar las tablas de Like en el admin
admin.site.register(Sharing_Post)#modelo para compartir posts.
admin.site.register(report_post)#modelo para reportar post.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):#con esto tendremos un buscador de post a partir del cmapo body
    search_fields = ["body"]
