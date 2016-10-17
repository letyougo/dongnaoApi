from django.shortcuts import render

# Create your views here.
from rest_framework import generics,permissions
from models import Student
from serializers import StudentSerializer


class StudentList(generics.ListCreateAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class StudentDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = Student.objects.all()
    serializer_class = StudentSerializer