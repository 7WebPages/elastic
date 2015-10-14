# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elastic_django', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='University',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.RenameModel(
            old_name='MyModel', new_name='Student'
        ),
        migrations.AddField(
            model_name='student',
            name='university',
            field=models.ForeignKey(blank=True, to='elastic_django.University', null=True),
        ),
    ]
