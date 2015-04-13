from django.contrib import admin

# Register your models here.
from main.models import ApplicationUser, Audio, Playlist, Like, Tag, AudioConnection


class AudioAdmin(admin.ModelAdmin):
    list_display = ('artist', 'title', 'last_updated', 'deleted')
    list_filter = ('deleted', )
    search_fields = ('artist', 'title')

admin.site.register(ApplicationUser)
admin.site.register(Audio, AudioAdmin)
admin.site.register(Playlist)
admin.site.register(Like)
admin.site.register(Tag)
# admin.site.register(Genre)
admin.site.register(AudioConnection)

