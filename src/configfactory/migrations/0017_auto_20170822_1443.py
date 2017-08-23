# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-22 14:43
from __future__ import unicode_literals

import json

from django.db import migrations

from configfactory.utils import json_dumps, json_loads


def create_config_db_store(apps, schema_editor):

    Component = apps.get_model('configfactory', 'Component')
    Config = apps.get_model('configfactory', 'Config')
    Environment = apps.get_model('configfactory', 'Environment')

    environments = Environment.objects.all()

    for component in Component.objects.all():
        settings = json_loads(component.settings_json)

        for environment in environments:
            config, created = Config.objects.get_or_create(
                component=component.alias,
                environment=environment.alias
            )
            config.settings_json = json.dumps(
                settings.get(environment.alias, {})
            )
            config.save()


class Migration(migrations.Migration):

    dependencies = [
        ('configfactory', '0016_auto_20170822_1441'),
    ]

    operations = [
        migrations.RunPython(
            code=create_config_db_store,
            reverse_code=migrations.RunPython.noop
        ),
    ]
