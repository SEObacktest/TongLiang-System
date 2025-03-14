# Generated by Django 5.1.3 on 2025-03-11 17:22

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0012_interview_settlement'),
    ]

    operations = [
        migrations.DeleteModel(
            name='TestCurriculumVitae',
        ),
        migrations.AddField(
            model_name='curriculumvitae',
            name='createTime',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='curriculumvitae',
            name='numTest',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='curriculumvitae',
            name='passTime',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='curriculumvitae',
            name='qualified',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='curriculumvitae',
            name='interview',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='CurriculumVitaeInterview', to='server.interview'),
        ),
    ]
