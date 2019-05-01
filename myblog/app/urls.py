"""myblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from app.views import *
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', post_list, name='post_list'),
    path('<int:id>/<slug:slug>/', post_detail, name='post_detail'),
    path('create/', post_create, name='post_create'),
    path('login/',UserLoginView, name='user_login'),
    path('logout/', UserLogoutView, name='user_logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset/confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('password-reset/complete', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('register/', register, name='register'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('<int:id>/edit_post',post_edit, name='edit_post'),
    path('<int:id>/delete_post', post_delete, name='post_delete'),
    path('oauth/',include('social_django.urls')),
    path('like',like_post,name='like_post'),

]

if settings.DEBUG==True:
    urlpatterns +=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

