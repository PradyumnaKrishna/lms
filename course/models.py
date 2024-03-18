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
    content = RichTextField()
    attachment = models.ForeignKey(
        Document, null=True, blank=True, on_delete=models.SET_NULL, related_name='+'
    )

    content_panels = Page.content_panels + [
        FieldPanel('content', classname="full"),
    ]

    parent_page_types = ['course.CoursePage']
    subpage_types = []
