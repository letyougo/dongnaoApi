# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-11-29 10:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deploy', '0003_auto_20161121_1232'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='deploy',
            field=models.CharField(default='build', max_length=128),
        ),
    ]
