# Generated by Django 4.2.11 on 2024-05-10 10:31

from django.db import migrations
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0003_resource_topics_resource_under_process'),
    ]

    operations = [
        migrations.AddField(
            model_name='resource',
            name='summary',
            field=wagtail.fields.RichTextField(blank=True, null=True),
        ),
    ]
