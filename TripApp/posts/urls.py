from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.home, name='home'),
    path('posts/', views.posts_list, name='posts_list'),
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    path('posts/create/', views.create_post, name='create_post'),
    path('posts/<int:post_id>/update/', views.update_post, name='update_post'),
    path('posts/<int:post_id>/delete/', views.delete_post, name='delete_post'),
    path('posts/tags/<slug:slug>/', views.tagged_posts, name='tagged_posts'),
    path('posts/tags/', views.popular_tag_list, name='tag_list'),
    path('like/<int:post_id>/', views.post_like, name='post_like'),
    path('posts/comments/<int:comment_id>/update/', views.update_comment, name='update_comment'),
    path('posts/comments/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    path('posts/locations/', views.popular_location_list, name='location_list'),
]
