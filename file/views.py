# coding=utf-8
from django.shortcuts import render

# Create your views here.

from django.http.response import HttpResponse,JsonResponse

from dongnaoApi.settings import FILE_ROOT,FILE_SYSTEM_DIR
import os
import shutil

import sys
reload(sys)
sys.setdefaultencoding("utf-8")
    
def filter(path):
   if not path:
      path = '/'
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
	print path,i,'hello'
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
def copy(request):
    old_path = request.GET['old_path']
    old_path = filter(old_path)
    new_path = request.GET['new_path']
    new_path = filter(new_path)

    if os.path.exists(new_path):
        return JsonResponse(dict(
                error='file exists'
            ))

    if not os.path.isdir(old_path):
	fn = shutil.copyfile
    else:
	fn = shutil.copytree

    fn(old_path,new_path)
    p = new_path.split('/')
    name = p[len(p)-1]
    return JsonResponse(dict(
	path = new_path.replace('/home/student/static/',''),
	name = name,
	ext=os.path.splitext(new_path)[1],
	isFolder = os.path.isdir(new_path)
))

def cut(request):
    old_path = request.GET['old_path']
    old_path = filter(old_path)
    new_path = request.GET['new_path']
    new_path = filter(new_path)

    if os.path.exists(new_path):
        return JsonResponse(dict(
                error='file exists'
            ))

    if not os.path.isdir(old_path):
	copy = shutil.copyfile
        rm = os.remove
    else:
	copy = shutil.copytree
        rm = shutil.rmtree

    copy(old_path,new_path)
    rm(old_path)
    p = new_path.split('/')
    name = p[len(p)-1]
    return JsonResponse(dict(
	path = new_path.replace('/home/student/static/',''),
	name = name,
	ext=os.path.splitext(new_path)[1],
	isFolder = os.path.isdir(new_path)
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

def upload(request):
    files = request.FILES.getlist('cloud')
    print files
    p = filter(request.POST['path'])
    print p
    print files
    for f in files:
        print f   
        
        target = open(p+'/'+f.name,'wb+')
        if f.multiple_chunks():
            for chunk in f.chunks():
                target.write(chunk)
        else:
            chunk = f.read()
            target.write(chunk)
        target.close()

    return HttpResponse('hello world')
