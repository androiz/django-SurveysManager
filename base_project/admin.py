from django.contrib import admin
from base_project.models import UserProfile, Survey, Question, Answer, UserTokenActivation


# Register your models here.


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')

@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name', 'active')

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'survey', 'question_type')

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'survey', 'question', 'answer_group')

@admin.register(UserTokenActivation)
class UserTokenActivationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'token')