from django.apps import AppConfig
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.llms.ollama import Ollama


class APIConfig(AppConfig):
    name = 'api'
    verbose_name = "API"

    def __init__(self, app_name, app_module):
        super().__init__(app_name, app_module)
        self.llm = None

    def ready(self):
        model = settings.LLM.get("model")
        if model is None:
            raise ImproperlyConfigured("LLM model not configured")
        
        if model == "gemini-pro":
            key = settings.LLM.get("key")
            if key is None:
                raise ImproperlyConfigured(f"LLM 'key' not configured for the model '{model}'")
            
            self.llm = ChatGoogleGenerativeAI(model=model, google_api_key=key)
            return

        if model == "ollama":
            model_type = settings.LLM.get("type")
            if model_type is None:
                raise ImproperlyConfigured(f"LLM 'type' not configured for the model '{model}'")
            
            config = settings.LLM.get("config", {})
            
            self.llm = Ollama(model=model_type, **config)
            return

        raise ImproperlyConfigured(f"LLM model '{model}' not supported")
