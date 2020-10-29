from django.urls import path, re_path
from .views import (
    EditProfileView

)




#we are mapping URLs to View functions
urlpatterns = [

    re_path(r'^edit-profile/$', EditProfileView.as_view(),  name='edit-profile'),
    
]


