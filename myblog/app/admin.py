from django.contrib import admin
from . models import Post
# Register your models here.


class PostAdmin(admin.ModelAdmin):
    list_display = ['title','slug','author','status']
    list_filter =['status','created','updated']
    search_fields = ['title','author__username']
admin.site.register(Post,PostAdmin)