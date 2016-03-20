from django.views import generic
from courses import models

class CourseList(generic.ListView):
    model = models.Course
    template_name = 'courses/student/course_list.html'
    
    def get_queryset(self):
        return self.request.user.enrollments.order_by('-create_date')