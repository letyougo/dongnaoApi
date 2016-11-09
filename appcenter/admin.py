from django.contrib import admin

# Register your models here.
from django.contrib import admin

# Register your models here.
from models import App

class AppDesc(admin.ModelAdmin):
    list_display = ('id','student','url','description')

admin.site.register(App,AppDesc)