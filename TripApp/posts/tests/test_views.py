from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from django.urls import reverse

from ..models import Post, Comment


class PostsListTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='test',
                                             password='testpassword')
        number_of_posts = 8

        for i in range(number_of_posts):
            Post.objects.create(name=f'Post {i}', user=self.user, about='...',
                                location='Test Location')

    def test_redirect_if_not_logged_in(self):
        response = self.client.get('/posts/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/users/login/?next=/posts/')

    def test_view_url_exits_at_desired_location(self):
        login = self.client.login(username='test', password='testpassword')
        response = self.client.get('/posts/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        login = self.client.login(username='test', password='testpassword')
        response = self.client.get(reverse('posts:posts_list'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        login = self.client.login(username='test', password='testpassword')
        response = self.client.get(reverse('posts:posts_list'))
        self.assertTemplateUsed(response, 'posts/posts_list.html')

    def test_pagination_is_five(self):
        login = self.client.login(username='test', password='testpassword')
        response = self.client.get(reverse('posts:posts_list'))
        self.assertTrue(len(response.context['posts']) == 5)


class PostDetailTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.post = Post.objects.create(name='post', user=self.user, about='...',
                                        location='test location')

    def test_redirect_if_not_logged_in(self):
        response = self.client.get('/posts/1/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/users/login/?next=/posts/1/')

    def test_view_url_exists_at_desired_location(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(f'/posts/{self.post.pk}/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('posts:post_detail', args=[self.post.pk]))
        self.assertEqual(response.status_code, 200)

    def test_get_all_comments(self):
        self.client.login(username='testuser', password='password')
        num_of_comments = 5
        for i in range(num_of_comments):
            comment = Comment.objects.create(post=self.post, user=self.user,
                                             body=f'comment {i}')

        response = self.client.get(reverse('posts:post_detail', args=[self.post.pk]))
        self.assertTrue(len(response.context['comments']) == 5)

    def test_add_comment(self):
        comments_count = Comment.objects.filter(post=self.post).count()

        self.client.login(username='testuser', password='password')
        self.client.post(reverse('posts:post_detail', args=[self.post.pk]), {'body': 'test_comment'})

        new_comment_count = Comment.objects.filter(post=self.post).count()
        self.assertEqual(new_comment_count, comments_count + 1)
        last_comment = Comment.objects.filter(post=self.post).order_by('-created')[0]
        self.assertEqual(last_comment.body, 'test_comment')
