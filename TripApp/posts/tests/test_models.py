from django.test import TestCase
from django.contrib.auth.models import User

from ..models import Post


class ActivePostsManagerTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='test', password='testpassword')
        Post.objects.create(name='test_post', user=self.user, about='...',
                            location='Kolobrzeg', active=False)
        Post.objects.create(name='test_post', user=self.user, about='...',
                            location='Kolobrzeg', active=True)
        Post.objects.create(name='test_post', user=self.user, about='...',
                            location='Kolobrzeg', active=True)

    def should_return_two_posts(self):
        posts = Post.actives()
        self.assertEquals(1, len(posts))


class PostModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='test',
                                             password='testpassword')
        self.post = Post.objects.create(name='test_post', user=self.user, about='...',
                                        location='Kolobrzeg')

    def test_str_method(self):
        self.assertEquals(str(self.post), f'test_post-test-{self.post.created}')

    def test_get_absolute_url_method(self):
        self.assertEquals(self.post.get_absolute_url(), f'/posts/{self.post.id}/')

    def test_get_likes_count(self):
        pass
        # todo
