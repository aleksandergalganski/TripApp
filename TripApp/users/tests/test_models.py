from django.test import TestCase
from django.contrib.auth.models import User

from ..models import Profile


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
        self.assertEquals(self.profile.get_absolute_url(), '/users/detail/test/')
