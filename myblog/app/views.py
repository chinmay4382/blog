from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse,HttpResponseRedirect
from.models import Post,Profile
from .forms import PostCreateForm,UserLoginForm,UserRegistrationForm,UserEditForm,ProfileEditForm
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required

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
    if request.method =="POST":
        form=UserRegistrationForm(request.POST or None)
        if form.is_valid():
            new_user=form.save(commit=False)
            password = form.cleaned_data.get('password')
            new_user.set_password(password)
            new_user.save()
            Profile.objects.create(user=new_user)
            return redirect('post_list')
    else:
        form = UserRegistrationForm()
    context = {'form': form}
    return render(request,'registration/register.html', context)


def edit_profile(request):
    if request.method == 'POST':
        user_form =UserEditForm(data=request.POST or None,instance=request.user)
        profile_form =ProfileEditForm(data=request.POST or None,instance=request.user.profile,files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form=UserEditForm(instance=request.user)
        profile_form=ProfileEditForm(instance=request.user.profile)

    context={
        'user_form':user_form,
        'profile_form':profile_form,
    }
    return render(request,'app/edit_profile.html',context)