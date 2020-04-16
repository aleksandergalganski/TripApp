from django.test import TestCase
from django.contrib.auth.models import User

from ..models import Profile
from posts.models import Post


class ProfileModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test',
                                             email='test@email.com',
                                             password='valid_password')
        self.profile = Profile.objects.create(user=self.user)
        self.profile.save()

    def test_str_method(self):
        self.assertEquals(str(self.profile), 'Profile for user test')

    def test_get_absolute_url_method(self):
        self.assertEquals(self.profile.get_absolute_url(), f'/users/detail/{self.user.pk}/')

    def test_get_posts_count(self):
        posts_count = 2

        for i in range(posts_count):
            Post.objects.create(name=f'Post {i}', user=self.user, about='...',
                                location='Test Location')

        self.assertEqual(self.profile.get_posts_count, 2)

    def test_get_total_likes_count(self):
        likes_count = 5
        post1 = Post.objects.create(name='post2', user=self.user, about='...',
                                    location='test location')
        post2 = Post.objects.create(name='post2', user=self.user, about='...',
                                    location='test location')

        for i in range(likes_count):
            user = User.objects.create_user(username=f'username{i}', password='password')
            post1.likes.add(user)
            post2.likes.add(user)

        self.assertEqual(self.profile.get_total_likes_count, 10)