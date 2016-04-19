from django.conf.urls import url
from .views import *
# from .views import instructor as instructor_views
# from .views import student as student_views

app_name = 'courses'

urlpatterns = [
    url(r'^$', CourseList.as_view(), name='course.list'),
    url(r'^course/create/$', CourseCreate.as_view(), name='course.create'),
    url(r'^course/(?P<pk>[0-9]+)/update$', CourseUpdate.as_view(), name='course.update'),
    url(r'^course/(?P<pk>[0-9]+)/$', AssignmentList.as_view(), name='assignment.list'),
    url(r'^course/(?P<pk>[0-9]+)/assignment/create/$', AssignmentCreate.as_view(), name='assignment.create'),
    url(r'^assignment/(?P<pk>[0-9]+)/update$', AssignmentUpdate.as_view(), name='assignment.update'),
    url(r'^assignment/(?P<pk>[0-9]+)/article/create/$', ArticleCreate.as_view(), name='article.create'),
    url(r'^article/(?P<pk>[0-9]+)/$', ArticleDetail.as_view(), name='article.detail'),
    
#     url(r'^i/$', instructor_views.CourseList.as_view(), name='instructor.courses'),
#     url(r'^i/course/create/$', instructor_views.CourseCreate.as_view(), name='instructor.courses.create'),
#     url(r'^i/course/(?P<pk>[0-9]+)/$', instructor_views.CourseUpdate.as_view(), name='instructor.courses.update'),
#     url(r'^i/course/(?P<pk>[0-9]+)/assignments/$', instructor_views.AssignmentList.as_view(), name='instructor.assignment.list'),
#     url(r'^i/course/(?P<pk>[0-9]+)/assignments/create/$', instructor_views.AssignmentCreate.as_view(), name='instructor.assignment.create'),
#     url(r'^i/course/assignments/(?P<pk>[0-9]+)/$', instructor_views.AssignmentUpdate.as_view(), name='instructor.assignment.update'),
#     
#     url(r'^s/$', student_views.CourseList.as_view(), name='student.courses'),
#     url(r'^s/course/(?P<pk>[0-9]+)/assignments/$', student_views.AssignmentList.as_view(), name='student.assignment.list'),
#     url(r'^s/course/assignments/(?P<pk>[0-9]+)/article/create/$', student_views.ArticleCreate.as_view(), name='student.article.create'),
#     url(r'^s/article/(?P<pk>[0-9]+)/$', student_views.ArticleDetail.as_view(), name='student.article.detail'),
]