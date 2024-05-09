import json
import markdown

from django.db.models.signals import post_save
from django.dispatch import receiver

from huey.contrib.djhuey import db_task

from llm.documents.loader import load_document
from llm.tasks import extract_topics, summarize_documents

from .models import Resource


@receiver(post_save, sender=Resource)
def topics_modelling(sender, instance: Resource, created: bool, **kwargs):
    if created and instance.attachment:
        instance.under_process = True
        instance.save()
        process_resource(instance)


@db_task()
def process_resource(resource: Resource):

    docs = load_document(resource.attachment.file.path)

    topics_task = extract_topics(docs)
    topics = topics_task.get(blocking=True)

    summary_task = summarize_documents(docs)
    summary = summary_task.get(blocking=True)

    resource.topics = json.dumps(topics)
    resource.summary = markdown.markdown(summary)
    resource.under_process = False
    resource.save()
