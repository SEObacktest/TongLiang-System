# Generated by Django 5.1.3 on 2025-03-12 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0017_evaluationuser_payday'),
    ]

    operations = [
        migrations.AddField(
            model_name='curriculumvitae',
            name='mainProblem',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AddField(
            model_name='curriculumvitae',
            name='problemDescription',
            field=models.TextField(default='', max_length=1000),
        ),
    ]
