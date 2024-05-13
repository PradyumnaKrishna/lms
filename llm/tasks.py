from typing import List

from huey.contrib.djhuey import task

from langchain.docstore.document import Document
from langchain.chains.summarize import load_summarize_chain

from . import get_llm
from llm.agents.topics import TopicModelling
from llm.documents.loader import preprocess
from llm.documents.vectorstore import get_vectorstore


@task()
def extract_topics(docs: List[Document]) -> List[str]:
    docs = [preprocess(doc) for doc in docs]
    llm = get_llm()

    agent = TopicModelling(llm)
    return agent.run(docs).topics


@task()
def summarize_documents(docs: List[Document]) -> str:
    llm = get_llm()
    chain = load_summarize_chain(llm)

    return chain.run(docs)


@task()
def store_embeddings(docs: List[Document], course_id: int, resource_id: int) -> List[str]:
    store = get_vectorstore()

    for doc in docs:
        doc.metadata["course_id"] = course_id
        doc.metadata["resource_id"] = resource_id

    return store.add_documents(docs)


@task()
def delete_embeddings(ids: List[str]):
    store = get_vectorstore()
    store.delete(ids)
