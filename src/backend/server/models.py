from django.db import models
from django.contrib.auth.models import User, AbstractUser

from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver


class EvaluationUser(AbstractUser):
    userId = models.CharField(max_length=20, unique=True)
    phone = models.CharField(max_length=20)
    isAdmin = models.BooleanField(default=False)
    isTeacher = models.BooleanField(default=False)
    score_test1 = models.IntegerField(default=0)
    stage = models.IntegerField(default=0) # 0: 群众 1: 团员 2: 积极分子 3: 发展对象 4: 预备党员 5: 正式党员


class Activity(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField(max_length=1000)
    startTime = models.DateTimeField()
    endTime = models.DateTimeField()
    location = models.CharField(max_length=100)
    student = models.ForeignKey(EvaluationUser, on_delete=models.CASCADE, related_name='Student', default=None, null=True)
    registerTime = models.DateTimeField(auto_now_add=True)
    certified = models.BooleanField(default=False)
    passed = models.BooleanField(default=False)
    admin = models.ForeignKey(EvaluationUser, on_delete=models.CASCADE, related_name='Admin', default=None, null=True)
    type = models.CharField(max_length=20)


class ActivityImage(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='Activity')
    image = models.ImageField(upload_to='activity_image')


class UserImage(models.Model):
    user = models.ForeignKey(EvaluationUser, on_delete=models.CASCADE, related_name='User')
    image = models.ImageField(upload_to='user_image')