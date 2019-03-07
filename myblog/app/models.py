from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.urls import  reverse

class Post(models.Model):
    STATUS_CHOICES=(
        ('draft','Draft'),
        ('published','Published')
    )
    title= models.CharField(max_length=100)
    slug=models.SlugField(max_length=120)
    author=models.ForeignKey(User ,related_name='blog_posts',on_delete=False)
    body=models.TextField(default="This is the body this is to check")
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    status= models.CharField(max_length=10,choices=STATUS_CHOICES,default='draft')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post_detail",args=[self.id,self.slug])