from django.shortcuts import render

# Create your views here.

from django.http.response import HttpResponse,JsonResponse

from dongnaoApi.settings import FILE_ROOT,FILE_SYSTEM_DIR
import os
import shutil


def filter(path):
    if path == '':
       path = '/'
    if path[0] == '/':
	path = path[1:]
    return os.path.join(FILE_SYSTEM_DIR,path)


def get(request):
    path = request.GET['path']
    p = filter(path)	
    info = os.listdir(p)

    json = []
    for i in info:
        d = {}
        d['path'] = os.path.join(path,i)
        d['name'] = i
        d['ext'] = os.path.splitext(i)[1]
        d['isFolder'] = os.path.isdir(filter(d['path']))
        json.append(d)

    return JsonResponse(dict(
        file=json,
        path=path
    ))

def rename(request):
    path = request.GET['path']
    path = filter(path)
    base = os.path.dirname(path)
    name = request.GET['name']
    if not os.path.exists(path):
        return JsonResponse(dict(
            error='file not exist'
        ))

    dist = os.path.join(base,name)
    os.rename(path,dist)

    
    return JsonResponse(dict(
        path=dist.replace('/home/student/static/',''),
	name=name,
	ext=os.path.splitext(name)[1],
	isFolder=os.path.isdir(dist)
    ))

def mkdir(request):
    path = request.GET['path']
    path = filter(path)
    name = request.GET['name']

    dist = os.path.join(path,name)
    if not os.path.exists(path):
        return JsonResponse(dict(
            error='file not exist'
        ))

    os.mkdir(dist)
    return JsonResponse(dict(
        path=dist.replace('/home/student/static/',''),
	name=name,
	ext=os.path.splitext(name)[1],
	isFolder=os.path.isdir(dist)
    ))

def remove(request):
    path = request.GET['path']
    path = filter(path)
    if not os.path.exists(path):
        return JsonResponse(dict(
            error='file not exist'
        ))
    if os.path.isdir(path):
        info = shutil.rmtree(path)
    else:
        info = os.remove(path)
    return JsonResponse(dict(
        success='delete files successful'
    ))
