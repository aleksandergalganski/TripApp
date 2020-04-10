from django.db import models
from django.conf import settings
from django.urls import reverse

from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='users/%Y/%m/%d', blank=True, null=True)
    bio = models.TextField(max_length=500)
    location = models.CharField(max_length=50)

    def __str__(self):
        return f'Profile for user {self.user.username}'

    def get_absolute_url(self):
        return reverse('users:user_detail', args=[self.user.username])

    def save(self, *args, **kwargs):
        """ Resizing an image """
        super(Profile, self).save(*args, **kwargs)

        if self.image:
            img = Image.open(self.image.path)

            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.image.path)

