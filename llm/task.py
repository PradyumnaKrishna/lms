import json

from huey.contrib.djhuey import db_task

from llm import get_llm

from .agents.topics import TopicModelling
from .documents.loader import load_document, preprocess


@db_task()
def extract_topics(resource):

    if not resource.attachment:
        return
    
    resource.under_process = True
    resource.save()

    docs = load_document(resource.attachment.file.path)
    docs = [preprocess(doc) for doc in docs]

    llm = get_llm()
    agent = TopicModelling(llm)
    topics = agent.run(docs).topics

    resource.topics = json.dumps(topics)
    resource.under_process = False
    resource.save()
