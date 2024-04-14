from django.urls import path
from api.views import NotificationView


urlpatterns = [
    path('notification/', NotificationView.as_view(), name='notify'),
]
