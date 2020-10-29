from django.urls import path, re_path
from .views import (
    register

)




#we are mapping URLs to View functions
urlpatterns = [

    re_path(r'^register/$', register,  name='register'),
    
]

