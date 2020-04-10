from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'users'

urlpatterns = [
    path('', views.users_list, name='users_list'),
    path('detail/<str:username>/', views.user_detail, name='user_detail'),
    path('edit/', views.edit_profile, name='edit_user'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
]
