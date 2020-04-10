from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.conf import settings

from taggit.managers import TaggableManager

from PIL import Image


class ActivePostsManager(models.Manager):
    def get_queryset(self):
        return super(ActivePostsManager, self).get_queryset().filter(active=True)


class Post(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name='posts')
    about = models.TextField()
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='post_images/%Y/%m/%d/', null=True, blank=True)
    tags = TaggableManager()
    location = models.CharField(max_length=100)
    active = models.BooleanField(default=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                   related_name='posts_likes')
    # Default Manager
    objects = models.Manager()
    # Custom Manager for active posts
    actives = ActivePostsManager()

    def __str__(self):
        return f'{self.name}-{self.user.username}-{self.created}'

    def get_like_url(self):
        return reverse('posts:post_like', args=[self.pk])

    def get_absolute_url(self):
        return reverse('posts:post_detail', args=[self.id])

    @property
    def get_likes_count(self):
        return self.likes.count()

    def save(self, *args, **kwargs):
        """ Resizing an image """
        super(Post, self).save(*args, **kwargs)

        if self.image:
            img = Image.open(self.image.path)

            if img.height > 500 or img.width > 500:
                output_size = (500, 500)
                img.thumbnail(output_size)
                img.save(self.image.path)