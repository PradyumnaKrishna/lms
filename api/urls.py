from django.urls import path
from api.views import AnnouncementView


urlpatterns = [
    path('announcements/', AnnouncementView.as_view(), name='announcements_api'),
]
