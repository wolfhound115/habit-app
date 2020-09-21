from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile, ProfileFollow

admin.site.register(User, UserAdmin)
admin.site.register(Profile)
admin.site.register(ProfileFollow)