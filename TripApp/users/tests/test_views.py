from django.test import TestCase
from django.contrib.auth.models import User

from ..models import Profile


class RegisterTest(TestCase):
    def setUp(self):
        pass

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
