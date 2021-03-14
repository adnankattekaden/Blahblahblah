from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.homepage,name='homepage'),
    path('signin/', views.signin,name='signin'),
    path('signup/', views.signup,name='signup'),
    path('signout/', views.signout,name='signout'),

    path('password-reset/',auth_views.PasswordResetView.as_view(),name='password_reset'),
    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view() ,name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),name='password_reset_complete'),


    path('profile/', views.consumer_profile,name='consumer_profile'),
    path('edit-profile/<int:id>/',views.consumer_profile_edit,name='consumer_profile_edit'),
    path('faq/', views.faq,name='faq'),
    path('pricing/', views.pricing,name='upgrade'),
    path('latest/', views.consumer_latest_feed,name='consumer_latest_feed'),
    path('artists/',views.artists_list,name='artists_list'),
    path('category-view/<int:id>/',views.category_view,name='category_view'),
    path('podcasters/<int:id>/', views.single_artist,name='single_artist'),
    path('single-podcast/<int:id>/',views.single_podcast,name='single_podcast'),
    path('single-episode/<int:id>/', views.single_episode,name='single_episode'),
    path('current-music/<int:id>/',views.current_music_data,name='current_music'),
    path('next/<int:id>/',views.next_music_data,name='nextsong'),
    path('previous/<int:id>/', views.previous_music_data,name='previousmusic'),
    path('playlist-items/', views.consumer_playlist_data,name='consumer_playlist_data'),
    path('add-liked/<int:id>/',views.add_liked,name='add_liked'),
    path('add-playlist/<int:id>/',views.add_playlist,name='add_playlist'),
    
    path('playlist/',views.manage_playlist,name='manage_playlist'),
    path('create-playlist/', views.create_playlist,name='create_playlist'),
    path('delete-playlist/<int:id>/', views.delete_playlist,name='delete_playlist'),
    path('manage-playlist-content/<int:id>/',views.manage_playlist_content,name='manage_playlist_content'),
    path('remove-playlist-item/<int:id>/', views.remove_playlist_content,name='remove_playlist_content'),
    path('follow/<int:id>/', views.follow_podcaster,name='follow_podcaster'),
    path('follow-show/<int:id>/', views.follow_show,name='follow_show'),
    path('followed-shows/', views.followed_podcast_list,name='followed_shows'),
    path('followed-artists/', views.followed_artists_list,name='followed_artists'),
    
]