from django.apps import AppConfig

from llm import get_llm


class APIConfig(AppConfig):
    name = "api"
    verbose_name = "API"
    llm = get_llm()
