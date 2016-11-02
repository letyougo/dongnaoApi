from django.shortcuts import render

# Create your views here.

from django.http.response import HttpResponse,JsonResponse

from dongnaoApi.settings import FILE_ROOT
import os
import shutil




def get(request):
    path = request.GET['path']
    info = os.listdir(path)

    json = []
    for i in info:
        d = {}
        d['path'] = os.path.join(path,i)
        d['name'] = i
        d['ext'] = os.path.splitext(i).join('.')
        d['isFolder'] = os.path.isdir(d['path'])
        json.append(d)

    return JsonResponse(dict(
        file=json,
        path=path
    ))

def rename(request):
    path = request.GET['path']
    base = os.path.dirname(path)
    name = request.GET['name']
    if not os.path.exists(path):
        return JsonResponse(dict(
            error='file not exist'
        ))

    dist = os.path.join(base,name)
    print dist
    os.rename(path,dist)


    return JsonResponse(dict(
        path=dist,
        name=name
    ))

def mkdir(request):
    path = request.GET['path']
    name = request.GET['name']

    dist = os.path.join(path,name)
    if not os.path.exists(path):
        return JsonResponse(dict(
            error='file not exist'
        ))

    os.mkdir(dist)
    return JsonResponse(dict(
        path=dist,
        name=name
    ))

def remove(request):
    path = request.GET['path']
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