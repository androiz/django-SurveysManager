# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('base_project', '0003_survey_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(to='base_project.Question'),
        ),
        migrations.AlterField(
            model_name='answer',
            name='survey',
            field=models.ForeignKey(to='base_project.Survey'),
        ),
        migrations.AlterField(
            model_name='question',
            name='survey',
            field=models.ForeignKey(to='base_project.Survey'),
        ),
        migrations.AlterField(
            model_name='survey',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
