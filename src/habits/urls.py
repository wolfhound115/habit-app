from django.urls import path
from .views import (
    habit_post_create_view,
    habit_post_delete_view,
    habit_post_detail_view,
    habit_post_list_view,
    habit_post_update_view,
    habit_track_list_view,
    habit_track_detail_feed_view,
    habit_track_detail_grid_view,
)




#we are mapping URLs to View functions
urlpatterns = [
    path('', habit_post_list_view),
    path('posts/<str:url_slug>/', habit_post_detail_view),
    path('posts/<str:url_slug>/edit/', habit_post_update_view),
    path('posts/<str:url_slug>/delete/', habit_post_delete_view),
    path('tracks', habit_track_list_view),
    path('tracks/<str:url_slug>/feed', habit_track_detail_feed_view),
    path('tracks/<str:url_slug>/grid', habit_track_detail_grid_view)
]


