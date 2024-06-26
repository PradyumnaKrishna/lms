# Generated by Django 4.2.11 on 2024-05-14 10:13

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields
import uuid
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0091_remove_revision_submitted_for_moderation'),
        ('course', '0005_resource_vectorstore_ids'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resource',
            name='content',
            field=wagtail.fields.RichTextField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='QuestionPaper',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('is_created', models.BooleanField(default=False)),
                ('course', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='question_papers', to='course.coursepage')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('question', models.TextField()),
                ('question_paper', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='course.questionpaper')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('answer', models.TextField()),
                ('is_correct', models.BooleanField(default=False)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.question')),
            ],
            options={
                'verbose_name_plural': 'Answers',
            },
        ),
    ]
