from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from django.urls import reverse

from ..views import register


class RegisterTest(TestCase):
    def setUp(self):
        pass

    def test_register_valid_data(self):
        pass

    def test_register_wrong_passwords(self):
        pass

    def test_register_existed_username(self):
        pass


class LoginTest(TestCase):
    def setUp(self):
        pass

    def test_valid_credentials(self):
        pass

    def test_invalid_credentials(self):
        pass
