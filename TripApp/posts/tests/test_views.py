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


class CreatePostTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')

    def test_redirect_if_not_logged_in(self):
        response = self.client.get('/posts/create/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/users/login/?next=/posts/create/')

    def test_view_url_exists_at_desired_location(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get('/posts/create/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('posts:create_post'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('posts:create_post'))
        self.assertTemplateUsed(response, 'posts/post_create.html')

    @staticmethod
    def make_tags_list(tags_names):
        tags_list = [tag for tag in tags_names]
        return tags_list

    def test_create_post(self):
        posts_count = Post.objects.all().count()
        self.client.login(username='testuser', password='password')
        data = {
            'name': 'Post',
            'about': 'About post',
            'tags': 'tag1 tag2 tag3',
            'location': 'location'
        }
        self.client.post('/posts/create/', data)
        new_posts_count = Post.objects.all().count()
        self.assertEqual(new_posts_count, posts_count + 1)
        last_post = Post.objects.order_by('-created')[0]
        self.assertEqual(last_post.name, 'Post')
        self.assertEqual(last_post.about, 'About post')
        tags_list = self.make_tags_list(last_post.tags.names())
        self.assertListEqual(sorted(tags_list), sorted(['tag1', 'tag2', 'tag3']))
        self.assertEqual(last_post.location, 'location')


class UpdatePostTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.post = Post.objects.create(name='post', user=self.user, about='...',
                                        location='test location')

    def test_redirect_if_not_logged_in(self):
        response = self.client.get('/posts/1/update/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/users/login/?next=/posts/1/update/')

    def test_view_url_exists_at_desired_location(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(f'/posts/{self.post.pk}/update/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('posts:update_post', args=[self.post.pk]))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('posts:update_post', args=[self.post.pk]))
        self.assertTemplateUsed(response, 'posts/post_update.html')


class DeletePostTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.post = Post.objects.create(name='post', user=self.user, about='...',
                                        location='test location')

    def test_redirect_if_not_logged_in(self):
        response = self.client.get('/posts/1/delete/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/users/login/?next=/posts/1/delete/')

    def test_view_url_exists_at_desired_location(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(f'/posts/{self.post.pk}/delete/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('posts:delete_post', args=[self.post.pk]))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('posts:delete_post', args=[self.post.pk]))
        self.assertTemplateUsed(response, 'posts/post_delete_confirm.html')

