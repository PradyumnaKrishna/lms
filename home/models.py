from django import forms
from django.db import models
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.models import ClusterableModel
from wagtail.admin.panels import FieldPanel, InlinePanel, TitleFieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Page
from wagtail.snippets.models import register_snippet

from .panels import TargetFieldPanel


class HomePage(Page):
    subpage_types = ["InstitutePage"]


class InstitutePage(Page):
    short_name = models.CharField(max_length=255)
    intro = RichTextField(blank=True)
    emblem = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    content_panels = [
        TitleFieldPanel("title", targets=[]),
        TargetFieldPanel("short_name", targets=["slug"]),
        FieldPanel("intro"),
        FieldPanel("emblem"),
    ]

    subpage_types = ["course.CoursePage"]
    parent_page_types = ["wagtailcore.Page", "home.HomePage"]

    def __str__(self):
        return self.title


@register_snippet
class Department(ClusterableModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    institute = models.ForeignKey(InstitutePage, on_delete=models.CASCADE)

    panels = [
        FieldPanel("name"),
        FieldPanel("description"),
        InlinePanel("programs", label="Programs"),
    ]

    def __str__(self):
        return self.name


@register_snippet
class Program(ClusterableModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255, blank=True, null=True, unique=True)
    description = models.TextField()
    department = ParentalKey(Department, on_delete=models.CASCADE, related_name="programs")

    panels = [
        FieldPanel("name"),
        FieldPanel("code"),
        FieldPanel("description"),
        InlinePanel("semesters", label="Semesters"),
    ]

    def __str__(self):
        return self.name


@register_snippet
class Semester(ClusterableModel):
    id = models.AutoField(primary_key=True)
    sem = models.IntegerField()
    program = ParentalKey(Program, on_delete=models.CASCADE, related_name="semesters")
    courses = ParentalManyToManyField("course.CoursePage")

    panels = [
        FieldPanel("sem"),
        FieldPanel("courses", widget=forms.CheckboxSelectMultiple),
    ]

    def __str__(self):
        return f"{self.program.name}: Semester {self.sem}"
