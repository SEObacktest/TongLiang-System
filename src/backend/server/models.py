from django.db import models
from django.contrib.auth.models import User, AbstractUser

from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver


class EvaluationUser(AbstractUser):
    userId = models.CharField(max_length=20, unique=True)
    phone = models.CharField(max_length=20)
    isAdmin = models.BooleanField(default=False)
    bankCard = models.CharField(max_length=30, default="")
    bank = models.CharField(max_length=30, default="")
    accountHolderName = models.CharField(max_length=30, default="")
    idCard = models.CharField(max_length=30, default="")
    age = models.IntegerField(default=0)
    gender = models.CharField(max_length=10, default="")
    account = models.CharField(max_length=30, default="")

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


# 约面试
class Interview(models.Model):
    interviewId = models.CharField(max_length=20, unique=True)
    interviewTime = models.DateTimeField()
    post = models.CharField(max_length=20)
    curriculumVitae = models.ForeignKey('CurriculumVitae', on_delete=models.CASCADE, related_name='CurriculumVitae', default=None, null=True)
    isAgreed = models.BooleanField(default=False)
    isArrived = models.BooleanField(default=False)
    commuteTime = models.CharField(max_length=20)
    createTime = models.DateTimeField(auto_now_add=True)

class CurriculumVitae(models.Model):
    user = models.ForeignKey(EvaluationUser, on_delete=models.CASCADE, related_name='CurriculumVitaeUser')
    interview = models.ForeignKey(Interview, on_delete=models.CASCADE, related_name='CurriculumVitaeInterview')
    time = models.DateTimeField(auto_now_add=True)
    post = models.CharField(max_length=20)
    file = models.FileField(upload_to='curriculum_vitae_file')

# 题库
class TestCurriculumVitae(models.Model):
    post = models.CharField(max_length=20)
    answer = models.BooleanField()
    file = models.FileField(upload_to='test_curriculum_vitae_file')

#     随机获取10道题
    def getTestCurriculumVitae(self):
        return self.objects.all().order_by('?')[:10]


class ActivityImage(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='Activity')
    image = models.ImageField(upload_to='activity_image')


class UserImage(models.Model):
    user = models.ForeignKey(EvaluationUser, on_delete=models.CASCADE, related_name='User')
    image = models.ImageField(upload_to='user_image')