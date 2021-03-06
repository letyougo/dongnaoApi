"""dongnaoApi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))

"""
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns 
from django.conf.urls import url,include
from django.contrib import admin
from rest_framework import routers
from django.conf import settings
from appcenter.views import home
from rest_framework_swagger.views import get_swagger_view
from deploy.views import schema_view

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^home$', home),
    url(r'^', include('react1.url')),
    url(r'^', include('file.url')),
    url(r'^', include('deploy.url')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
]
# + static('/static/', document_root=settings.FILE_SYSTEM_DIR)



