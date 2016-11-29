from __future__ import unicode_literals

from django.db import models

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=32)
    password = models.CharField(max_length=64)
    folder = models.CharField(max_length=32)
    logo = models.CharField(max_length=128,null=True,blank=True)

    def to_obj(self):
        return dict(
            name = self.name,
            folder = self.folder,
            logo = self.logo

        )
    def __unicode__(self):
        return self.name

class Project(models.Model):
    name = models.CharField(max_length=32)
    description = models.TextField(max_length=128,null=True,blank=True)
    url = models.CharField(max_length=128,default='')
    admin = models.ForeignKey(User)
    logo = models.CharField(max_length=128,null=True,blank=True)
    deploy = models.CharField(max_length=128,default='build')
    def to_obj(self):
        return dict(
            name = self.name,
            description = self.description,
            url = self.url,
            admin = self.admin.to_obj(),
            logo = self.logo
        )
    def __unicode__(self):
        return self.name


