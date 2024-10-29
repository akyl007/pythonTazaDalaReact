from datetime import timedelta

from django.db import models
from django.utils import timezone
from users.models import CustomUser


class Category(models.Model):
    name = models.CharField(max_length=100)
    days_to_complete = models.PositiveIntegerField()  # Число дней для выполнения

    def __str__(self):
        return self.name
class Complaint(models.Model):
    STATUS_CHOICES = [
        ('На проверке', 'Submitted'),
        ('В процессе', 'In Progress'),
        ('Исполнено', 'Done'),
        ('Отклонено', 'Cancelled')
    ]
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    description = models.TextField()
    location = models.CharField(max_length=255)  # Хранит название города и улицы
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='На проверке')
    image = models.ImageField(upload_to='complaint_images/', blank=True, null=True)  # Поле для изображения
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if self.category:  # Проверяем, что category не None
            self.due_date = timezone.now() + timezone.timedelta(days=self.category.days_to_complete)
        super().save(*args, **kwargs)

