# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-11-09 06:18
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appcenter', '0003_remove_app_score'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='app',
            name='logo',
        ),
    ]
