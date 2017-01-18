from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
import os

# Create your models here.

def get_image_path(instance, filename):
    return os.path.join('avatar', str(instance.id), filename)

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    avatar = models.ImageField(upload_to=get_image_path, blank=True, null=True)

    def __str__(self):
        return str(self.id)

class Survey(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=100, blank=False, null=False)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Question(models.Model):
    survey = models.ForeignKey(Survey)
    question_type = models.CharField(max_length=100, blank=False, null=False)
    question_description = models.CharField(max_length=255, blank=False, null=False)
    question_options = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return str(self.id)

class Answer(models.Model):
    survey = models.ForeignKey(Survey)
    question = models.ForeignKey(Question)
    answer_group = models.IntegerField(null=False, blank=False)
    answer = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return str(self.id)

class UserTokenActivation(models.Model):
    user = models.ForeignKey(User, null=False)
    token = models.CharField(max_length=255, blank=False, null=False)

    def __str__(self):
        return str(self.user.username)