from django.forms import ModelForm, TextInput, CheckboxInput
from models import Survey

class SurveyForm(ModelForm):

    class Meta:
        model = Survey
        fields = ['name', 'active']

    def __init__(self, *args, **kwargs):
        super(SurveyForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget = TextInput(attrs={
            'id': 'survey_name',
            'class': 'form-control',
            'name': 'survey_name',
            'placeholder': 'Name'})
        self.fields['active'].widget = CheckboxInput(attrs={
            'id': 'fancy-checkbox-info',
            'name': 'fancy-checkbox-info'
        })

    def save(self, request, commit=True,):
        instance = super(SurveyForm, self).save(request, commit=False)
        instance.user = request.user
        if commit:
            instance.save()
        return instance