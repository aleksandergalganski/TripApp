from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from ..models import Profile
from posts.models import Post


class RegisterTest(TestCase):

    def test_register_valid_data(self):
        data = {
            'username': 'JohnTheUser',
            'firstName': 'John',
            'email': 'test@email.com',
            'password': 'validpass',
            'password2': 'validpass'
        }
        self.client.post('/users/register/', data)
        users_count = User.objects.count()
        profiles_count = Profile.objects.count()
        self.assertEqual(users_count, 1)
        self.assertEqual(profiles_count, 1)

    def test_register_wrong_passwords(self):
        data = {
            'username': 'JohnTheUser',
            'firstName': 'John',
            'email': 'test@email.com',
            'password': 'validpass',
            'password2': 'validpass12'
        }
        self.client.post('/users/register/', data)
        users_count = User.objects.count()
        profiles_count = Profile.objects.count()
        self.assertEqual(users_count, 0)
        self.assertEqual(profiles_count, 0)

    def test_register_existed_username(self):
        User.objects.create_user(username='user', password='password')
        data = {
            'username': 'user',
            'firstName': 'John',
            'email': 'test@email.com',
            'password': 'validpass',
            'password2': 'validpass'
        }
        self.client.post('/users/register/', data)
        users_count = User.objects.count()
        profiles_count = Profile.objects.count()
        self.assertEqual(users_count, 1)
        self.assertEqual(profiles_count, 0)


class LoginTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_valid_credentials(self):
        credentials = {'username': 'testuser', 'password': 'testpassword'}
        response = self.client.post('/users/login/', credentials)
        self.assertRedirects(response, '/posts/')

    def test_invalid_credentials(self):
        invalid_credentials = {'username': 'testuser', 'password': 'wrongpassword'}
        response = self.client.post('/users/login/', invalid_credentials)
        self.assertRedirects(response, '/users/login/')


class UsersListTest(TestCase):
    def setUp(self):
        User.objects.create_user(username='test', password='testpassword')
        num_of_users = 8

        for i in range(num_of_users):
            User.objects.create_user(username=f'user {i}', password='testpassword')

        self.client.login(username='test', password='testpassword')

    def test_view_url_exits_at_desired_location(self):
        response = self.client.get('/users/list/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('users:users_list'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('users:users_list'))
        self.assertTemplateUsed(response, 'users/users_list.html')

    def test_pagination_is_five(self):
        response = self.client.get(reverse('users:users_list'))
        self.assertTrue(len(response.context['users']) == 5)


class UserDetailTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='password')
        self.profile = Profile.objects.create(user=self.user)
        self.client.login(username='test', password='password')

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(f'/users/detail/{self.user.pk}/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('users:user_detail', kwargs={'user_id': self.user.pk}))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(f'/users/detail/{self.user.pk}/')
        self.assertTemplateUsed(response, 'users/user_detail.html')


class UserEditTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='user1')
        self.profile1 = Profile.objects.create(user=self.user1)
        self.user2 = User.objects.create_user(username='user2', password='user2')
        self.profile2 = Profile.objects.create(user=self.user2)

    def test_authorized_user(self):
        self.client.login(username='user1', password='user1')
        response = self.client.get(reverse('users:edit_user', kwargs={'user_id': self.user1.pk}))
        self.assertEqual(response.status_code, 200)

    def test_unauthorized_user(self):
        self.client.login(username='user2', password='user2')
        response = self.client.get(reverse('users:edit_user', kwargs={'user_id': self.user1.pk}))
        self.assertEqual(response.status_code, 403)

    def test_edit_profile(self):
        self.client.login(username='user1', password='user1')
        data = {
            'first_name': 'name',
            'email': 'email@email.com',
            'bio': 'bio',
            'location': 'location'
        }
        user_id = self.user1.pk
        response = self.client.post(reverse('users:edit_user', args=[user_id]), data)
        user = User.objects.get(pk=user_id)

        self.assertRedirects(response, reverse('users:user_detail', args=[user_id]))
        self.assertEqual(user.first_name, 'name')
        self.assertEqual(user.email, 'email@email.com')
        self.assertEqual(user.profile.bio, 'bio')
        self.assertEqual(user.profile.location, 'location')


class UserDeleteTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='userdel', password='password')
        self.profile = Profile.objects.create(user=self.user)

    def test_authorized_user(self):
        self.client.login(username='userdel', password='password')
        response = self.client.get(reverse('users:delete_user', args=[self.user.pk]))
        self.assertEqual(response.status_code, 200)

    def test_unauthorized_user(self):
        user2 = User.objects.create_user(username='user2', password='password')
        self.client.login(username='user2', password='password')
        response = self.client.get(reverse('users:delete_user', args=[self.user.pk]))
        self.assertEqual(response.status_code, 403)

    def test_delete_user(self):
        users_count = User.objects.count()
        profiles_count = Profile.objects.count()

        self.client.login(username='userdel', password='password')
        response = self.client.post(reverse('users:delete_user', args=[self.user.pk]))

        self.assertRedirects(response, reverse('posts:home'))
        new_users_count = User.objects.count()
        new_profiles_count = Profile.objects.count()
        self.assertEqual(users_count - 1, new_users_count)
        self.assertEqual(profiles_count - 1, new_profiles_count)



