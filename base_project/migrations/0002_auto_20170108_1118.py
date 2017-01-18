# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import base_project.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base_project', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('answer_group', models.IntegerField()),
                ('answer', models.CharField(max_length=255, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('question_type', models.CharField(max_length=100)),
                ('question_description', models.CharField(max_length=255)),
                ('question_options', models.CharField(max_length=255, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(null=True, upload_to=base_project.models.get_image_path, blank=True),
        ),
        migrations.AddField(
            model_name='question',
            name='survey',
            field=models.OneToOneField(to='base_project.Survey'),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.OneToOneField(to='base_project.Question'),
        ),
        migrations.AddField(
            model_name='answer',
            name='survey',
            field=models.OneToOneField(to='base_project.Survey'),
        ),
    ]
