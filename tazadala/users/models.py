from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from .utils import CustomUserManager

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=11, unique=True, null=True)

    objects = CustomUserManager()

    def __str__(self):
        return self.email
