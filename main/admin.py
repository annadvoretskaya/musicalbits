from django.contrib import admin

# Register your models here.
from main.models import ApplicationUser, Audio, Playlist, Like, Tag, Genre

admin.site.register(ApplicationUser)
admin.site.register(Audio)
admin.site.register(Playlist)
admin.site.register(Like)
admin.site.register(Tag)
admin.site.register(Genre)

