from django.views import generic
from courses import models
from datetime import datetime
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404
from courses import forms

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

class ArticleCreate(generic.CreateView):
    form_class = forms.ArticleForm
    template_name = 'courses/student/article_form.html'

    def get_initial(self):
        assignment = get_object_or_404(models.Assignment, pk=self.kwargs['pk'])
        return { 'assignment' : assignment }

    def get_context_data(self, **kwargs):
        context = super(ArticleCreate, self).get_context_data(**kwargs)
        context['assignment'] = get_object_or_404(models.Assignment, pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.create_date = datetime.now()
        return super(ArticleCreate, self).form_valid(form)

class ArticleDetail(generic.DetailView):
    model = models.Article
    template_name = 'courses/student/article_detail.html'
