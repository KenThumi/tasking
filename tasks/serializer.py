from django.contrib.auth.models import User
from django.db.models import fields
from rest_framework import serializers
from .models import  Phase, Task

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model =User
        fields = ['username']

class PhaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phase
        fields = ['title']

class TaskSerializer(serializers.ModelSerializer): #(many=True, read_only=True)
    user = UserSerializer(read_only=True)
    phase = PhaseSerializer(read_only=True)

    class Meta:
        model = Task
        fields = ['title','user', 'phase']