from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
import views




urlpatterns = patterns('',
    url(r'^deploy/user/$', views.UserList.as_view(), name='user-list'),
    url(r'^deploy/user/(?P<pk>[0-9]+)/$', views.UserDetail.as_view(), name='user-detail'),

    url(r'^deploy/project/$', views.ProjectList.as_view(), name='project-list'),
    url(r'^deploy/project/(?P<pk>[0-9]+)/$', views.ProjectDetail.as_view(), name='project-detail'),
)

urlpatterns = format_suffix_patterns(urlpatterns)