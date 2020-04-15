from django.db import models


class ProfileQuerySet(models.QuerySet):
    def get_users_by_location(self, location):
        return self.filter(location__contains=location)


class ProfileManager(models.Manager):
    def get_queryset(self):
        return ProfileQuerySet(self.model, using=self._db)

    def get_users_by_location(self, location):
        return self.get_queryset().get_users_by_location(location)
