from functools import lru_cache

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from langchain_community.llms.ollama import Ollama
from langchain_core.language_models import BaseLLM
from langchain_google_genai import ChatGoogleGenerativeAI


@lru_cache
def get_llm() -> BaseLLM:
    model = settings.LLM.get("model")
    if model is None:
        raise ImproperlyConfigured("LLM model not configured")

    if model == "gemini-pro":
        key = settings.LLM.get("key")
        if key is None:
            raise ImproperlyConfigured(f"LLM 'key' not configured for the model '{model}'")

        return ChatGoogleGenerativeAI(model=model, google_api_key=key)

    if model == "ollama":
        model_type = settings.LLM.get("type")
        if model_type is None:
            raise ImproperlyConfigured(f"LLM 'type' not configured for the model '{model}'")

        config = settings.LLM.get("config", {})

        return Ollama(model=model_type, **config)

    raise ImproperlyConfigured(f"LLM model '{model}' not supported")
