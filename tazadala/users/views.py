# users/views.py
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework import generics, viewsets

from .admin import User
from .models import CustomUser
from .serializers import UserSerializer
import logging

logger = logging.getLogger(__name__)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Complaint
from .serializers import ComplaintSerializer

@api_view(['GET'])
def get_user_profile(request):
    """Получает профиль текущего пользователя."""
    user = request.user
    if user.is_authenticated:
        serializer = UserSerializer(user)
        return Response(serializer.data)  # Возвращаем сериализованные данные пользователя
    else:
        return Response({'detail': 'Неавторизованный доступ'}, status=status.HTTP_401_UNAUTHORIZED)  # Ошибка доступа

class ComplaintDetail(UpdateAPIView):
    """Предоставляет функционал для обновления состояния жалобы."""
    queryset = Complaint.objects.all()
    serializer_class = ComplaintSerializer
    permission_classes = []  # Доступ без ограничений

    def patch(self, request, *args, **kwargs):
        """Обрабатывает PATCH-запрос для частичного обновления жалобы."""
        return self.partial_update(request, *args, **kwargs)

class ComplaintCreateView(generics.CreateAPIView):
    """Создание новой жалобы с привязкой к текущему пользователю."""
    serializer_class = ComplaintSerializer
    permission_classes = [IsAuthenticated]  # Доступ только для авторизованных пользователей

    def perform_create(self, serializer):
        """Сохраняет новую жалобу с информацией о пользователе и местоположении."""
        location = self.request.data.get('location')  # Получаем местоположение из запроса
        image = self.request.FILES.get('image')  # Получаем изображение, если оно есть
        if location:
            serializer.save(user=self.request.user, location=location, image=image)  # Сохраняем жалобу с местоположением
        else:
            serializer.save(user=self.request.user, location="Location not provided")  # Если местоположение не указано

class ComplaintListView(generics.ListAPIView):
    """Предоставляет список всех жалоб."""
    queryset = Complaint.objects.all()
    serializer_class = ComplaintSerializer
    permission_classes = [AllowAny]  # Доступ для всех

    def get_queryset(self):
        """Возвращает список всех жалоб и логирует запрос."""
        print("GET запрос на /api/users/complaints/")
        return super().get_queryset()

class ComplaintDeleteView(generics.DestroyAPIView):
    """Удаление жалобы по ID."""
    queryset = Complaint.objects.all()
    serializer_class = ComplaintSerializer
    permission_classes = [IsAuthenticated]  # Доступ только для авторизованных пользователей

class UserComplaintListView(ListAPIView):
    """Предоставляет список жалоб текущего пользователя."""
    serializer_class = ComplaintSerializer
    permission_classes = [IsAuthenticated]  # Доступ только для авторизованных пользователей

    def get_queryset(self):
        """Возвращает только жалобы текущего пользователя."""
        return Complaint.objects.filter(user=self.request.user)

class RegisterView(generics.CreateAPIView):
    """Регистрация нового пользователя."""
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]  # Доступ для всех

class UserLoginView(APIView):
    """Аутентификация пользователя и получение токена доступа."""
    permission_classes = [AllowAny]  # Доступ для всех

    def post(self, request, *args, **kwargs):
        """Обрабатывает POST-запрос для входа пользователя."""
        email = request.data.get('email')  # Получаем email из запроса
        password = request.data.get('password')  # Получаем пароль из запроса

        try:
            user = CustomUser.objects.get(email=email)  # Ищем пользователя по email
            if user.check_password(password):  # Проверяем правильность пароля
                token, _ = Token.objects.get_or_create(user=user)  # Получаем или создаем токен для пользователя
                return Response({'token': token.key}, status=status.HTTP_200_OK)  # Возвращаем токен
            else:
                return Response({'detail': 'Неверный пароль'}, status=status.HTTP_400_BAD_REQUEST)  # Неверный пароль
        except CustomUser.DoesNotExist:
            return Response({'detail': 'Пользователь не найден'}, status=status.HTTP_400_BAD_REQUEST)  # Пользователь не найден

class ComplaintViewSet(viewsets.ModelViewSet):
    """Предоставляет набор действий для управления жалобами."""
    queryset = Complaint.objects.all()
    serializer_class = ComplaintSerializer

    def partial_update(self, request, *args, **kwargs):
        """Частичное обновление существующей жалобы."""
        instance = self.get_object()  # Получаем объект жалобы по ID
        serializer = self.get_serializer(instance, data=request.data, partial=True)  # Сериализуем данные запроса
        if serializer.is_valid():
            serializer.save()  # Сохраняем изменения
            return Response(serializer.data)  # Возвращаем сериализованные данные
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Ошибка валидации
