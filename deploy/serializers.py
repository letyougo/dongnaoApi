from django.contrib.auth.models import User
from rest_framework import serializers
from models import User,Project
from rest_framework import generics
from rest_framework import generics,permissions
from rest_framework.reverse import reverse









class UserSerializer(serializers.ModelSerializer):
    # snippets = serializers.HyperlinkedRelatedField(many=True, view_name='snippet-detail')

    class Meta:
        model = User
        fields = ('id', 'name','password','folder','logo','url')



class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'name','description','admin','logo','url')

