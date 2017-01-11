# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import TemplateView

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from base_project.models import UserProfile, Survey, Question
from base_project.forms import SurveyForm
from base_project.constants import CHECKBOX, SELECT, INTEGER, TEXT, YES_NO, WIDGET_TYPES

from django.contrib import messages

import json

# Create your views here.

class Home(TemplateView):
    template_name = "home.html"

class SignUp(TemplateView):
    template_name = "sign_up.html"

    def post(self, request):
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        email = request.POST.get('email')
        password = request.POST.get('password')

        context = {
            'first_name': name,
            'last_name': surname,
            'email': email
        }

        if name and surname and password and email:
            u, created = User.objects.get_or_create(email=email)
            if created:
                # user was created
                # set the password here
                u.first_name = name
                u.last_name = surname
                u.username = email
                u.set_password(password)
                u.is_active = False
                u.save()

                user_profile = UserProfile.objects.get_or_create(user=u)

                messages.success(request, "<strong>Exito!</strong> Te hemos enviado un email de confirmacion para completar tu registro.")
                return HttpResponseRedirect('/')
            else:
                # user was retrieved
                messages.error(request, "<strong>Error!</strong> No puede haber campos vacios.")
                return render(request, template_name=self.template_name, context=context)

        else:
            # user was empty
            messages.error(request, "<strong>Error!</strong> No puede haber campos vacios.")
            return render(request, template_name=self.template_name, context=context)

class Login(TemplateView):
    template_name = "login.html"

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(username=email, password=password)

        if user is not None:
            # A backend authenticated the credentials
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return redirect('/my_account')
            else:
                # An inactive account was used - no logging in!
                return redirect('/login')
        else:
            # No backend authenticated the credentials
            return redirect('/login')

class Logout(TemplateView):
    template_name = "login.html"

    def get(self, request):
        logout(request)
        return redirect('/')

class MyAccount(TemplateView):
    template_name = "my_account.html"

    def get(self, request, *args, **kwargs):
        user_profile = UserProfile.objects.get(user=request.user)
        surveys = Survey.objects.filter(user=request.user)

        context = {
            'profile': user_profile,
            'surveys': surveys
        }
        return render(request, template_name=self.template_name, context=context)

class CreateSurvey(TemplateView):
    template_name = 'createsurvey.html'

    def get(self, request, *args, **kwargs):
        user = request.user
        form = SurveyForm()

        context = {
            'user': user,
            'form': form
        }

        return render(request, template_name=self.template_name, context=context)

    def post(self, request):
        user = request.user
        data = request.POST

        survey = json.loads(data['dict'])

        survey_name = survey['survey_name']
        survey_active = survey['active']

        try:
            s = Survey.objects.create(user=user, name=survey_name, active=survey_active)
        except Exception as e:
            print e

        for i in range(0,len(survey['question_type'])):
            QUESTION_TYPE_N = "question_type_" + str(i)
            QUESTION_DESCRIPTION_N = "question_description_" + str(i)
            QUESTION_OPTIONS_N = "question_options_" + str(i)

            TYPES = [SELECT, CHECKBOX]

            question_type = survey['question_type'][QUESTION_TYPE_N]
            question_description = survey['question_description'][QUESTION_DESCRIPTION_N]
            question_options = ""
            if question_type in TYPES:
                question_options = survey['question_options'][QUESTION_OPTIONS_N]


            q = Question.objects.create(survey=s, question_type=question_type,
                                        question_description=question_description,
                                        question_options=question_options)


        context = {
            'status': 1
        }

        return HttpResponse(json.dumps(context), content_type='application/json')

class EditProfile(TemplateView):
    template_name = "edit_profile.html"

    def get(self, request, *args, **kwargs):
        user = request.user

        context = {
            'empty_field': False,
            'update_success': False,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }

        return render(request, template_name=self.template_name, context=context)

    def post(self, request):
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        email = request.POST.get('email')

        user = request.user

        context = {
            'first_name': name,
            'last_name': surname,
            'email': email
        }

        if name and surname and email:
            if user:
                user.first_name = name
                user.last_name = surname
                user.username = email
                user.email = email
                user.save()

                messages.success(request, "<strong>Exito!</strong> Tu informacion se ha guardado correctamente.")
                return render(request, template_name=self.template_name, context=context)
            else:
                # user was retrieved
                messages.error(request, "<strong>Error!</strong> No puede haber campos vacios.")
                return render(request, template_name=self.template_name, context=context)

        else:
            # user was empty
            messages.error(request, "<strong>Error!</strong> No puede haber campos vacios.")
            return render(request, template_name=self.template_name, context=context)

class ChangeImage(TemplateView):
    template_name = "change_image.html"

    def get(self, request, *args, **kwargs):
        user = request.user
        user_profile = UserProfile.objects.get(user=user)

        context = {
            'profile': user_profile
        }

        return render(request, template_name=self.template_name, context=context)

    def post(self, request):

        user = request.user
        user_profile = UserProfile.objects.get(user=user)

        context = {
            'profile': user_profile
        }

        if request.FILES.get('avatar'):
            if user:
                file = request.FILES.get('avatar')

                user_profile.avatar = file
                user_profile.save()

                messages.success(request, "<strong>Exito!</strong> La imagen se ha guardado correctamente.")
                return render(request, template_name=self.template_name, context=context)
            else:
                messages.error(request, "<strong>Error!</strong> Tu sesion ha expirado.")
                return render(request, template_name=self.template_name, context=context)
        else:
            messages.error(request, "<strong>Error!</strong> No puede haber campos vacios.")
            return render(request, template_name=self.template_name, context=context)

class ChangePassword(TemplateView):
    template_name = "change_password.html"

    def post(self, request):

        last_password = request.POST.get('last_password')
        new_password_1 = request.POST.get('new_password_1')
        new_password_2 = request.POST.get('new_password_2')

        user = request.user

        context = {

        }

        if last_password and new_password_1 and new_password_2:

            if user:
                check_password = user.check_password(last_password)
                if check_password:
                    if last_password != new_password_1 and new_password_1 == new_password_2:
                        user.set_password(new_password_1)
                        user.save()

                        messages.success(request, "<strong>Exito!</strong> La contraseña se ha guardado correctamente.")
                        return render(request, template_name=self.template_name, context=context)
                    else:
                        # user was retrieved
                        messages.error(request, "<strong>Error!</strong> La nueva contraseña no coincide.")
                        return render(request, template_name=self.template_name, context=context)
                else:
                    messages.error(request, "<strong>Error!</strong> La contraseña no es correcta.")
                    return render(request, template_name=self.template_name, context=context)
            else:
                messages.error(request, "<strong>Error!</strong> Tu sesion ha expirado.")
                return render(request, template_name=self.template_name, context=context)
        else:
            # user was empty
            messages.error(request, "<strong>Error!</strong> No puede haber campos vacios.")
            return render(request, template_name=self.template_name, context=context)

class SurveyOptionsSurvey(TemplateView):
    template_name = "survey_options_survey.html"

    def get(self, request, id):
        user = request.user
        survey = Survey.objects.get(user=user, pk=id)

        context = {
            'user': user,
            'survey': survey
        }

        return render(request, template_name=self.template_name, context=context)

    def post(self, request, id):
        name = request.POST.get('survey_name')
        active = YES_NO(request.POST.get('survey_active'))

        user = request.user

        survey = Survey.objects.get(user=user, pk=id)
        survey.name = name
        survey.active = active
        survey.save()


        context = {
            'user': user,
            'survey': survey
        }

        messages.success(request, "<strong>Exito!</strong> La imagen se ha guardado correctamente.")
        return render(request, template_name=self.template_name, context=context)

class SurveyOptionsQuestions(TemplateView):
    template_name = "survey_options_questions.html"

    def get(self, request, id):
        user = request.user
        survey = Survey.objects.get(user=user, pk=id)
        questions = Question.objects.filter(survey=survey)

        context = {
            'user': user,
            'survey': survey,
            'questions': questions,
            'widget_types': WIDGET_TYPES
        }

        return render(request, template_name=self.template_name, context=context)

class DeleteSurvey(TemplateView):

    def get(self, request, id):
        user = request.user
        survey = Survey.objects.get(user=user, pk=id)
        survey.delete()

        messages.success(request, "<strong>Exito!</strong> La encuesta ha sido eliminada correctamente.")
        return HttpResponseRedirect('/my_account')


class SurveyView(TemplateView):
    template_name = "survey.html"

    def get(self, request, id):
        user = request.user
        survey = Survey.objects.get(user=user, pk=id)
        questions = Question.objects.filter(survey=survey)

        TYPES = [SELECT, CHECKBOX]

        for x in questions:
            if x.question_type in TYPES:
                x.options = x.question_options.split(",")

        context = {
            'user': user,
            'survey': survey,
            'questions': questions,
            'widget_types': WIDGET_TYPES
        }

        return render(request, template_name=self.template_name, context=context)