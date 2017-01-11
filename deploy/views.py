from django.shortcuts import render







from rest_framework import generics,permissions
from models import User,Project
from serializers import UserSerializer,ProjectSerializer
from django.http.response import JsonResponse

from dongnaoApi.settings import BASE_DIR
import os
import requests
from rest_framework import response, schemas


def schema_view(request):
    generator = schemas.SchemaGenerator(title='Pastebin API')
    return response.Response(generator.get_schema(request=request))



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
base_path = os.path.join(BASE_DIR,'deploy','temp-user-projects')
def login(request):
    name = request.GET['name']
    password = request.GET['password']
    query = User.objects.filter(name=name,password=password)
    if len(query) == 0:
        return JsonResponse({'info':'user not find','noLogin':True})
    else:
        print 'set cookie'
        response = JsonResponse({'info':query[0].name + ' login','noLogin':False})
        response.set_cookie('user',query[0].id,3600*24*7)
    return response

def init(request):
    user_id = request.COOKIES['user']
    user = User.objects.get(id=user_id)
    users = User.objects.all()

    user_path = os.path.join(base_path,user.name)
    user_path_exist = os.path.exists(user_path)

    if not user_path_exist:
        os.mkdir(user_path)


    return JsonResponse(
            dict(
                info=user.to_obj(),
                project=[p.to_obj2() for p in user.project_set.all()],
                users = [u.to_obj() for u in users]
            )    
        )


def logout(request):
    response = JsonResponse(dict(
        info="You're logged out."
    ))
    response.delete_cookie('user')
    return response

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
    os.chdir(base_path)
    for user in query:
        os.path.exists(user.folder) or os.mkdir(user.folder)
    return JsonResponse({'info':'create folders successful'})
    
from distutils.dir_util import copy_tree,remove_tree
from tools import Shell
from gittle import Gittle

def get_repo_info(repo_path,is_my_repo):
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
        is_my_repo=is_my_repo
    )


def clone(request):
    user_id = int(request.COOKIES['user'])
    user = User.objects.get(id=user_id)
    folder = user.folder

    url = request.GET['url']
    name = request.GET['name']
    description = request.GET['description'] if 'description' in request.GET else 'description'
    logo = request.GET['logo'] if 'logo' in request.GET else 'logo'
    
    project = Project.objects.filter(name=name)
    if len(project)==0:
        pro = Project.objects.create(name=name, description=description, logo=logo, url=url, admin=user)
    else:
        pro = project[0]
        pro.name = name
        pro.description = description
        pro.logo = logo
        pro.url = url
        pro.admin = user
        pro.save()

    my_path = os.path.join(base_path,folder)
    os.chdir(my_path)

    repo_path = os.path.join(my_path,name)
    if os.path.exists(repo_path):
        return remove_tree(repo_path)

    shell = Shell()
    print 'git clone ' + url + ' ' + name
    shell.run('git clone ' + url + ' ' + name)
    print 'git clone over'

    result = get_repo_info(repo_path,True)
    result['name'] = name
    result['description'] = description
    result['logo'] = logo
    result['url'] = url
    result['admin'] = user.to_obj()
    result['id']= pro.id
    return JsonResponse(result)


def detail(request):
    user_id = int(request.COOKIES['user'])
    folder = User.objects.get(id=user_id).folder
    repo_id = request.GET['repo_id']
    repo = Project.objects.get(id=repo_id)

    is_my_repo = user_id == repo.admin.id


    repo_path = os.path.join(base_path,repo.admin.folder,repo.name)

    result = get_repo_info(repo_path,is_my_repo)
    result['name'] = repo.name
    result['description'] = repo.description
    result['logo'] = repo.logo
    result['url'] = repo.url
    result['admin'] = repo.admin.to_obj()
    result['deploy']=repo.deploy
    return JsonResponse(result)

def branch(request):

    repo = Project.objects.get(id=request.GET['repo_id'])
    user_id = int(request.COOKIES['user'])
    user = User.objects.get(id=user_id)
    if int(repo.admin.id) != user_id:
        return JsonResponse(dict(
            action=False,
            info='you are not the owner of this repo'
        ))
    folder = user.folder
    name = repo.name
    repo_path = os.path.join(base_path, folder, name)
    os.chdir(repo_path)

    shell = Shell()
    shell.run('git pull origin '+request.GET['branch'])
    shell.run('git checkout -b'+request.GET['branch'])

    result = get_repo_info(repo_path,True)
    result['msg1'] = shell.info
    result['msg2'] = shell.err
    result['name'] = repo.name
    result['description'] = repo.description
    result['logo'] = repo.logo
    result['url'] = repo.url
    result['admin'] = repo.admin.to_obj()
    result['deploy']=repo.deploy
    return JsonResponse(result)

def checkout(request):
    repo = Project.objects.get(id=request.GET['repo_id'])
    user_id = int(request.COOKIES['user'])
    user = User.objects.get(id=user_id)
    if int(repo.admin.id) != user_id:
        return JsonResponse(dict(
            action=False,
            info='you are not the owner of this repo'
        ))
    folder = user.folder
    name = repo.name
    repo_path = os.path.join(base_path, folder, name)
    os.chdir(repo_path)

    shell = Shell()
    shell.run('git checkout '+request.GET['branch'])

    r = get_repo_info(repo_path,True)
    shell.run('git pull origin '+r['active_branch'])
    result = get_repo_info(repo_path,True)
    result['msg1'] = shell.info
    result['msg2'] = shell.err
    result['name'] = repo.name
    result['description'] = repo.description
    result['logo'] = repo.logo
    result['url'] = repo.url
    result['admin'] = repo.admin.to_obj()
    result['deploy']=repo.deploy
    return JsonResponse(result)

def pull(request):
    repo = Project.objects.get(id=request.GET['repo_id'])
    user_id = int(request.COOKIES['user'])
    user = User.objects.get(id=user_id)
    if int(repo.admin.id) != user_id:
        return JsonResponse(dict(
            action=False,
            info='you are not the owner of this repo'
        ))
    folder = user.folder
    name = repo.name
    repo_path = os.path.join(base_path, folder, name)
    os.chdir(repo_path)
    print repo_path
    r = get_repo_info(repo_path,True)
    
    shell = Shell()
    shell.run('git pull origin '+r['active_branch'])
    result = get_repo_info(repo_path,True)
    result['msg1'] = shell.info
    result['msg2'] = shell.err
    result['name'] = repo.name
    result['description'] = repo.description
    result['logo'] = repo.logo
    result['url'] = repo.url
    result['admin'] = repo.admin.to_obj()
    result['deploy']=repo.deploy
    return JsonResponse(result)

def reset(request):
    repo = Project.objects.get(id=request.GET['repo_id'])
    user_id = int(request.COOKIES['user'])
    user = User.objects.get(id=user_id)
    folder = User.objects.get(id=user_id).folder
    name = repo.name
    repo_path = os.path.join(base_path, folder, name)
    os.chdir(repo_path)
    if int(repo.admin.id) != user_id:
        return JsonResponse(dict(
            action=False,
            info='you are not the owner of this repo'
        ))

    shell = Shell()
    shell.run('git reset --hard '+request.GET['sha'])

    result = get_repo_info(repo_path,True)
    result['msg1'] = shell.info
    result['msg2'] = shell.err
    result['name'] = repo.name
    result['description'] = repo.description
    result['logo'] = repo.logo
    result['url'] = repo.url
    result['admin'] = repo.admin.to_obj()
    result['deploy']=repo.deploy
    return JsonResponse(result)

def editDeploy(request):
    repo = Project.objects.get(id=request.GET['repo_id'])
    user_id = int(request.COOKIES['user'])
    user = User.objects.get(id=user_id)
    
    folder = User.objects.get(id=user_id).folder
    name = repo.name
    repo_path = os.path.join(base_path, folder, name)
    os.chdir(repo_path)
    if int(repo.admin.id)!=user.id:
        return JsonResponse(dict(
            action=False,
            info='you are not the owner of this repo'
        ))

    repo.deploy = request.GET['deploy']
    result = get_repo_info(repo_path,True)
    repo.save()
    result['name'] = repo.name
    result['description'] = repo.description
    result['logo'] = repo.logo
    result['url'] = repo.url
    result['admin'] = repo.admin.to_obj()
    result['deploy']=repo.deploy
    
    return JsonResponse(result)
    
    

from distutils.dir_util import copy_tree,remove_tree
def deploy(request):



    repo = Project.objects.get(id=request.GET['repo_id'])
    user_id = int(request.COOKIES['user'])
    user = User.objects.get(id=user_id)



    if int(repo.admin.id)!=user.id:
        return JsonResponse(dict(
            action=False,
            info='you are not the owner of this repo'
        ))

    req = requests.get('http://kit.sec.xiaomi.srv/get_team_by_user/?name=' + user.name)
    content = req.json()
    if content.error:
        return JsonResponse(dict(error='user is not a menber of miui'))

    team = content.team

    folder = User.objects.get(id=user_id).folder
    name = repo.name
    repo_path = os.path.join(base_path, folder, name)
    deploy_path = os.path.join(repo_path,repo.deploy)
    online_path = os.path.join('/home/work/www/cdn/secStatic/groups',team.name,user.name,folder,name)

    remove_files=[]
    shell = Shell()
    
    if os.path.exists(online_path):
        remove_tree(online_path)
    copy_tree(deploy_path,os.path.join(online_path,repo.deploy))
    
    return JsonResponse({'action':'successful',online_path:online_path}, safe=False)

def preview(request):
    repo = Project.objects.get(id=request.GET['repo_id'])
    user_id = int(request.COOKIES['user'])

    repo_path = os.path.join(base_path,repo.admin.name,repo.name)
    deploy = repo.deploy

    def getIndex(repo_path, depoly):

        for d in depoly.split(','):
            dir = os.path.join(repo_path, d)
            for root, sub_dirs, files in os.walk(dir):
                print root, files
                if 'index.html' in files:
                    return os.path.join(root, 'index.html')

        return os.path.join(repo_path, depoly.split(',')[0], 'index.html')

    path = getIndex(repo_path, deploy) or 'error'
    path = path.replace(base_path,'')


    return JsonResponse(dict(deploy=repo.deploy,path=path,static='static'))
