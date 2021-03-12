from django.urls import path
from . import views

urlpatterns = [
    path('', views.creator_login,name='creator_login'),
    path('logout/',views.creator_logout,name='creator_logout'),
    path('signup/', views.creator_signup,name='creator_signup'),
    path('dashboard/', views.creator_dashboard,name='creator_dashboard'),
    path('manage-podcasts/', views.manage_podcasts,name='manage_podcasts'),
    path('create-podcast/', views.create_podcast,name='create_podcast'),
    path('edit-podcast/<int:id>/', views.edit_podcast,name='edit_podcast'),
    path('delete-podcast/<int:id>/', views.delete_podcast,name='delete_podcast'),
    path('manage-episodes/<int:id>/',views.manage_episodes,name='manage_episodes'),
    path('create-episode/', views.create_episode,name='create_episode'),
    path('delete-episode/<int:id>/', views.delete_episode,name='delete_episode'),
    path('profile/', views.creator_profile,name='creator_profile'),
    path('edit-profiles/<int:id>', views.edit_profile,name='edit_profile'),
    path('edit/<int:id>/', views.edit_profiles,name='edit_profiles'),

]
