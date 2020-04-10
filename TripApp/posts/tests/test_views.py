from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from django.urls import reverse

from ..models import Post


class PostsListTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='test',
                                             password='testpassword')
        number_of_posts = 8

        for i in range(number_of_posts):
            Post.objects.create(name=f'Post {i}', user=self.user, about='...',
                                location='Test Location')
        login = self.client.login(username='test', password='testpassword')

    def test_view_url_exits_at_desired_location(self):
        response = self.client.get('/posts/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('posts:posts_list'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('posts:posts_list'))
        self.assertTemplateUsed(response, 'posts/posts_list.html')

    def test_pagination_is_five(self):
        response = self.client.get(reverse('posts:posts_list'))
        self.assertTrue(len(response.context['posts']) == 5)