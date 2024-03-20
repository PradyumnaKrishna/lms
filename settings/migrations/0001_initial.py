# Generated by Django 4.2.11 on 2024-03-18 08:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("wagtailimages", "0025_alter_image_file_alter_rendition_file"),
        ("wagtailcore", "0091_remove_revision_submitted_for_moderation"),
    ]

    operations = [
        migrations.CreateModel(
            name="SiteSettings",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "logo",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to="wagtailimages.image",
                    ),
                ),
                (
                    "site",
                    models.OneToOneField(
                        editable=False,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="wagtailcore.site",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]