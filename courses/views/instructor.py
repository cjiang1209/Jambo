from django.views import generic
from courses import models
from datetime import datetime
from django.core.urlresolvers import reverse_lazy

class CourseList(generic.ListView):
    model = models.Course
    template_name = 'courses/instructor/course_list.html'
    
    def get_queryset(self):
        return self.request.user.instructions.order_by('-create_date')

class CourseCreate(generic.CreateView):
    model = models.Course
    fields = [ 'title', 'instructors', 'description', 'students' ]
    template_name = 'courses/instructor/course_form.html'
    success_url = reverse_lazy('courses:instructor.courses')
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.create_date = datetime.now()
        return super(CourseCreate, self).form_valid(form)

class CourseUpdate(generic.UpdateView):
    model = models.Course
    fields = [ 'title', 'instructors', 'description', 'students' ]
    template_name = 'courses/instructor/course_form.html'
    success_url = reverse_lazy('courses:instructor.courses')
    