# -*- coding: utf-8 -*-
import csv
import hashlib

from django.db.models import Max
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import TemplateView

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from base_project.emails import account_activation_email
from base_project.models import UserProfile, Survey, Question, Answer, UserTokenActivation
from base_project.forms import SurveyForm
from base_project.constants import CHECKBOX, SELECT, INTEGER, TEXT, YES_NO, WIDGET_TYPES, RADIO

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

                token = hashlib.sha256(u.username).hexdigest()
                UserTokenActivation.objects.create(user=u, token=token)
                url = request.META['HTTP_HOST'] + "/activation/" + token + "/"
                sent_email = account_activation_email(url, u.email)

                messages.success(request, "<strong>Warning!</strong> Te hemos enviado un email de confirmacion para completar tu registro.")
                return HttpResponseRedirect('/')
            else:
                # user was retrieved
                messages.error(request, "<strong>Error!</strong> No puede haber campos vacios.")
                return render(request, template_name=self.template_name, context=context)

        else:
            # user was empty
            messages.error(request, "<strong>Error!</strong> No puede haber campos vacios.")
            return render(request, template_name=self.template_name, context=context)

def account_activation(request, token):
    try:
        uta = UserTokenActivation.objects.get(token=token)
        user = User.objects.get(id=uta.user.id)
        user.is_active = True
        user.save()
        uta.delete()

        messages.success(request, "<strong>Exito!</strong> Tu cuenta ha sido activada correctamente.")
        return HttpResponseRedirect('/')
    except Exception as e:
        print e
        return HttpResponseRedirect('/')

def resend_activation(request, user_id):
    user = User.objects.get(pk=user_id)

    uta = UserTokenActivation.objects.get(user=user)
    token = uta.token
    url = request.META['HTTP_HOST'] + "/activation/" + token + "/"
    sent_email = account_activation_email(url, user.email)

    messages.success(request, "<strong>Exito!</strong> Te hemos enviado un email de confirmacion para completar tu registro.")
    return HttpResponseRedirect('/')

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
                # return redirect('/login')
                messages.warning(request, "<strong>Warning!</strong> Es necesario activar la cuenta. \
                Pulsa <a href='/resend/" + str(user.id) + "/'>aqui</a> para recibir el correo de activacion.")
                return HttpResponseRedirect('/login')
        else:
            # No backend authenticated the credentials
            #return redirect('/login')
            messages.error(request, "<strong>Error!</strong> El usuario o la contraseña son incorrectos.")
            return HttpResponseRedirect('/login')

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

            TYPES = [SELECT, CHECKBOX, RADIO]

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
            'email': user.email,
            'selected_option': 'profile'
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
            'profile': user_profile,
            'selected_option': 'image'
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

    def get(self, request, *args, **kwargs):

        context = {
            'selected_option': 'password'
        }

        return render(request, template_name=self.template_name, context=context)

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
            'survey': survey,
            'selected_option': 'survey'
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
            'widget_types': WIDGET_TYPES,
            'selected_option': 'questions'
        }

        return render(request, template_name=self.template_name, context=context)

class SurveyOptionsData(TemplateView):
    template_name = "survey_options_data.html"

    def get(self, request, id):
        user = request.user
        survey = Survey.objects.get(user=user, pk=id)
        questions = Question.objects.filter(survey=survey)
        unclassified_answers = Answer.objects.filter(survey=survey)

        answers = dict()
        for x in unclassified_answers:
            if x.answer_group in answers.keys():
                answers[x.answer_group].append(x)
            else:
                answers[x.answer_group] = [x]

        for key, elem in answers.items():
            answers[key] = sorted(elem, key=lambda x: x.question.id)

        context = {
            'user': user,
            'survey': survey,
            'questions': questions,
            'answers': answers,
            'selected_option': 'data'
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
        survey = Survey.objects.get(pk=id)
        if survey.active:
            questions = Question.objects.filter(survey=survey)

            TYPES = [SELECT, CHECKBOX, RADIO]

            for x in questions:
                if x.question_type in TYPES:
                    x.options = x.question_options.split(",")

            context = {
                'survey': survey,
                'questions': questions,
                'widget_types': WIDGET_TYPES
            }

            return render(request, template_name=self.template_name, context=context)
        else:
            return redirect("/")

    def post(self, request, id):
        survey = Survey.objects.get(pk=id)

        max_group = Answer.objects.filter(survey=survey).aggregate(Max('answer_group'))['answer_group__max']
        if max_group is not None:
            max_group = max_group + 1
        else:
            max_group = 0

        checkbox_answers = dict()

        for key, value in request.POST.items():
            ql = key.split('_')
            if ql[0] == 'question':
                q_id = int(ql[1])
                q = Question.objects.get(pk=q_id, survey=survey)
                if q.question_type != CHECKBOX:
                    answer = Answer.objects.create(survey=survey, question=q, answer_group=max_group, answer=value)
                else:
                    num_options = len(q.question_options.split(","))
                    if ql[0]+"_"+ql[1] in checkbox_answers.keys():
                        checkbox_answers[ql[0] + "_" + ql[1]][int(ql[3])-1] = 1
                    else:
                        checkbox_answers[ql[0] + "_" + ql[1]] = [0] * num_options
                        checkbox_answers[ql[0] + "_" + ql[1]][int(ql[3]) - 1] = 1

        # CHECKBOX Question
        for key, value in checkbox_answers.items():
            ql = key.split('_')
            q_id = int(ql[1])
            q = Question.objects.get(pk=q_id, survey=survey)
            checkbox_answer = str(value).strip('[]')
            answer = Answer.objects.create(survey=survey, question=q, answer_group=max_group, answer=checkbox_answer)

        return redirect('/my_account')

def exportCSV(request, id):
    user = request.user
    survey = Survey.objects.get(user=user, pk=id)
    questions = Question.objects.filter(survey=survey)
    unclassified_answers = Answer.objects.filter(survey=survey)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="data.csv"'
    writer = csv.writer(response)

    first_line = ['Row'] + [x.question_description for x in questions]
    writer.writerow(first_line)

    answers = dict()
    for x in unclassified_answers:
        if x.answer_group in answers.keys():
            answers[x.answer_group].append(x)
        else:
            answers[x.answer_group] = [x]

    for key, elem in answers.items():
        answers[key] = sorted(elem, key=lambda x: x.question.id)

    for index, key in enumerate(answers.keys()):
        writer.writerow([str(index)] + [x.answer for x in answers[key]])

    return response