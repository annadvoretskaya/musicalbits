from django.contrib.auth.models import AbstractUser
from django.db import models


class ApplicationUser(AbstractUser):
    pass


class Audio(models.Model):
    artist = models.CharField(max_length=100, blank=True, null=True, default=True)
    title = models.CharField(max_length=100, blank=True, null=True, default=True)
    url = models.URLField(max_length=1000)
    path = models.CharField(max_length=1000, blank=True, null=True, default=True)
    expires = models.DateField(blank=True, null=True, default=None)
    added_at = models.DateField(auto_now_add=True)
    user = models.ForeignKey(ApplicationUser, null=True, blank=True, default=None, related_name='audio')