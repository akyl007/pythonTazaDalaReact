from datetime import timedelta

from django.shortcuts import render
from django.utils import timezone

# complaints/views.py
from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Complaint
from .serializers import ComplaintSerializer



class ComplaintCreateView(CreateAPIView):
    """Создание новой жалобы с привязкой к текущему пользователю."""
    serializer_class = ComplaintSerializer
    permission_classes = [IsAuthenticated]

    def get_due_date(self, category_text):

        # Словарь с количеством дней для каждой категории
        category_days = {
            "1": 2,
            "2": 3,
            "3": 7,
        }
        days = category_days.get(category_text, 0)  # Получаем дни или 0 по умолчанию
        return timezone.now() + timedelta(days=days)

    def perform_create(self, serializer):

        location = self.request.data.get('location')
        image = self.request.FILES.get('image')

        category_text = self.request.data.get('category')
        due_date = self.get_due_date(category_text)


        serializer.save(user=self.request.user, location=location, image=image, due_date=due_date)

class ComplaintListView(ListAPIView):
    """Предоставляет список всех жалоб."""
    queryset = Complaint.objects.all()
    serializer_class = ComplaintSerializer
    permission_classes = [AllowAny]  # Доступ для всех

    def get_queryset(self):

        print("GET запрос на /api/users/complaints/")
        return super().get_queryset().order_by('-created_at')

class ComplaintDeleteView(DestroyAPIView):
    """Удаление жалобы по ID."""
    queryset = Complaint.objects.all()
    serializer_class = ComplaintSerializer
    permission_classes = [IsAuthenticated]  # Доступ только для авторизованных пользователей

class ComplaintDetail(UpdateAPIView):
    """Предоставляет функционал для обновления состояния жалобы."""
    queryset = Complaint.objects.all()
    serializer_class = ComplaintSerializer
    permission_classes = []  # Доступ без ограничений

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

class UserComplaintListView(ListAPIView):
    serializer_class = ComplaintSerializer
    permission_classes = [IsAuthenticated]  # Доступ только для авторизованных пользователей

    def get_queryset(self):
        return Complaint.objects.filter(user=self.request.user).order_by('-created_at')
