from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse,HttpResponseRedirect
from.models import Post
from .forms import PostCreateForm,UserLoginForm,UserRegistrationForm
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
# Create your views here.

def post_list(request):
    posts=Post.objects.all()
    context={'posts':posts,}
    return render(request,'app/post_list.html',context)

def post_detail(request,id,slug):
    post=get_object_or_404(Post,id=id,slug=slug)
    context={'post':post}
    return render(request,'app/post_detail.html',context)


def post_create(request):
    if request.method == 'POST':
        form= PostCreateForm(request.POST)
        if form.is_valid():
            post=form.save(commit=False)
            post.author=request.user
            post.save()
    else:
        form= PostCreateForm()

    context={'form':form}
    return render(request,'app/post_create.html',context)

def UserLoginView(request):
    if request.method=='POST':
        form =UserLoginForm(request.POST)
        if form.is_valid():
            username=request.POST['username']
            password=request.POST['password']
            user= authenticate(username=username,password=password)
            if user:
                if user.is_active:
                    login(request,user)
                    return HttpResponseRedirect(reverse('post_list'))
                else:
                    return HttpResponse('User Not Active')
            else :
                return HttpResponse('User Not Found')
    else:
        form=UserLoginForm()
        context={'form':form}
        return render(request,'app/login.html',context)


def UserLogoutView(request):
    logout(request)
    return redirect('post_list')


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('post_list')


    else:
        form = UserRegistrationForm()
    context = {'form': form}
    return render(request,'registration/register.html', context)
