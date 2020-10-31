from django.urls import path, re_path
from .views import (
    NewsfeedView,
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
    autocompleteModel,
    AutoCompleteView,
    EditPostView,
)




#we are mapping URLs to View functions
urlpatterns = [
    path('', NewsfeedView.as_view(), name='newsfeed'),


    #TRYING TO GET INFINITE SCROLLING TO WORK
    path('posts/', post_list, name='post-list'),
    path('<str:url_username>/', habit_all_posts_list_view, name='user-profile'),
    path('<str:url_username>/posts/<str:url_slug>/', habit_post_detail_view),
    path('<str:url_username>/posts/<str:url_slug>/edit/', EditPostView.as_view()),
    path('<str:url_username>/posts/<str:url_slug>/delete/', habit_post_delete_view),
    path('<str:url_username>/tracks', habit_all_tracks_list_view),
    path('<str:url_username>/tracks/<str:url_slug>/feed', habit_track_detail_feed_view),
    path('<str:url_username>/tracks/<str:url_slug>/grid', habit_track_detail_grid_view),
    #path('post-like/', PostLikeToggle, name='PostLikeToggle'),
    re_path(r'^ajax/post-like/$', PostLikeToggle,  name='PostLikeToggle'),
    re_path(r'^ajax/comment-like/$', CommentLikeToggle,  name='CommentLikeToggle'),
    re_path(r'^ajax/profile-follow/$', ProfileFollowToggle,  name='ProfileFollowToggle'),
    re_path(r'^ajax/search/', autocompleteModel, name='search'),
    re_path(r'^ajax/autocomplete/$',AutoCompleteView.as_view(), name='autocomplete')
    
]

#urlpatterns += [re_path(r'^like/', PostLikeToggle,  name='PostLikeToggle')] #need to figure out if this url is correct... might cause issues if some other url starts with 'like'


