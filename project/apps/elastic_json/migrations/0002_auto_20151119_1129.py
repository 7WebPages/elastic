# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from elastic_json.utils.infrastructure import create_index


def create(apps, schema_editor):
    create_index()


class Migration(migrations.Migration):

    dependencies = [
        ('elastic_json', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create)
    ]
