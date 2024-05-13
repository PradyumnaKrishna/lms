from functools import lru_cache

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from langchain_core.embeddings import Embeddings
from langchain_core.vectorstores import VectorStore
from langchain_community.embeddings.huggingface import HuggingFaceInferenceAPIEmbeddings, HuggingFaceEmbeddings
from langchain_community.vectorstores.chroma import Chroma


def setup_embedding(conf: dict) -> Embeddings:
    model_name = conf.get("model", "BAAI/bge-base-en-v1.5")

    embedding_type = conf.get("type", None)
    if embedding_type == "huggingface" or embedding_type is None:
        return HuggingFaceEmbeddings(model_name=model_name)

    elif embedding_type == "huggingface_inference_api":
        api_key = conf.get("api_key", "")
        api_url = conf.get("api_url", None)

        return HuggingFaceInferenceAPIEmbeddings(
            api_key=api_key,
            api_url=api_url,
            model_name=model_name,
        )

    raise ImproperlyConfigured("Invalid embedding configuration.")


@lru_cache
def get_vectorstore() -> VectorStore:
    conf = settings.VECTORSTORE
    if conf is None:
        raise ImproperlyConfigured("VECTORSTORE not configured")

    embedding_function = setup_embedding(conf.get("embedding", {}))

    store = conf.get("store", None)
    if store == "chroma":
        persist_directory = conf.get("persist_directory", None)

        return Chroma(
            embedding_function=embedding_function,
            persist_directory=persist_directory,
        )
        
    raise ImproperlyConfigured("VECTORSTORE 'type' not configured or not supported")
