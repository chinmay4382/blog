from django.contrib import admin
from . models import Post,Profile
# Register your models here.


class PostAdmin(admin.ModelAdmin):
    list_display = ['title','slug','author','status']
    list_filter =['status','created','updated']
    search_fields = ['title','author__username']

admin.site.register(Post,PostAdmin)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user','dob','photo')

admin.site.register(Profile,ProfileAdmin)


