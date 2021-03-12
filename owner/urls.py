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

    
]
