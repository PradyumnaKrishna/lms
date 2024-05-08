# Generated by Django 4.2.11 on 2024-05-08 10:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0002_alter_coursepage_credit'),
        ('home', '0005_remove_homepage_logo'),
    ]

    operations = [
        migrations.AddField(
            model_name='program',
            name='code',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
        migrations.CreateModel(
            name='Semester',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('sem', models.IntegerField()),
                ('courses', models.ManyToManyField(to='course.coursepage')),
                ('program', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.program')),
            ],
        ),
    ]
