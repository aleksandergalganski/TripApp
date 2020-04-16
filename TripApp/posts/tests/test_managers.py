from django.test import TestCase
from django.contrib.auth.models import User

from ..models import Post, Comment


class PostManagerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='usertest', password='password')

    def test_active(self):
        num_of_users = 6
        for i in range(num_of_users):
            status = True if i % 2 == 0 else False
            Post.objects.create(name='post', user=self.user, about='...',
                                location='location', active=status)

        self.assertEqual(Post.posts.actives().count(), 3)

    def test_get_users_post(self):
        num_of_posts = 3
        for i in range(num_of_posts):
            Post.objects.create(name='post', user=self.user, about='...',
                                location='test location')
        self.assertEqual(Post.posts.get_users_posts('usertest').count(), 3)

    def test_get_posts_by_location(self):
        locations = ('Kolobrzeg', 'Kolobrzeg', 'Gdansk')
        num_of_posts = 3
        for i in range(num_of_posts):
            Post.objects.create(name='post', user=self.user, about='...',
                                location=locations[i])
        self.assertEqual(Post.posts.get_posts_by_location('Kolobrzeg').count(), 2)


class CommentManagerTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='usertest', password='password')
        self.user2 = User.objects.create_user(username='usertest2', password='password')
        self.post = Post.objects.create(name='post', user=self.user1, about='...',
                                        location='location')

    def test_get_users_comments(self):
        num_of_comments = 3
        for i in range(num_of_comments):
            Comment.objects.create(user=self.user1, post=self.post, body='...')

        for i in range(num_of_comments):
            Comment.objects.create(user=self.user2, post=self.post, body='...')

        self.assertEqual(Comment.comments.get_users_comments('usertest').count(), 3)

