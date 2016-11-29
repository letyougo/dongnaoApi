from django.shortcuts import render



# Create your views here.
from rest_framework import generics,permissions
from models import User,Project
from serializers import UserSerializer,ProjectSerializer
from django.http.response import JsonResponse
from rest_framework.response import Response

from rest_framework.decorators import detail_route
from dongnaoApi.settings import BASE_DIR
import os
class UserList(generics.ListCreateAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProjectList(generics.ListCreateAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class ProjectDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

def login(request):
    name = request.GET['name']
    password = request.GET['password']
    query = User.objects.filter(name=name,password=password)
    if len(query) == 0:
        return JsonResponse({'info':'user not find'})
    else:
        print 'set cookie'
        response = JsonResponse({'info':query[0].name + ' login'})
        response.set_cookie('user',query[0].id)
    return response

def logout(request):
    response = JsonResponse(dict(
        info="You're logged out."
    ))
    response.delete_cookie('user')
    return response


def create(request):
    user_id = request.COOKIES['user']
    url = request.GET['url']
    name = request.GET['name']
    description = request.GET['description'] if 'description' in  request.GET else 'description'
    logo = request.GET['logo'] if 'logo' in request.GET else 'logo'
    user = User.objects.get(id=user_id)
    Project.objects.create(name=name,description=description,logo=logo,url=url,admin=user)

    return JsonResponse(dict(name=user.name,url=url))

def myproject(request):
    user_id = int(request.COOKIES['user'])
    print user_id,'cookies'
    user = User.objects.get(id=user_id)
    project = user.project_set.all()
    return JsonResponse(dict(
        project = [p.to_obj() for p in project]
    ))

def sync(request):
    query = User.objects.all()
    path = os.path.join(BASE_DIR,'deploy','temp-user-projects') 
    os.chdir(path)
    for user in query:
        os.path.exists(user.folder) or os.mkdir(user.folder)
    return JsonResponse({'info':'create folders successful'})
    


