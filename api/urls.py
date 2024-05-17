from django.urls import path

from api.views import NotificationView, GeneratePaperView


urlpatterns = [
    path("notification/", NotificationView.as_view(), name="notify"),
    path("generate_paper/", GeneratePaperView.as_view(), name="generate_paper"),
]
