from django.db import models


class PostQuerySet(models.QuerySet):
    def get_users_posts(self, username):
        return self.filter(user__username=username)

    def actives(self):
        return self.filter(active=True)


class PostManager(models.Manager):
    def get_queryset(self):
        return PostQuerySet(self.model, using=self._db)

    def get_users_posts(self, username):
        return self.get_queryset().get_users_posts(username)

    def actives(self):
        return self.get_queryset().actives()


class CommentQuerySet(models.QuerySet):
    def get_users_comments(self, username):
        return self.filter(user__username=username)


class CommentManager(models.Manager):
    def get_queryset(self):
        return CommentQuerySet(self.model, using=self._db)

    def get_users_comments(self, username):
        return self.get_queryset().get_users_comments(username)
