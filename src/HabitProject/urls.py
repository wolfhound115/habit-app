"""habit URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from habits.views import (
    habit_post_detail_page
)

#whatever view you want to use you have to import here
from .views import (
    home_page,
    about_page,
    contact_page
)


#we are mapping URLs to View functions
urlpatterns = [
    path('', home_page),
    path('habit/<str:url_slug>/', habit_post_detail_page),
    path('about/', about_page),
    path('contact/', contact_page),
    path('admin/', admin.site.urls),
]
