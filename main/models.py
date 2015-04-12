import datetime
from django.contrib.auth.models import AbstractUser
from django.db import models


class ApplicationUser(AbstractUser):
    audio = models.ManyToManyField("Audio")


class Audio(models.Model):
    artist = models.CharField(max_length=100, blank=True, null=True, default=None)
    title = models.CharField(max_length=100, blank=True, null=True, default=None)
    url = models.URLField(max_length=1000)
    path = models.CharField(max_length=1000, blank=True, null=True, default=True)
    expires = models.DateField(blank=True, null=True, default=None)
    added_at = models.DateField(auto_now_add=True)
    owner = models.ForeignKey(ApplicationUser, null=True, blank=True, default=None, related_name='tracks')
    deleted = models.BooleanField(default=False)
    last_updated = models.DateTimeField(auto_now=True, default=None)
    # download_date = models.DateTimeField(auto_now_add=True, blank=True)

    @property
    def name(self):
        return '%s - %s' % (self.artist, self.title)

    def __unicode__(self):
        return self.name


class Playlist(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True, default=None)
    user = models.ForeignKey(ApplicationUser, null=True, blank=True, default=None, related_name='playlist')
    audio = models.ManyToManyField(Audio, through='AudioConnection')

    def __unicode__(self):
        return self.name


class AudioConnection(models.Model):
    playlist = models.ForeignKey(Playlist)
    audio = models.ForeignKey(Audio)
    number = models.SmallIntegerField(default=0, blank=True, null=True)

    class Meta:
        ordering = ('number', )

    def __unicode__(self):
        return "%s %s %s" % (self.playlist, self.audio, self.number)


class Like(models.Model):
    user = models.ForeignKey(ApplicationUser, related_name='likes')
    playlist = models.ForeignKey(Playlist, related_name='likes')


class Tag(models.Model):
    name = models.CharField(max_length=200)
    audio = models.ForeignKey(Audio, null=True, blank=True, default=None, related_name='tags')


class Genre(models.Model):
    name = models.CharField(max_length=50)
    audio = models.ForeignKey(Audio, null=True, blank=True, default=None, related_name='genres')


class AudioRating(models.Model):
    user = models.ForeignKey(ApplicationUser)
    audio = models.ForeignKey(Audio, related_name='ratings')
    value = models.SmallIntegerField(default=0)

