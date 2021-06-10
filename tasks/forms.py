# from .models import Profile, Project, Review
from tasks.models import Task
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
        fields = '__all__'




