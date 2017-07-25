# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-24 14:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configfactory', '0003_auto_20160219_1410'),
    ]

    operations = [
        migrations.AlterField(
            model_name='component',
            name='alias',
            field=models.SlugField(help_text='Unique component alias', unique=True),
        ),
    ]
