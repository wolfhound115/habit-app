from django.contrib import admin

# Register your models here.
from .models import HabitPost, HabitTrack

admin.site.register(HabitPost)
admin.site.register(HabitTrack)