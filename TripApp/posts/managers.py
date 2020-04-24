from django.db import models


class PostQuerySet(models.QuerySet):
    def get_users_posts(self, username):
        return self.filter(user__username=username).order_by('-created')

    def actives(self):
        return self.filter(active=True).order_by('-created')

    def get_posts_by_location(self, location):
        return self.filter(active=True).filter(location__contains=location).order_by('-created')

    def after(self, date):
        pass

    def before(self, date):
        pass


class PostManager(models.Manager):
    def get_queryset(self):
        return PostQuerySet(self.model, using=self._db)

    def get_users_posts(self, username):
        return self.get_queryset().get_users_posts(username)

    def actives(self):
        return self.get_queryset().actives()

    def get_posts_by_location(self, location):
        return self.get_queryset().get_posts_by_location(location)

    def after(self, date):
        pass

    def before(self, date):
        pass


class CommentQuerySet(models.QuerySet):
    def get_users_comments(self, username):
        return self.filter(user__username=username)


class CommentManager(models.Manager):
    def get_queryset(self):
        return CommentQuerySet(self.model, using=self._db)

    def get_users_comments(self, username):
        return self.get_queryset().get_users_comments(username)
