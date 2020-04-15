from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.conf import settings

from taggit.managers import TaggableManager

from PIL import Image

from .managers import PostManager, CommentManager


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
    # Custom Manager
    posts = PostManager()

    def __str__(self):
        return f'{self.name}-{self.user.username}-{self.created}'

    @property
    def image_url(self):
        if self.image:
            return self.image.url
        return '#'

    def get_like_url(self):
        return reverse('posts:post_like', args=[self.pk])

    def get_absolute_url(self):
        return reverse('posts:post_detail', args=[self.pk])

    @property
    def get_likes_count(self):
        return self.likes.count()

    @property
    def tags_to_str(self):
        tags = [tag.name for tag in self.tags.all()]
        return ', '.join(tags)

    def save(self, *args, **kwargs):
        """ Resizing an image """
        super(Post, self).save(*args, **kwargs)

        if self.image:
            img = Image.open(self.image.path)

            if img.height > 500 or img.width > 500:
                output_size = (500, 500)
                img.thumbnail(output_size)
                img.save(self.image.path)

    class Meta:
        verbose_name = 'post'
        verbose_name_plural = 'posts'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    body = models.TextField()
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)

    # Default Manager
    objects = models.Manager()
    # Custom Manager
    comments = CommentManager()

    def __str__(self):
        return f'{str(self.post)} commented by {self.user.username}'

    class Meta:
        verbose_name = 'comment'
        verbose_name_plural = 'comments'
