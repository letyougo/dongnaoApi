from django.contrib.auth.models import User
from rest_framework import serializers
from models import Student
from rest_framework import generics
from rest_framework import generics,permissions
from rest_framework.reverse import reverse









class StudentSerializer(serializers.ModelSerializer):
    # snippets = serializers.HyperlinkedRelatedField(many=True, view_name='snippet-detail')

    class Meta:
        model = Student
        fields = ('id', 'name','age','sex','single','url')


