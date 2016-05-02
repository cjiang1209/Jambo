from django.views import generic
from django.contrib.auth.decorators import login_required
from courses import models
from helper import auth
from datetime import datetime
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from . import forms

class AjaxableResponseMixin(object):
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """
    def form_invalid(self, form):
        response = super(AjaxableResponseMixin, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super(AjaxableResponseMixin, self).form_valid(form)
        if self.request.is_ajax():
            data = {
                'id': self.object.pk,
            }
            return JsonResponse(data)
        else:
            return response

class CourseList(generic.ListView):
    model = models.Course
    template_name = 'courses/course_list.html'
    
    def get_queryset(self):
        if auth.is_student(self.request.user):
            return self.request.user.enrollments.order_by('-create_date')
        elif auth.is_instructor(self.request.user):
            return self.request.user.instructions.order_by('-create_date')
        else:
            return None

class CourseCreate(generic.CreateView):
    model = models.Course
    fields = [ 'title', 'instructors', 'description', 'students' ]
    template_name = 'courses/course_form.html'
    success_url = reverse_lazy('courses:course.list')
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.create_date = datetime.now()
        return super(CourseCreate, self).form_valid(form)

class CourseUpdate(generic.UpdateView):
    model = models.Course
    fields = [ 'title', 'instructors', 'description', 'students' ]
    template_name = 'courses/course_form.html'
    success_url = reverse_lazy('courses:course.list')

class AssignmentList(generic.ListView):
    model = models.Assignment
    template_name = 'courses/assignment_list.html'
    
    def get_context_data(self, **kwargs):
        context = super(AssignmentList, self).get_context_data(**kwargs)
        context['course'] = models.Course.objects.get(id=self.kwargs['pk'])
        return context
    
    def get_queryset(self):
        return models.Assignment.objects.filter(course__id=self.kwargs['pk'])

class AssignmentCreate(generic.CreateView):
    model = models.Assignment
    fields = [ 'title', 'course', 'description', 'due_date' ]
    template_name = 'courses/assignment_form.html'
    
    def get_success_url(self):
        return reverse_lazy('courses:assignment.list', kwargs={'pk' : self.kwargs['pk']})
    
    def get_initial(self):
        course = get_object_or_404(models.Course, pk=self.kwargs['pk'])
        return { 'course' : course }
    
    def get_context_data(self, **kwargs):
        context = super(AssignmentCreate, self).get_context_data(**kwargs)
        context['course'] = get_object_or_404(models.Course, pk=self.kwargs['pk'])
        return context
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.create_date = datetime.now()
        #form.instance.course = models.Course.objects.get(id=self.kwargs['pk'])
        return super(AssignmentCreate, self).form_valid(form)

class AssignmentUpdate(generic.UpdateView):
    model = models.Assignment
    fields = [ 'title', 'course', 'description', 'due_date' ]
    template_name = 'courses/assignment_form.html'

    def get_context_data(self, **kwargs):
        context = super(AssignmentUpdate, self).get_context_data(**kwargs)
        context['course'] = self.get_form().instance.course
        return context

    def get_success_url(self):
        course_id = self.get_form().instance.course.id
        return reverse_lazy('courses:assignment.list', kwargs={'pk' : course_id})

class ArticleCreate(generic.CreateView):
    form_class = forms.ArticleForm
    template_name = 'courses/article_form.html'

#     def get_initial(self):
#         assignment = get_object_or_404(models.Assignment, pk=self.kwargs['pk'])
#         return { 'assignment' : assignment }

    def get_context_data(self, **kwargs):
        context = super(ArticleCreate, self).get_context_data(**kwargs)
        context['assignment'] = get_object_or_404(models.Assignment, pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.create_date = datetime.now()
        
        assignment = get_object_or_404(models.Assignment, pk=self.kwargs['pk'])
        if not assignment:
            return False
        form.instance.assignment = assignment
        
        return super(ArticleCreate, self).form_valid(form)

class ArticleDetail(generic.DetailView):
    model = models.Article
    template_name = 'courses/article_detail.html'

class GradingAttemptCreate(generic.base.RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        article = get_object_or_404(models.Article, pk=self.kwargs['pk'])
        attempt = models.GradingAttempt(article=article, content=article.content,
            create_date=datetime.now(), last_modified_date=datetime.now())
        attempt.save()
        return reverse_lazy('courses:grading_attempt.update', kwargs={'pk' : attempt.id})

class GradingAttemptUpdate(generic.DetailView):
    model = models.GradingAttempt
    template_name = 'courses/grading_attempt_form.html'

class GradingAttemptContentUpdate(AjaxableResponseMixin, generic.UpdateView):
    model = models.GradingAttempt
    fields = [ 'content' ]
    
    def form_valid(self, form):
        form.instance.last_modified_date = datetime.now()
        return super(GradingAttemptContentUpdate, self).form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('courses:grading_attempt.update', kwargs={'pk' : self.kwargs['pk']})

class CommentCreate(AjaxableResponseMixin, generic.CreateView):
    model = models.Comment
    fields = [ 'content', 'attempt' ]
    
    def form_valid(self, form):
        form.instance.create_date = datetime.now()
        return super(CommentCreate, self).form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('courses:course.list')