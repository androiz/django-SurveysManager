# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base_project', '0005_usertokenactivation'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='question_columns',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='question',
            name='question_rows',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
