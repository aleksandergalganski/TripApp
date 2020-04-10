from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'users'

urlpatterns = [
    path('', views.users_list, name='users_list'),
    path('/<str:username>/', views.user_detail, name='user_detail'),
    path('edit/', views.edit_profile, name='edit_user'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logged-out.html'), name='logout'),
    path('register/', views.register, name='register'),
    path('password_change/',
         auth_views.PasswordChangeView.as_view(template_name='registration/password-change-form.html'),
         name='password_change'),
    path('password_change/done/',
         auth_views.PasswordChangeDoneView.as_view(template_name='registration/password-change-done.html'),
         name='password_change_done'),
    path('password_reset/',
         auth_views.PasswordResetView.as_view(template_name='registration/password-reset-form.html'),
         name='password_reset'),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='registration/password-reset-done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='registration/password-reset-confirm.html'),
         name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='registration/password-reset-complete.html'),
         name='password_reset_complete'),
]
