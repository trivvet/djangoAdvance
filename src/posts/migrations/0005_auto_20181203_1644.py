# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-12-03 16:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_post_time_read'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='time_read',
            field=models.IntegerField(default=0),
        ),
    ]
