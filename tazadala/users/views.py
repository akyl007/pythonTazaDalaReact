# users/views.py
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from rest_framework.authtoken.models import Token
from rest_framework import generics

from .models import CustomUser
from .serializers import UserSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .utils import logger

@api_view(['GET'])
def get_user_profile(request):
    """Получает профиль текущего пользователя."""
    user = request.user
    if user.is_authenticated:
        serializer = UserSerializer(user)
        return Response(serializer.data)  # Возвращаем сериализованные данные пользователя
    else:
        return Response({'detail': 'Неавторизованный доступ'}, status=status.HTTP_401_UNAUTHORIZED)  # Ошибка доступа


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

