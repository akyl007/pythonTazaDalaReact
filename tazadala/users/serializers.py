# users/serializers.py
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import CustomUser, Complaint

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'password')  # Определяем поля для сериализации пользователя

    def create(self, validated_data):
        user = CustomUser(**validated_data)  # Создаём нового пользователя с переданными данными
        user.set_password(validated_data['password'])  # Хэшируем пароль перед сохранением
        user.save()  # Сохраняем пользователя в базе данных
        return user  # Возвращаем созданного пользователя


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', 'is_staff')  # Поля для сериализации с добавлением роли администратора

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])  # Хэшируем пароль
        return super().create(validated_data)  # Создаём пользователя с хэшированным паролем


class ComplaintSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # Возвращаем строковое представление пользователя (например, имя)

    class Meta:
        model = Complaint
        fields = ['id', 'description', 'location', 'status', 'created_at', 'image', 'user', 'user_id']  # Поля для сериализации жалобы

    def create(self, validated_data):
        return Complaint.objects.create(**validated_data)  # Создаём новую жалобу с переданными данными
