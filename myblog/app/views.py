from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from.models import Post
# Create your views here.

def post_list(request):
    posts=Post.objects.all()
    context={'posts':posts,}
    return render(request,'app/post_list.html',context)

def post_detail(request,id,slug):
    post=get_object_or_404(Post,id=id,slug=slug)
    context={'post':post}
    return render(request,'app/post_detail.html',context)
