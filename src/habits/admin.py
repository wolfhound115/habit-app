from django.contrib import admin

# Register your models here.
from .models import HabitPost, HabitTrack, HabitEvent

admin.site.register(HabitPost)
admin.site.register(HabitTrack)
admin.site.register(HabitEvent)