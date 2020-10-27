from django.urls import path, re_path
from .views import (
    register

)




#we are mapping URLs to View functions
urlpatterns = [

    re_path(r'^register/$', register,  name='register'),
    
]

#urlpatterns += [re_path(r'^like/', PostLikeToggle,  name='PostLikeToggle')] #need to figure out if this url is correct... might cause issues if some other url starts with 'like'


