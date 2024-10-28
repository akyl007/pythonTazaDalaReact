from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class CustomUserManager(UserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email должен быть указан')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    objects = CustomUserManager()  # Устанавливаем пользовательский менеджер

    def __str__(self):
        return self.email

class Complaint(models.Model):
    STATUS_CHOICES = [
        ('На проверке', 'Submitted'),
        ('В процессе', 'In Progress'),
        ('Решено', 'Resolved'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    description = models.TextField()
    location = models.CharField(max_length=255)  # Хранит название города и улицы
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='На проверке')
    image = models.ImageField(upload_to='complaint_images/', blank=True, null=True)  # Поле для изображения
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Complaint {self.id} by {self.user.email}"