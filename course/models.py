import uuid
from django.db import models

from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, InlinePanel, TitleFieldPanel
from wagtail.documents.models import Document

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

from home.panels import TargetFieldPanel


class CoursePage(Page):
    description = RichTextField()
    code = models.CharField(max_length=255)
    credit = models.DecimalField(max_digits=3, decimal_places=0)
    topics = RichTextField()

    content_panels = [
        TitleFieldPanel("title", targets=[]),
        TargetFieldPanel('code', targets=["slug"]),
        FieldPanel('credit', classname="full"),
        FieldPanel('description', classname="full"),
        FieldPanel('topics', classname="full"),
        InlinePanel('announcements', label="Announcements"),
    ]

    parent_page_types = ['home.InstitutePage']
    subpage_types = ['course.Resource']


class Announcement(ClusterableModel):
    id = models.AutoField(primary_key=True)
    course = ParentalKey(CoursePage, on_delete=models.CASCADE, related_name='announcements')
    title = models.CharField(max_length=255)
    body = RichTextField()
    attachment = models.ForeignKey(
        Document, null=True, blank=True, on_delete=models.SET_NULL, related_name='+'
    )

    panels = [
        FieldPanel('title'),
        FieldPanel('body', classname="full"),
        FieldPanel('attachment'),
    ]


class Resource(Page):
    content = RichTextField(blank=True, null=True)
    attachment = models.ForeignKey(
        Document, null=True, blank=True, on_delete=models.SET_NULL, related_name='+'
    )
    under_process = models.BooleanField(default=False, blank=True)
    topics = models.TextField(default="", blank=True)
    summary = RichTextField(blank=True, null=True)
    vectorstore_ids = models.TextField(default="", blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('content', classname="full"),
        FieldPanel('attachment'),
        FieldPanel('under_process'),
        FieldPanel('topics'),
        FieldPanel('summary'),
    ]

    parent_page_types = ['course.CoursePage']
    subpage_types = []


class QuestionPaper(Page):
    course = ParentalKey(CoursePage, on_delete=models.CASCADE, related_name='question_papers')
    is_created = models.BooleanField(default=False)

    content_panels = Page.content_panels + [
        FieldPanel('course'),
        FieldPanel('is_created'),
        InlinePanel('questions', label="Questions"),
    ]

    parent_page_types = ['wagtailcore.Page']
    subpage_types = []


class Question(ClusterableModel):
    id = models.UUIDField(primary_key=True, editable=False, unique=True, default=uuid.uuid4)
    question_paper = ParentalKey(QuestionPaper, on_delete=models.CASCADE, related_name='questions')
    question = models.TextField()

    def __str__(self):
        return self.question
    
    panels = [
        FieldPanel('question_paper'),
        FieldPanel('question'),
        InlinePanel('answers', label="Answers"),
    ]


class Answer(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, unique=True, default=uuid.uuid4)
    question = ParentalKey(Question, on_delete=models.CASCADE, related_name="answers")
    answer = models.TextField()
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.answer

    class Meta:
        verbose_name_plural = "Answers"
