from django.contrib import admin

from .models import Complaint, Category


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('id', 'description', 'status', 'created_at', 'due_date')  # Укажите нужные поля
    search_fields = ('description',)  # Поля для поиска

@admin.register(Category)  # Пример, если у вас есть модель Category
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')  # Замените 'name' на имя поля вашей модели
    search_fields = ('name',)
