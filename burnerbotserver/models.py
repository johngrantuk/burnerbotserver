from django.conf import settings
from django.db import models
from django.utils import timezone


class UserDetail(models.Model):
    added = models.DateTimeField(default=timezone.now)
    username = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    private_key = models.CharField(max_length=200)
    hash = models.CharField(max_length=200)

    def __str__(self):
        return self.username
