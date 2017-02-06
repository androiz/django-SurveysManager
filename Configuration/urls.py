"""untitled1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from Configuration import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.conf.urls.static import static

from base_project.views import Home, SignUp, Login, Logout, MyAccount, \
    EditProfile, ChangeImage, ChangePassword, CreateSurvey, SurveyOptionsSurvey, DeleteSurvey, SurveyOptionsQuestions, \
    SurveyView, SurveyOptionsData, exportCSV, account_activation, resend_activation, SurveyOptionCharts, exportPDF

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', Home.as_view()),

    url(r'^my_account/$', login_required(MyAccount.as_view())),
    url(r'^create_survey/$', login_required(CreateSurvey.as_view())),

    url(r'^edit_profile/$', login_required(EditProfile.as_view())),
    url(r'^change_image/$', login_required(ChangeImage.as_view())),
    url(r'^change_password/$', login_required(ChangePassword.as_view())),

    url(r'^survey_options/(?P<id>\d+)/$', login_required(SurveyOptionsSurvey.as_view())),
    url(r'^survey_questions/(?P<id>\d+)/$', login_required(SurveyOptionsQuestions.as_view())),
    url(r'^survey_data/(?P<id>\d+)/$', login_required(SurveyOptionsData.as_view())),
    url(r'^survey_charts/(?P<id>\d+)/$', login_required(SurveyOptionCharts.as_view())),

    url(r'^survey/(?P<id>\d+)/$', SurveyView.as_view()),
    url(r'^delete_survey/(?P<id>\d+)/$', login_required(DeleteSurvey.as_view())),
    url(r'^exportCSV/(?P<id>\d+)/$', login_required(exportCSV)),
    url(r'^exportPDF/(?P<id>\d+)/$', login_required(exportPDF)),

    url(r'^sign_up/$', SignUp.as_view()),
    url(r'^login/$', Login.as_view()),
    url(r'^logout/$', login_required(Logout.as_view())),
    url(r'^activation/(?P<token>\w+)/$', account_activation),
    url(r'^resend/(?P<user_id>\d+)/$', resend_activation),

    url(r'^rosetta/', include('rosetta.urls')),
    url(r'^i18n/', include('django.conf.urls.i18n')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
