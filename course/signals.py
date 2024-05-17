import json

import markdown

from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from huey.contrib.djhuey import db_task

from llm.documents.loader import load_document
from llm.tasks import (
    delete_embeddings,
    extract_topics,
    store_embeddings,
    summarize_documents,
)

from .models import Resource


@receiver(post_save, sender=Resource)
def topics_modelling(sender, instance: Resource, created: bool, **kwargs):
    if created and instance.attachment:
        instance.under_process = True
        instance.save()
        process_resource(instance)


@receiver(post_delete, sender=Resource)
def delete_resource(sender, instance: Resource, **kwargs):
    if instance.attachment:
        if instance.vectorstore_ids:
            ids = json.loads(instance.vectorstore_ids)
            delete_embeddings(ids)


@db_task()
def process_resource(resource: Resource):

    data = resource.attachment.file.read()

    docs = load_document(data)
    vs_task = store_embeddings(
        docs,
        resource.get_parent().id,
        resource.id,
    )

    topics_task = extract_topics(docs)
    topics = topics_task.get(blocking=True)

    summary_task = summarize_documents(docs)
    summary = summary_task.get(blocking=True)
    vs_ids = vs_task.get(blocking=True)

    resource.topics = json.dumps(topics)
    resource.vectorstore_ids = json.dumps(vs_ids)
    resource.summary = markdown.markdown(summary)
    resource.under_process = False
    resource.save()
