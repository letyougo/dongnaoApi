from django.shortcuts import render

# Create your views here.
from rest_framework import generics,permissions
from models import Student
from serializers import StudentSerializer

from rest_framework.response import Response

from rest_framework.decorators import detail_route

class StudentList(generics.ListCreateAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class StudentDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


