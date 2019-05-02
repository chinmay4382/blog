from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.urls import reverse
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager,self).get_queryset().filter(status="published")


class Post(models.Model):
    objects = models.Manager()
    published = PublishedManager()
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published')
    )
    id = models.AutoField(primary_key=True, auto_created=True)
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120)
    author = models.ForeignKey(User,related_name='blog_posts',on_delete=False)
    body = models.TextField(default="This is the body this is to check")
    likes = models.ManyToManyField(User,related_name='app_posts')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,choices=STATUS_CHOICES,default='draft')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post_detail",args=[self.id,self.slug])

    def total_likes(self):
        return self.likes.count()


@receiver(pre_save,sender=Post)
def pre_save_slug(sender,**kwargs):
    slug= slugify(kwargs['instance'].title)
    kwargs['instance'].slug = slug


class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    dob = models.DateField(null=True,blank=True)
    photo = models.ImageField(null=True,blank=True)

    def __str__(self):
        return "Profile of user{}".format(self.user.username)


class Images(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', blank=True, null=True)

    def __str__(self):
        return str(self.post.id)


class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    content = models.TextField(max_length=160)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}-{}'.format(self.post.title, str(self.user.username))
