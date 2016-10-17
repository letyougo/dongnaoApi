from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
import views




urlpatterns = patterns('',
                       url(r'^react1/student/$', views.StudentList.as_view(), name='student-list'),
                       url(r'^react1/student/(?P<pk>[0-9]+)/$', views.StudentDetail.as_view(), name='student-detail'),
)

urlpatterns = format_suffix_patterns(urlpatterns)