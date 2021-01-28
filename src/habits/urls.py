from django.urls import path, re_path
from .views import (
    habit_post_create_view,
    habit_post_delete_view,
    habit_post_detail_view,
    habit_all_posts_list_view,
    habit_post_update_view,
    habit_all_tracks_list_view,
    habit_track_detail_feed_view,
    habit_track_detail_grid_view,
    PostLikeToggle,
    CommentLikeToggle,
    ProfileFollowToggle,
    post_list,
    AutoCompleteView,
    EditPostView,
    ConfirmPostDeleteView
)




#we are mapping URLs to View functions
urlpatterns = [
    path('', post_list, name='post-list'),
    path('<str:url_username>/', habit_all_posts_list_view, name='user-profile'),
    path('<str:url_username>/posts/<str:url_slug>/', habit_post_detail_view),
    path('<str:url_username>/posts/<str:url_slug>/edit/', EditPostView.as_view()),
    path('<str:url_username>/posts/<str:url_slug>/delete/', ConfirmPostDeleteView.as_view(), name='confirm-delete-post'),
    path('<str:url_username>/tracks', habit_all_tracks_list_view),
    path('<str:url_username>/tracks/<str:url_slug>/feed', habit_track_detail_feed_view),
    path('<str:url_username>/tracks/<str:url_slug>/grid', habit_track_detail_grid_view),
    re_path(r'^ajax/post-like/$', PostLikeToggle,  name='PostLikeToggle'),
    re_path(r'^ajax/comment-like/$', CommentLikeToggle,  name='CommentLikeToggle'),
    re_path(r'^ajax/profile-follow/$', ProfileFollowToggle,  name='ProfileFollowToggle'),
    re_path(r'^ajax/autocomplete/$',AutoCompleteView.as_view(), name='autocomplete')
    
]



