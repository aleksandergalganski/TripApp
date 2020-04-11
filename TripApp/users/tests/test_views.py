from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from ..models import Profile


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

