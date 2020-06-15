from django.urls import path
from .views import (
    habit_post_create_view,
    habit_post_delete_view,
    habit_post_detail_view,
    habit_post_list_view,
    habit_post_update_view,
)


#we are mapping URLs to View functions
urlpatterns = [
    path('', habit_post_list_view),
    path('posts/<str:url_slug>/', habit_post_detail_view),
    path('posts/<str:url_slug>/edit/', habit_post_update_view),
    path('posts/<str:url_slug>/delete/', habit_post_delete_view),
]
