from django.test import TestCase
from django.contrib.auth.models import User

from ..models import Post, Comment


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
        self.assertEqual(1, len(posts))


class PostModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='test',
                                             password='testpassword')
        self.post = Post.objects.create(name='test_post', user=self.user, about='...',
                                        location='Kolobrzeg')

    def test_str_method(self):
        self.assertEqual(str(self.post), f'test_post-test-{self.post.created}')

    def test_get_absolute_url_method(self):
        self.assertEqual(self.post.get_absolute_url, f'/posts/{self.post.id}/')

    def test_get_likes_count(self):
        pass
        # todo


class CommentModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test')
        self.post = Post.objects.create(name='testpost', user=self.user, about='...',
                                        location='Kolobrzeg')
        self.comment = Comment.objects.create(post=self.post, user=self.user, body='...')

    def test_str_method(self):
        self.assertEqual(str(self.comment), f'{str(self.post)} commented by test')
