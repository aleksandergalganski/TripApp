from django.db import models
from django.conf import settings
from django.urls import reverse

from PIL import Image

from .managers import ProfileManager


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='users/%Y/%m/%d', blank=True, null=True)
    bio = models.TextField(max_length=500)
    location = models.CharField(max_length=50)
    # Default Manager
    objects = models.Manager()
    # Custom Manager
    profiles = ProfileManager()

    def __str__(self):
        return f'Profile for user {self.user.username}'

    def get_absolute_url(self):
        return reverse('users:user_detail', args=[self.user.pk])

    @property
    def image_url(self):
        if self.image:
            return self.image.url
        return '#'

    @property
    def get_posts_count(self):
        return self.user.posts.all().count()

    @property
    def get_total_likes_count(self):
        likes_count = 0
        user_posts = self.user.posts.all()

        for post in user_posts:
            likes_count += post.likes.count()

        return likes_count

    def save(self, *args, **kwargs):
        """ Resizing an image """
        super(Profile, self).save(*args, **kwargs)

        if self.image:
            img = Image.open(self.image.path)

            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.image.path)

    class Meta:
        verbose_name = 'profile'
        verbose_name_plural = 'profiles'

