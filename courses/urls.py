from django.conf.urls import url
from .views import *
# from .views import instructor as instructor_views
# from .views import student as student_views

app_name = 'courses'

urlpatterns = [
    url(r'^$', CourseList.as_view(), name='course.list'),
    url(r'^course/create/$', CourseCreate.as_view(), name='course.create'),
    url(r'^course/(?P<pk>[0-9]+)/update/$', CourseUpdate.as_view(), name='course.update'),
    url(r'^course/(?P<pk>[0-9]+)/$', CourseDetail.as_view(), name='course.detail'),
    
    url(r'^course/(?P<pk>[0-9]+)/assignment$', AssignmentList.as_view(), name='assignment.list'),
    
    url(r'^course/(?P<pk>[0-9]+)/manage/assignment$', AssignmentManagementList.as_view(), name='manage.assignment.list'),
    url(r'^course/(?P<pk>[0-9]+)/assignment/create/$', AssignmentCreate.as_view(), name='assignment.create'),
    
    url(r'^assignment/(?P<pk>[0-9]+)/update/$', AssignmentUpdate.as_view(), name='assignment.update'),
    
    url(r'^submissionperiod/create/$', SubmissionPeriodCreate.as_view(), name='submission_period.create'),
    url(r'^submissionperiod/delete/$', SubmissionPeriodDelete.as_view(), name='submission_period.delete'),
    url(r'^submissionperiod/delete/(?P<pk>[0-9]+)/$', SubmissionPeriodDelete.as_view(), name='submission_period.delete'),
    
    url(r'^assignment/(?P<pk>[0-9]+)/article/$', ArticleList.as_view(), name='article.list'),
    
    url(r'^assignment/(?P<pk>[0-9]+)/article/create/$', ArticleCreate.as_view(), name='article.create'),
    url(r'^assignment/(?P<pk>[0-9]+)/article/origin/create/$', ArticleOriginCreate.as_view(), name='article.origin.create'),
    url(r'^gradingattempt/(?P<pk>[0-9]+)/article/create/$', ArticleRevisionCreate.as_view(), name='article.revision.create'),
    #url(r'^submissionperiod/(?P<pk>[0-9]+)/article/create/$', ArticleCreate.as_view(), name='article.create'),
    url(r'^article/(?P<pk>[0-9]+)/update/$', ArticleUpdate.as_view(), name='article.update'),
    url(r'^article/(?P<pk>[0-9]+)/$', ArticleDetail.as_view(), name='article.detail'),
    
    url(r'^article/(?P<pk>[0-9]+)/gradingattempt/create/$', GradingAttemptCreate.as_view(), name='grading_attempt.create'),
    url(r'^gradingattempt/(?P<pk>[0-9]+)/update/$', GradingAttemptUpdate.as_view(), name='grading_attempt.update'),
    url(r'^gradingattempt/(?P<pk>[0-9]+)/updatecontent/$', GradingAttemptContentUpdate.as_view(), name='grading_attempt.update_content'),
    url(r'^gradingattempt/(?P<pk>[0-9]+)/$', GradingAttemptDetail.as_view(), name='grading_attempt.detail'),
    
    url(r'^comment/create/$', CommentCreate.as_view(), name='comment.create'),
    url(r'^comment/$', CommentDetail.as_view(), name='comment.detail'),
    url(r'^comment/(?P<pk>[0-9]+)/$', CommentDetail.as_view(), name='comment.detail'),
    url(r'^comment/delete/$', CommentDelete.as_view(), name='comment.delete'),
    url(r'^comment/delete/(?P<pk>[0-9]+)/$', CommentDelete.as_view(), name='comment.delete'),
    
    url(r'^commenttemplate/$', CommentTemplateList.as_view(), name='commenttemplate.list'),
    url(r'^commenttemplateclass/create/$', CommentTemplateClassCreate.as_view(), name='commenttemplateclass.create'),
    url(r'^commenttemplate/create/$', CommentTemplateCreate.as_view(), name='commenttemplate.create'),
    
    url(r'^course/(?P<pk>[0-9]+)/grade/$', GradeList.as_view(), name='grade.list'),
    
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