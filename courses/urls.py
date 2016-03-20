from django.conf.urls import url
from .views import instructor as instructor_views
from .views import student as student_views

app_name = 'courses'

urlpatterns = [
    url(r'^i$', instructor_views.CourseList.as_view(), name='instructor.courses'),
    url(r'^i/course/create/$', instructor_views.CourseCreate.as_view(), name='instructor.courses.create'),
    url(r'^i/course/(?P<pk>[0-9]+)/$', instructor_views.CourseUpdate.as_view(), name='instructor.courses.update'),
    
    url(r'^s$', student_views.CourseList.as_view(), name='student.courses'),
]