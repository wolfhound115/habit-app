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
from django.conf import settings


from django.contrib import admin
from django.urls import path, include
from habits.views import (
    habit_post_create_view,
    habit_track_create_view,
)
import django

#whatever view you want to use you have to import here
from .views import (
    home_page,
    about_page,
    contact_page
)


#we are mapping URLs to View functions


urlpatterns = [
    path('', home_page),
    path('habit/new-post/', habit_post_create_view),
    path('habit/new-track/', habit_track_create_view),
    path('habit/', include('habits.urls')),

    path('about/', about_page),
    path('contact/', contact_page),
    path('admin/', admin.site.urls),
]


# MANDATORY for using django-recurrence
# https://django-recurrence.readthedocs.io/en/latest/installation.html
import django
from django.conf.urls import url
from django.views.i18n import JavaScriptCatalog

# Your normal URLs here...

# If you already have a js_info_dict dictionary, just add
# 'recurrence' to the existing 'packages' tuple.
js_info_dict = {
    'packages': ('recurrence', ),
}

# jsi18n can be anything you like here
urlpatterns += [
    url(r'^jsi18n/$', JavaScriptCatalog.as_view(), js_info_dict),
]


# jsi18n can be anything you like here
urlpatterns += [
    path('jsi18n/', django.views.i18n.JavaScriptCatalog.as_view(
        packages=['recurrence']), name="javascript-catalog"),
]
# monkey patch workaround for bug in recurrence library
django.views.i18n.javascript_catalog = None

if settings.DEBUG:
    # test mode
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)





