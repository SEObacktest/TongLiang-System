# Generated by Django 5.1.3 on 2025-03-07 16:48

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0005_remove_activity_student_activity_hr'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activity',
            name='hr',
        ),
        migrations.AddField(
            model_name='activity',
            name='student',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Student', to=settings.AUTH_USER_MODEL),
        ),
    ]
