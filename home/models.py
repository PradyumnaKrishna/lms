from django.db import models

from wagtail.admin.panels import FieldPanel, TitleFieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Page
from wagtail.snippets.models import register_snippet

from .panels import TargetFieldPanel


class HomePage(Page):
    logo = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL, related_name='+'
    )

    content_panels = Page.content_panels + [
        FieldPanel('logo'),
    ]

    subpage_types = ['InstitutePage']


class InstitutePage(Page):
    short_name = models.CharField(max_length=255)
    intro = RichTextField(blank=True)
    emblem = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL, related_name='+'
    )

    content_panels = [
        TitleFieldPanel("title", targets=[]),
        TargetFieldPanel('short_name', targets=["slug"]),
        FieldPanel('intro'),
        FieldPanel('emblem'),
    ]

    parent_page_types = ['wagtailcore.Page', 'home.HomePage']

    def __str__(self):
        return self.title


@register_snippet
class Department(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    institute = models.ForeignKey(InstitutePage, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    

@register_snippet
class Program(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
