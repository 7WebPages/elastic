# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('year_in_school', models.CharField(max_length=2, choices=[(b'FR', b'Freshman'), (b'SO', b'Sophomore'), (b'JR', b'Junior'), (b'SR', b'Senior')])),
                ('age', models.SmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)])),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('courses', models.ManyToManyField(to='elastic_json.Course', null=True, blank=True)),
            ],
            options={
                'es_mapping': {'properties': {'first_name': {'index': 'not_analyzed', 'type': 'string'}, 'last_name': {'index': 'not_analyzed', 'type': 'string'}, 'university': {'type': 'object', 'properties': {'_id': {'index': 'not_analyzed', 'store': True}, 'name': {'index': 'not_analyzed', 'type': 'string'}}}, 'course_names': {'index': 'not_analyzed', 'type': 'string', 'store': 'yes'}, 'name_complete': {'preserve_separators': True, 'analyzer': 'simple', 'payloads': True, 'max_input_length': 50, 'preserve_position_increments': True, 'type': 'completion'}, 'year_in_school': {'type': 'string'}, '_id': {'index': 'not_analyzed', 'store': True}, 'age': {'type': 'short'}}},
                'es_index_name': 'django',
                'es_type_name': 'student',
            },
        ),
        migrations.CreateModel(
            name='University',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='student',
            name='university',
            field=models.ForeignKey(blank=True, to='elastic_json.University', null=True),
        ),
    ]
