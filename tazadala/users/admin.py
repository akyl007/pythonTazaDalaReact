from django.contrib.auth import get_user_model

User = get_user_model()

from django.contrib import admin
from .models import CustomUser  # Импортируйте свою модель пользователя

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email')  # Укажите нужные поля
    search_fields = ('username', 'email')  # Поля для поиска