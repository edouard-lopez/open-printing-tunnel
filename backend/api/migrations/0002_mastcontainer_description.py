# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-28 16:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mastcontainer',
            name='description',
            field=models.TextField(blank=True, help_text='Headquarter office or a branch', verbose_name='site location'),
        ),
    ]
