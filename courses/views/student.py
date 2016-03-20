from django.views import generic
from courses import models

class CourseList(generic.ListView):
    model = models.Course
    template_name = 'courses/student/course_list.html'
    
    def get_queryset(self):
        return self.request.user.enrollments.order_by('-create_date')

class AssignmentList(generic.ListView):
    model = models.Assignment
    template_name = 'courses/student/assignment_list.html'
    
    def get_context_data(self, **kwargs):
        context = super(AssignmentList, self).get_context_data(**kwargs)
        context['course'] = models.Course.objects.get(id=self.kwargs['pk'])
        return context
    
    def get_queryset(self):
        return models.Assignment.objects.filter(course__id=self.kwargs['pk'])