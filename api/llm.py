from functools import lru_cache

from django.apps import apps
from langchain_core.language_models import BaseLLM

from api.apps import APIConfig


@lru_cache
def get_llm() -> BaseLLM:
    return apps.get_app_config(APIConfig.name).llm
