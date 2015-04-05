from django.contrib import admin

# Register your models here.
from main.models import ApplicationUser, Audio, Playlist, Like, Teg, Genre

admin.site.register(ApplicationUser)
admin.site.register(Audio)
admin.site.register(Playlist)
admin.site.register(Like)
admin.site.register(Teg)
admin.site.register(Genre)

