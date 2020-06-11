from django.db import models

# Create your models here.


from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
	print("****")
	print("Hi i'm in the user model")
	pass

class Profile(models.Model):
	pass