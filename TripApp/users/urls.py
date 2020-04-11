from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('list/', views.users_list, name='users_list'),
    path('detail/<int:user_id>/', views.user_detail, name='user_detail'),
    path('edit/<int:user_id>', views.edit_profile, name='edit_user'),
    path('delete/<int:user_id>/', views.delete_profile, name='delete_profile'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
]
