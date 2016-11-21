from django.contrib import admin

# Register your models here.
from deploy.models import *

class UsertDesc(admin.ModelAdmin):
    list_display = ('id','name','folder')

class ProjectDesc(admin.ModelAdmin):
    list_display = ('id','name','description','admin')

admin.site.register(User,UsertDesc)
admin.site.register(Project,ProjectDesc)