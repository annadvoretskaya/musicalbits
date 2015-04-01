from django.contrib import admin

# Register your models here.
from main.models import ApplicationUser, Audio

admin.site.register(ApplicationUser)
admin.site.register(Audio)
