# complaints/urls.py
from django.urls import path
from .views import ComplaintCreateView, ComplaintListView, ComplaintDeleteView, ComplaintDetail, UserComplaintListView

urlpatterns = [
    path('create/', ComplaintCreateView.as_view(), name='complaint-create'),  # Создание новой жалобы
    path('', ComplaintListView.as_view(), name='complaint-list'),  # Список всех жалоб
    path('<int:pk>/', ComplaintDeleteView.as_view(), name='complaint-delete'),  # Удаление жалобы по её ID
    path('<int:pk>/change/', ComplaintDetail.as_view(), name='complaint-detail'),  # Изменение статуса жалобы по её ID
    path('me/', UserComplaintListView.as_view(), name='user-complaints'),  # Список жалоб текущего пользователя
]
