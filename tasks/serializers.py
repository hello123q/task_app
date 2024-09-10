# tasks/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Task
from rest_framework.authtoken.models import Token

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'due_date', 'category']

class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ['user']
