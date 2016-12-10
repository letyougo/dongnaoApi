from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
import views




urlpatterns = patterns('',
    url(r'^deploy/user/$', views.UserList.as_view(), name='user-list'),
    url(r'^deploy/user/(?P<pk>[0-9]+)/$', views.UserDetail.as_view(), name='user-detail'),

    url(r'^deploy/project/$', views.ProjectList.as_view(), name='project-list'),
    url(r'^deploy/project/(?P<pk>[0-9]+)', views.ProjectDetail.as_view(), name='project-detail'),
    url(r'^deploy/login', views.login,name='deploy-login'),
    url(r'^deploy/logout', views.logout,name='deploy-logout'),
    url(r'^deploy/myproject', views.myproject, name='deploy-create'),
    url(r'^deploy/sync', views.sync, name='deploy-sync'),
    url(r'^deploy/clone', views.clone, name='deploy-clone'),
    url(r'^deploy/detail', views.detail, name='deploy-detail'),
    url(r'^deploy/branch', views.branch, name='deploy-detail'),
    url(r'^deploy/checkout', views.checkout, name='deploy-detail'),
    url(r'^deploy/pull', views.pull, name='deploy-detail'),
    url(r'^deploy/reset', views.reset, name='deploy-detail'),
    url(r'^deploy/init', views.init, name='deploy-detail'),
    url(r'^deploy/editDeploy', views.editDeploy, name='deploy-detail'),
    url(r'^deploy/deploy', views.deploy, name='deploy-detail'),

)

urlpatterns = format_suffix_patterns(urlpatterns)
