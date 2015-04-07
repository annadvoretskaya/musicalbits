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

    @property
    def name(self):
        return '%s - %s' % (self.artist, self.title)

    def __unicode__(self):
        return self.name

class Playlist(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True, default=True)
    user = models.ForeignKey(ApplicationUser, null=True, blank=True, default=None, related_name='playlist')
    audio = models.ManyToManyField(Audio, null=True, blank=True, default=None)

    def __unicode__(self):
        return self.name

class Like(models.Model):
    user = models.ForeignKey(ApplicationUser, related_name='likes')
    playlist = models.ForeignKey(Playlist, related_name='likes')


class Tag(models.Model):
    name = models.CharField(max_length=200)
    audio = models.ForeignKey(Audio, null=True, blank=True, default=True, related_name='tags')


class Genre(models.Model):
    name = models.CharField(max_length=50)
    audio = models.ForeignKey(Audio, null=True, blank=True, default=True, related_name='genres')

