# Generated by Django 4.2.11 on 2024-05-13 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0004_resource_summary'),
    ]

    operations = [
        migrations.AddField(
            model_name='resource',
            name='vectorstore_ids',
            field=models.TextField(blank=True, default=''),
        ),
    ]
