# users/urls.py
from django.urls import path
from .views import RegisterView, ComplaintCreateView, ComplaintListView, ComplaintDeleteView, ComplaintDetail
from .views import UserLoginView, UserComplaintListView
from .views import get_user_profile

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),  # Регистрация нового пользователя
    path('login/', UserLoginView.as_view(), name='login'),  # Вход пользователя
    path('complaints/', ComplaintListView.as_view(), name='complaint-list'),  # Список всех жалоб
    path('complaints/create/', ComplaintCreateView.as_view(), name='complaint-create'),  # Создание новой жалобы
    path('me/', get_user_profile, name='user-profile'),  # Получение профиля текущего пользователя
    path('me/complaints/', UserComplaintListView.as_view(), name='user-complaints'),  # Список жалоб текущего пользователя
    path('complaints/<int:pk>/', ComplaintDeleteView.as_view(), name='complaint-delete'),  # Удаление жалобы по её ID
    path('complaints/<int:pk>/change/', ComplaintDetail.as_view(), name='complaint-detail'),  # Изменение статуса жалобы по её ID
]
