from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)  # Make email unique
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.username
