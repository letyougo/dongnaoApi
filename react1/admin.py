from django.contrib import admin

# Register your models here.
from react1.models import *

class StudentDesc(admin.ModelAdmin):
    list_display = ('id','name','age','sex','score','single')

admin.site.register(Student,StudentDesc)