from __future__ import unicode_literals

from django.db import models

# Create your models here.
from react1.models import Student
class App(models.Model):
    student = models.ForeignKey(Student,null=True,blank=True)
    url = models.CharField(max_length=256,null=True,blank=True)
    description = models.TextField()
