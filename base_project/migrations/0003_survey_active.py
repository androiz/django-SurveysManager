# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base_project', '0002_auto_20170108_1118'),
    ]

    operations = [
        migrations.AddField(
            model_name='survey',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
