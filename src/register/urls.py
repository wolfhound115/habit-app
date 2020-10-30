from django.urls import path, re_path
from .views import (
    register

)

from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf import settings



#we are mapping URLs to View functions
urlpatterns = [

    re_path(r'^register/$', register,  name='register'),
    re_path(r'^login/$', auth_views.LoginView.as_view(), name='login'),
    re_path(r'^logout/$', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    
]

