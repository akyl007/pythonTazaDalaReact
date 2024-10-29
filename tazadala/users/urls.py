# users/urls.py
from django.urls import path, include
from .views import RegisterView, UserLoginView, get_user_profile

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),  # Регистрация нового пользователя
    path('login/', UserLoginView.as_view(), name='login'),  # Вход пользователя
    path('me/', get_user_profile, name='user-profile'),  # Получение профиля текущего пользователя
    path('complaints/', include('complaints.urls')),  # Включаем URL-адреса жалоб
]
