from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Student(models.Model):
    name = models.CharField(max_length=32,unique=True)
    age = models.IntegerField()
    sex = models.CharField(max_length=32)
    single = models.BooleanField()

    def __unicode__(self):
        return self.name


