# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-11-09 06:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('react1', '0002_student_score'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='logo',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]
