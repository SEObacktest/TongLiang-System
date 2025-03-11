import os

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

#     计算属于该用户的Interview个数
    def getInterviewCount(self):
        if Interview.objects.all().filter(user=self).count() is None:
            return 0
        return Interview.objects.all().filter(user=self).count()

    def getUnSettlementInterview(self):
        return Interview.objects.all().filter(user=self).filter(settlement=False)

    def to_dict(self):
        return {
            "userId": self.userId,
            "username": self.username,
            "phone": self.phone,
            "isAdmin": self.isAdmin,
            "account": self.account,
            "bankCard": self.bankCard,
            "bank": self.bank,
            "accountHolderName": self.accountHolderName,
            "idCard": self.idCard,
            "age": self.age,
            "gender": self.gender,
            "last_login": self.last_login,
            "date_joined": self.date_joined,
            "interviewCount": self.getInterviewCount(),
        }

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
    interviewee = models.CharField(max_length=20, default='')
    interviewTime = models.DateTimeField()
    post = models.CharField(max_length=20)
    user = models.ForeignKey(EvaluationUser, on_delete=models.CASCADE, related_name='CurriculumVitaeUser', default=None)
    isAgreed = models.BooleanField(default=False)
    isArrived = models.BooleanField(default=False)
    commuteTime = models.CharField(max_length=20)
    createTime = models.DateTimeField(auto_now_add=True)
    settlement = models.BooleanField(default=False)

class CurriculumVitae(models.Model):
    interview = models.ForeignKey(Interview, on_delete=models.CASCADE, related_name='CurriculumVitaeInterview')
    time = models.DateTimeField(auto_now_add=True)
    post = models.CharField(max_length=20)
    file = models.FileField(upload_to='curriculum_vitae_file')

# 题库
class TestCurriculumVitae(models.Model):
    post = models.CharField(max_length=20)
    answer = models.BooleanField()
    file = models.FileField(upload_to='test_curriculum_vitae_file')
    createTime = models.DateTimeField(auto_now_add=True)
    numTest = models.IntegerField(default=0)
    passTime = models.IntegerField(default=0)

    def getPassRate(self):
        if self.numTest == 0:
            return 0
        return self.passTime / self.numTest

#     随机获取10道题
    @classmethod
    def getTestCurriculumVitae(cls):
        return cls.objects.order_by('?')[:10]  # 直接通过 cls.objects 调用

    def delete(self, *args, **kwargs):
        # 在删除数据库记录之前，删除文件
        if self.file:
            if os.path.isfile(self.file.path):
                os.remove(self.file.path)
        models.Model.delete(self, *args, **kwargs)

class ActivityImage(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='Activity')
    image = models.ImageField(upload_to='activity_image')


class UserImage(models.Model):
    user = models.ForeignKey(EvaluationUser, on_delete=models.CASCADE, related_name='User')
    image = models.ImageField(upload_to='user_image')