from django.conf.urls import url
from .views import instructor as instructor_views
from .views import student as student_views

app_name = 'courses'

urlpatterns = [
    url(r'^i/$', instructor_views.CourseList.as_view(), name='instructor.courses'),
    url(r'^i/course/create/$', instructor_views.CourseCreate.as_view(), name='instructor.courses.create'),
    url(r'^i/course/(?P<pk>[0-9]+)/$', instructor_views.CourseUpdate.as_view(), name='instructor.courses.update'),
    url(r'^i/course/(?P<pk>[0-9]+)/assignments/$', instructor_views.AssignmentList.as_view(), name='instructor.assignment.list'),
    url(r'^i/course/(?P<pk>[0-9]+)/assignments/create/$', instructor_views.AssignmentCreate.as_view(), name='instructor.assignment.create'),
    url(r'^i/course/assignments/(?P<pk>[0-9]+)/$', instructor_views.AssignmentUpdate.as_view(), name='instructor.assignment.update'),
    
    url(r'^s/$', student_views.CourseList.as_view(), name='student.courses'),
    url(r'^s/course/(?P<pk>[0-9]+)/assignments/$', student_views.AssignmentList.as_view(), name='student.assignment.list'),
    url(r'^s/course/assignments/(?P<pk>[0-9]+)/article/create/$', student_views.ArticleCreate.as_view(), name='student.article.create'),
    url(r'^s/article/(?P<pk>[0-9]+)/$', student_views.ArticleDetail.as_view(), name='student.article.detail'),
]