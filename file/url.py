from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
import views




urlpatterns = patterns('',
    url(r'^file/get/$', views.get),
    url(r'^file/rename/$', views.rename),
    url(r'^file/mkdir/$', views.mkdir),
    url(r'^file/remove/$', views.remove),
    url(r'^file/copy/$', views.copy),
    url(r'^file/move/$', views.cut),
    url(r'^file/upload/$', views.upload),

)

urlpatterns = format_suffix_patterns(urlpatterns)
