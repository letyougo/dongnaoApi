# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-11-09 06:13
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appcenter', '0002_app_score'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='app',
            name='score',
        ),
    ]
