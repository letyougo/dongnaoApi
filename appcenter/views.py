from django.shortcuts import render

# Create your views here.
from models import App
def home(request):
    app = App.objects.all()
    return render(request,'homepage.html',dict(app=app))