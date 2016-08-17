from django.views import generic
from django.contrib.auth.decorators import login_required
from courses import models
from helper import auth
from datetime import datetime
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.core import serializers
from . import forms
from django.views.decorators.http import last_modified
from django.views.generic.base import View

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

# Course

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
    #fields = [ 'title', 'instructors', 'description', 'students' ]
    form_class = forms.CourseForm
    template_name = 'courses/course_form.html'
    success_url = reverse_lazy('courses:course.list')
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.create_date = datetime.now()
        return super(CourseCreate, self).form_valid(form)

class CourseUpdate(generic.UpdateView):
    model = models.Course
    #fields = [ 'title', 'instructors', 'description', 'students' ]
    form_class = forms.CourseForm
    template_name = 'courses/course_form.html'
    success_url = reverse_lazy('courses:course.list')

# Assignment

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
    #fields = [ 'title', 'course', 'description', 'due_date' ]
    form_class = forms.AssignmentForm
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
    #fields = [ 'title', 'course', 'description', 'due_date' ]
    form_class = forms.AssignmentForm
    template_name = 'courses/assignment_form.html'

    def get_context_data(self, **kwargs):
        context = super(AssignmentUpdate, self).get_context_data(**kwargs)
        context['course'] = self.get_form().instance.course
        return context

    def get_success_url(self):
        course_id = self.get_form().instance.course.id
        return reverse_lazy('courses:assignment.list', kwargs={'pk' : course_id})


# Submission Period

class SubmissionPeriodCreate(AjaxableResponseMixin, generic.CreateView):
    model = models.SubmissionPeriod
    fields = [ 'title', 'start_date', 'end_date', 'assignment' ]
    success_url = reverse_lazy('courses:course.list')

class SubmissionPeriodDelete(AjaxableResponseMixin, generic.DeleteView):
    model = models.SubmissionPeriod
    success_url = reverse_lazy('courses:course.list')

# Article

class ArticleCreate(generic.CreateView):
    model = models.Article
    form_class = forms.ArticleForm
    template_name = 'courses/article_form.html'

    def get_initial(self):
        period = get_object_or_404(models.SubmissionPeriod, pk=self.kwargs['pk'])
        return { 'submission_period' : period }

    def get_context_data(self, **kwargs):
        context = super(ArticleCreate, self).get_context_data(**kwargs)
        period = get_object_or_404(models.SubmissionPeriod, pk=self.kwargs['pk'])
        context['assignment'] = period.assignment
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        current_date = datetime.now()
        form.instance.create_date = current_date
        form.instance.last_modified_date = current_date
        
        #period = get_object_or_404(models.SubmissionPeriod, pk=self.kwargs['pk'])
        #if not period:
        #    return False
        #form.instance.assignment = assignment
        
        return super(ArticleCreate, self).form_valid(form)

class ArticleUpdate(generic.UpdateView):
    model = models.Article
    form_class = forms.ArticleForm
    template_name = 'courses/article_form.html'
    
    def get_context_data(self, **kwargs):
        context = super(ArticleUpdate, self).get_context_data(**kwargs)
        context['assignment'] = self.get_form().instance.submission_period.assignment
        return context
    
    def form_valid(self, form):
        form.instance.last_modified_date = datetime.now()
        return super(ArticleUpdate, self).form_valid(form)
    
    def get_success_url(self):
        course_id = self.get_form().instance.submission_period.assignment.course.id
        return reverse_lazy('courses:assignment.list', kwargs={'pk' : course_id})

class ArticleFromGradingAttemptCreate(generic.CreateView):
    form_class = forms.ArticleForm
    template_name = 'courses/article_from_grading_attempt_form.html'

    def get_initial(self):
        attempt = get_object_or_404(models.GradingAttempt, pk=self.kwargs['pk'])
        return { 'content': attempt.article.content }

    def get_context_data(self, **kwargs):
        context = super(ArticleFromGradingAttemptCreate, self).get_context_data(**kwargs)
        context['gradingattempt'] = get_object_or_404(models.GradingAttempt, pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.create_date = datetime.now()
        
        attempt = get_object_or_404(models.GradingAttempt, pk = self.kwargs['pk'])
        if not attempt:
            return False
        form.instance.parent_attempt = attempt
        form.instance.assignment = attempt.article.assignment
        
        return super(ArticleFromGradingAttemptCreate, self).form_valid(form)

class ArticleDetail(generic.DetailView):
    model = models.Article
    template_name = 'courses/article_detail.html'

# Grading Attempt

class GradingAttemptCreate(generic.base.RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        article = get_object_or_404(models.Article, pk = self.kwargs['pk'])
        if hasattr(article, 'gradingattempt'):
            attempt = article.gradingattempt
        else:
            current_date = datetime.now()
            attempt = models.GradingAttempt(article = article,
                content = article.content,
                create_date = current_date,
                last_modified_date = current_date)
            attempt.save()
        return reverse_lazy('courses:grading_attempt.update', kwargs = {'pk' : attempt.id})

class GradingAttemptDisplay(generic.DetailView):
    model = models.GradingAttempt
    template_name = 'courses/grading_attempt_form.html'
    
    def get_context_data(self, **kwargs):
        context = super(GradingAttemptDisplay, self).get_context_data(**kwargs)
        context['form'] = forms.GradingAttemptGradeForm(instance = get_object_or_404(models.GradingAttempt, pk = self.kwargs['pk']))
        return context

class GradingAttemptGradeUpdate(AjaxableResponseMixin, generic.UpdateView):
    model = models.GradingAttempt
    form_class = forms.GradingAttemptGradeForm
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(GradingAttemptGradeUpdate, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.last_modified_date = datetime.now()
        print(form.instance.grade)
        return super(GradingAttemptGradeUpdate, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('courses:grading_attempt.update', kwargs = {'pk': self.object.pk})

class GradingAttemptUpdate(View):
    def get(self, request, *args, **kwargs):
        view = GradingAttemptDisplay.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = GradingAttemptGradeUpdate.as_view()
        return view(request, *args, **kwargs)

class GradingAttemptContentUpdate(AjaxableResponseMixin, generic.UpdateView):
    model = models.GradingAttempt
    fields = [ 'content' ]
    
    def form_valid(self, form):
        form.instance.last_modified_date = datetime.now()
        print(datetime.now())
        return super(GradingAttemptContentUpdate, self).form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('courses:grading_attempt.update', kwargs={'pk' : self.kwargs['pk']})

class GradingAttemptDetail(generic.DetailView):
    model = models.GradingAttempt
    template_name = 'courses/grading_attempt_detail.html'

# Comment

class CommentCreate(AjaxableResponseMixin, generic.CreateView):
    model = models.Comment
    fields = [ 'content', 'attempt' ]
    success_url = reverse_lazy('courses:course.list')
    
    def form_valid(self, form):
        form.instance.create_date = datetime.now()
        return super(CommentCreate, self).form_valid(form)

class CommentDetail(generic.DetailView):
    model = models.Comment
    fields = [ 'content', 'create_date' ]
    
    #def get_object(self, queryset=None):
    #    return self.model.objects.get(pk=self.kwargs['id'])
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        data = {
            "comment_id": self.object.id,
            "content": self.object.content,
            "create_date": self.object.create_date
        }
        return JsonResponse(data)

class CommentDelete(AjaxableResponseMixin, generic.DeleteView):
    model = models.Comment
    success_url = reverse_lazy('courses:course.list')

class CommentTemplateList(generic.ListView):
    model = models.CommentTemplateClass
    template_name = 'courses/comment_template_list.html'
     
    def get_queryset(self):
        return models.CommentTemplateClass.objects.filter(parent_class__isnull=True)

class CommentTemplateClassCreate(generic.CreateView):
    model = models.CommentTemplateClass
    fields = [ 'title', 'is_end_class', 'parent_class']
    template_name = 'courses/comment_template_class_form.html'
    success_url = reverse_lazy('courses:commenttemplate.list')

class CommentTemplateCreate(generic.CreateView):
    form_class = forms.CommentTemplateForm
    template_name = 'courses/comment_template_form.html'
    success_url = reverse_lazy('courses:commenttemplate.list')