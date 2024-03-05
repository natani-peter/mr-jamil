from django import forms
from django.contrib.auth.forms import UserCreationForm
from . import models


class RegisterTeacher(UserCreationForm):
    class Meta:
        model = models.Teacher
        fields = ['username', 'gender', 'email', 'phone']
        labels = {"text": ''}


class RecordForm(forms.ModelForm):
    subject_taught = forms.CharField(help_text='Subject to be taught')
    topic = forms.CharField(help_text='subject to be taught')

    class Meta:
        model = models.ClassRecord
        fields = ['subject_taught', 'topic']
        attrs = {'label': ''}
