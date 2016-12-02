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
        return JsonResponse({'info':'user not find','noLogin':True})
    else:
        print 'set cookie'
        response = JsonResponse({'info':query[0].name + ' login','noLogin':False})
        response.set_cookie('user',query[0].id)
    return response

def init(request):
    user_id = request.COOKIES['user']
    user = User.objects.get(id=user_id)
    users = User.objects.all()  
    return JsonResponse(
            dict(
                info=user.to_obj(),
                project=[p.to_obj2() for p in  user.project_set.all()],
                users = [u.to_obj() for u in users]
            )    
        )

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

base_path = os.path.join(BASE_DIR,'deploy','temp-user-projects')

def sync(request):
    query = User.objects.all()
    os.chdir(base_path)
    for user in query:
        os.path.exists(user.folder) or os.mkdir(user.folder)
    return JsonResponse({'info':'create folders successful'})
    
from distutils.dir_util import copy_tree,remove_tree
from tools import Shell
from gittle import Gittle


def get_repo_info(repo_path):
    if not os.path.exists(repo_path):
        return dict(
            info=[],
            error=True,
            msg='repo not exist'
        )

    git_path = os.path.join(repo_path, '.git')
    if not os.path.exists(git_path):
        return dict(
            info=[],
            error=True,
            msg='.git file lost'
        )

    repo = Gittle(repo_path)
    list_dir = os.listdir(repo_path)
    folders = []
    print list_dir
    for i in range(len(list_dir)):
        if os.path.isdir(os.path.join(repo_path, list_dir[i])):
            folders.append(list_dir[i])

    return dict(
        commit_info=repo.commit_info(start=0),
        remote_branches=repo.remote_branches,
        local_branches=repo.branches,
        active_branch=repo.active_branch,
        folders=folders,
    )

def repo(request):
    id = request.get['repo_id']
    project = Project.objects.get(id=id)
    repo_name = project.name
    user_name = project.admin.name
    path = os.join(base_dir,user_name,repo_name)
    result = get_repo_info(path)
    return JsonRespons(result)


def clone(request):
    user_id = int(request.COOKIES['user'])
    folder = User.objects.get(id=user_id).folder
    my_path = os.path.join(base_path,folder)
    os.chdir(my_path)
    url = request.GET['url']
    name = request.GET['name']
    repo_path = os.path.join(my_path,name)
    if os.path.exists(repo_path):
        return remove_tree(repo_path)

    shell = Shell()
    print 'git clone ' + url + ' ' + name
    shell.run('git clone ' + url + ' ' + name)
    print 'git clone over'

    result = get_repo_info(repo_path)
    print result
    return JsonResponse(result)

def detail(request):
    user_id = int(request.COOKIES['user'])
    folder = User.objects.get(id=user_id).folder
    name = request.GET['name']
    repo_path = os.path.join(base_path,folder,name)

    result = get_repo_info(repo_path)
    return JsonResponse(result)


def branch(request):
    user_id = int(request.COOKIES['user'])
    folder = User.objects.get(id=user_id).folder
    name = request.GET['name']
    repo_path = os.path.join(base_path, folder, name)
    os.chdir(repo_path)

    shell = Shell()
    shell.run('git checkout -b'+request.GET['branch'])
    shell.run('git pull origin '+request.GET['branch'])

    return JsonResponse(dict(
        info=shell.info,
        err=shell.err
    ), safe=False)

def reset(request):
    user_id = int(request.COOKIES['user'])
    folder = User.objects.get(id=user_id).folder
    name = request.GET['name']
    repo_path = os.path.join(base_path, folder, name)
    os.chdir(repo_path)

    shell = Shell()
    shell.run('git reset --hard '+request.GET['sha'])

    return JsonResponse(dict(
        info=shell.info,
        err=shell.err
    ), safe=False)
