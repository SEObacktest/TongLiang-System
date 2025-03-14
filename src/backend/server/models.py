import os

from django.db import models
from django.contrib.auth.models import User, AbstractUser

from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver


class EvaluationUser(AbstractUser):
    userId = models.CharField(max_length=20, unique=True)
    phone = models.CharField(max_length=20)
    city = models.CharField(max_length=20, default="")
    isAdmin = models.BooleanField(default=False)
    bankCard = models.CharField(max_length=30, default="")
    bank = models.CharField(max_length=30, default="")
    accountHolderName = models.CharField(max_length=30, default="")
    idCard = models.CharField(max_length=30, default="")
    age = models.IntegerField(default=0)
    gender = models.CharField(max_length=10, default="")
    account = models.CharField(max_length=30, default="")
    payDay = models.DateTimeField(default=None, null=True)

#     计算属于该用户的Interview个数
    def getInterviewCount(self):
        if Interview.objects.all().filter(user=self).count() is None:
            return 0
        return Interview.objects.all().filter(user=self).count()

    def getUnSettlementInterview(self):
        return Interview.objects.all().filter(user=self).filter(settlement=False, isArrived=True)

    def getSettlementInterview(self):
        return Interview.objects.all().filter(user=self).filter(settlement=True)

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
            "unSettlementInterview": self.getUnSettlementInterview().count(),
            "settlementInterview": self.getSettlementInterview().count(),
            "city": self.city,
            "payDay": self.payDay,
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

    def to_dict(self):
        file_url = CurriculumVitae.objects.get(interview=self).file.url
        return {
            'id': self.id,
            'post': self.post,
            'name': self.interviewee,
            'hr': self.user.username,
            'interview_time': self.interviewTime,
            'file_url': file_url,
            'create_time': self.createTime,
            'commuteTime': self.commuteTime,
            'isAgreed': self.isAgreed,
            'isArrived': self.isArrived,
            'settlement': self.settlement
        }

class Settlement(models.Model):
    user = models.ForeignKey(EvaluationUser, on_delete=models.CASCADE, related_name='SettlementUser', default=None)
    settlementTime = models.DateTimeField(auto_now_add=True)
    amount = models.FloatField()
    bankCard = models.CharField(max_length=30)
    bank = models.CharField(max_length=30)
    accountHolderName = models.CharField(max_length=30)
    idCard = models.CharField(max_length=30)

    def to_dict(self):
        return {
            'id': self.id,
            'hr': self.user.username,
            'settlement_time': self.settlementTime,
            'amount': self.amount,
            'bankCard': self.bankCard,
            'bank': self.bank,
            'accountHolderName': self.accountHolderName,
            'idCard': self.idCard,
        }

class CurriculumVitae(models.Model):
    interview = models.ForeignKey(Interview, on_delete=models.CASCADE, related_name='CurriculumVitaeInterview', default=None, null=True)
    time = models.DateTimeField(auto_now_add=True)
    post = models.CharField(max_length=20)
    file = models.FileField(upload_to='curriculum_vitae_file')
    qualified = models.BooleanField(default=False)
    createTime = models.DateTimeField(auto_now_add=True)
    numTest = models.IntegerField(default=0)
    passTime = models.IntegerField(default=0)
    mainProblem = models.CharField(max_length=20, default='')
    problemDescription = models.TextField(max_length=1000, default='')

    def getPassRate(self):
        if self.numTest == 0:
            return 0
        return self.passTime / self.numTest

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