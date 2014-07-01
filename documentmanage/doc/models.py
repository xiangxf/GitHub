from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class DepartmentInfo(models.Model):
    departname = models.TextField(max_length=45)
    departinfo = models.TextField(max_length=100)

class FileInfo(models.Model):
    filename=models.TextField(max_length=50)
    file=models.FileField(upload_to='document/')
    fileinfo=models.TextField(max_length=200)
    departno=models.ForeignKey(DepartmentInfo)

class UserInfo(models.Model):
    user = models.OneToOneField(User,primary_key=True)
    username = models.TextField(blank=True)
    departno = models.ForeignKey(DepartmentInfo)
    accesstype = models.IntegerField()

