from django.shortcuts import render,get_object_or_404, redirect
from django.http import HttpResponse,HttpResponseRedirect, JsonResponse, Http404
from.models import *
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.loader import render_to_string
from django.forms import modelformset_factory
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.


def post_list(request):
    posts = Post.objects.all().order_by('-id')
    query = request.GET.get('q')
    if query:
        posts = Post.objects.filter(
            Q(title__icontains=query)|
            Q(author__username__icontains=query)|
            Q(body__icontains=query)
        )

    paginator = Paginator(posts,5)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    if page is None:
        start_index = 0
        end_index = 5
    else:
        (start_index, end_index) = proper_pagination(posts, index=4)

    page_range = list(paginator.page_range)[start_index:end_index]

    context = {'posts': posts, 'page_range': page_range}

    return render(request, 'app/post_list.html', context)

def home(request):
    return redirect('post_list')


def proper_pagination(posts, index):
    start_index = 0
    end_index = 5
    if posts.number > index:
        start_index = posts.number - index
        end_index = start_index + end_index
    return start_index, end_index


def post_detail(request, id, slug):
    post = get_object_or_404(Post, id=id, slug=slug)
    comments = Comment.objects.filter(post=post).order_by('-id')
    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        is_liked = True

    if request.method == 'POST':
        comment_form = CommentForm(request.POST or None)
        if comment_form.is_valid():
            content = request.POST.get('content')
            comment = Comment.objects.create(post=post, user=request.user, content=content)
            comment.save()
            # return HttpResponseRedirect(post.get_absolute_url())
    else:
        comment_form= CommentForm()

    context = {
        'post': post,
        'is_liked': is_liked,
        'total_likes': post.total_likes(),
        'comments': comments,
        'comment_form': comment_form,
    }
    if request.is_ajax():
        html = render_to_string('app/comments.html', context, request=request)
        return JsonResponse({'form': html})

    return render(request, 'app/post_detail.html', context)


def post_create(request):

    ImageFormset = modelformset_factory(Images, fields=('image',), extra=4)
    if request.method == 'POST':
        form = PostCreateForm(request.POST)
        formset = ImageFormset(request.POST or None, request.FILES or None)
        if form.is_valid()and formset.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            for f in formset:
                print(f.cleaned_data)
                try:
                    photo = Images(post=post, image=f.cleaned_data.get('image'))
                    photo.save()
                except Exception as e:
                    break
            messages.success(request, "Post has been successfully created.")
            return redirect('post_list')
    else:
        form = PostCreateForm()
        formset = ImageFormset(queryset=Images.objects.none())
    context={'form': form,'formset':formset}
    return render(request,'app/post_create.html',context)


def post_delete(request, id):
    post = get_object_or_404(Post, id=id)
    post.delete()
    messages.warning(request, 'post has been successfully deleted!')
    return redirect('post_list')



def post_edit(request,id):
    try:
        print("1111111111111111")
        post = get_object_or_404(Post, id=id)
    except :
        print("Login Through Social does not have Profile ")
        post=None
        pass
    ImageFormset = modelformset_factory(Images, fields=('image',), extra=4, max_num=4)
    if post.author != request.user:
        raise Http404()
    if request.method == "POST":
        form = PostEditForm(request.POST or None, instance=post)
        formset = ImageFormset(request.POST or None, request.FILES or None)
        if form.is_valid() and formset.is_valid():
            form.save()
            data = Images.objects.filter(post=post)
            for index, f in enumerate(formset):
                if f.cleaned_data:
                    if f.cleaned_data['id'] is None:
                        photo = Images(post=post, image=f.cleaned_data.get('image'))
                        photo.save()
                    elif f.cleaned_data['image'] is False:
                        photo = Images.objects.get(id=request.POST.get('form-' + str(index) + '-id'))
                        photo.delete()
                    else:
                        photo = Images(post=post, image=f.cleaned_data.get('image'))
                        d = Images.objects.get(id=data[index].id)
                        d.image = photo.image
            messages.success(request, "{} has been successfully updated!".format(post.title))
            return HttpResponseRedirect(post.get_absolute_url())
    else:
        form = PostEditForm(instance=post)
        formset = ImageFormset(queryset=Images.objects.filter(post=post))
    context = {'form': form,'post': post, 'formset': formset}
    return render(request, 'app/post_edit.html', context)


def like_post(request):
    post = get_object_or_404(Post,id=request.POST.get('post_id'))
    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
        is_liked = True
    context = {'post': post, 'is_liked': is_liked, 'total_likes': post.total_likes()}
    return HttpResponseRedirect(post.get_absolute_url())

    # pass


def UserLoginView(request):

    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            print(username)
            password = request.POST['password']
            print(password)
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('post_list'))
                else:
                    return HttpResponse('User Not Active')
            else:
                return HttpResponse('User Not Found')
    else:
        form = UserLoginForm()
    context = {'form': form}
    return render(request, 'app/login.html', context)


def UserLogoutView(request):
    logout(request)
    return redirect('post_list')


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
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
        user_form = UserEditForm(data=request.POST or None, instance=request.user)
        profile_form = ProfileEditForm(data=request.POST or None,instance=request.user.profile, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return HttpResponseRedirect(reverse("edit_profile"))
    else:
        try:
            user_form = UserEditForm(instance=request.user)
        except:
            print("Social Login does not have Profile")
            user_form=None
        profile_form = ProfileEditForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request,'app/edit_profile.html',context)
