from django.apps import AppConfig


class CourseConfig(AppConfig):
    name = "course"
    verbose_name = "Course"

    def ready(self):
        # Implicitly connect signal handlers decorated with @receiver.
        from . import signals
