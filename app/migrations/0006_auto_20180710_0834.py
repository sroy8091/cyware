# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-07-10 08:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20180710_0833'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdetails',
            name='followers',
            field=models.IntegerField(blank=True, null=True, verbose_name='Followers'),
        ),
    ]
