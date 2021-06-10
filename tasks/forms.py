# from .models import Profile, Project, Review
from django.forms import fields
from tasks.models import Challege, Task
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username','email','password1','password2']


class TaskingForm(forms.ModelForm):
    class Meta:
        model = Task
        exclude = ['phase']


class UpdateTaskPhaseForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['phase']


class ChallengeForm(forms.ModelForm):
    class Meta:
        model = Challege
        fields = ['description']




