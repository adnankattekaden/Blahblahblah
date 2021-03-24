from django.urls import path
from . import views

urlpatterns = [
    path('', views.owner_login,name='owner_login'),
    path('logout/',views.owner_logout,name='owner_logout'),
    path('dashboard/', views.owner_dashboard,name='owner_dashboard'),
    path('manage-category/',views.manage_category,name='manage_category'),
    path('create-category/', views.create_category,name='create_category'),
    path('edit-category/<int:id>/',views.edit_category,name='edit_category'),
    path('delete-category/<int:id>/',views.delete_category,name='delete_category'),
    path('manage-plans/', views.manage_plans,name='manage_plans'),
    path('create-plans/', views.create_plan,name='create_plan'),
    path('delete-plan/<int:id>/', views.delete_plan,name='delete_plan'),
    path('manage-ads/', views.manage_ads,name='manage_ads'),
    path('create-ads/', views.create_ads,name='create_ads'),
    path('sales-report/', views.sales_report,name='sales_report'),
    path('cancelled-report/', views.cancelled_report,name='cancelled_report'),
    path('manage-listners/', views.manage_listners,name='manage_listners'),
    path('manage-creators/', views.manage_creators,name='manage_creators'),
    path('block-users/<int:id>/', views.block_users,name='block_users'),
    path('unblock-users/<int:id>/',views.unblock_users,name='unblock_users'),

    path('featured-shows/',views.manage_featured_shows,name='featured_shows'),
    path('add-featured-shows/',views.add_featured_shows,name='add_featured_shows'),
    path('remove-featured-show/<int:id>/',views.remove_featured_show,name='remove_featured_show'),

    path('manage-top-podcasters/', views.manage_top_podcasters,name='manage_top_podcasters'),
    path('add-top-podcasters/',views.add_top_podcasters,name='add_top_podcasters'),
    path('remove-top-podcasters/<int:id>/', views.remove_top_podcasters,name='remove_top_podcasters'),

    path('manage-trending/', views.manage_trending,name='manage_trending'),
    path('add-trending/', views.add_trending,name='add_trending'),
    path('remove-trending/<int:id>/', views.remove_trending,name='remove_trending'),
    
    path('manage-popular-shows/', views.manage_popular_shows,name='manage_popular_shows'),
    path('add-popular-shows/', views.add_popular_shows,name='add_popular_shows'),
    path('remove-popular-shows/<int:id>/',views.remove_popular_shows,name='remove_popular_shows'),
]
