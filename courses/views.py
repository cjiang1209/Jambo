from django.views import generic
from django.contrib.auth.decorators import login_required
from courses import models
from helper import auth
from datetime import datetime
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from courses import forms
from django.views.generic.base import View
from guardian.shortcuts import assign_perm
from guardian.mixins import LoginRequiredMixin
from guardian.mixins import PermissionRequiredMixin
from django.core import serializers
from django.views.generic.detail import SingleObjectMixin

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

class CourseList(LoginRequiredMixin, generic.ListView):
    model = models.Course
    template_name = 'courses/course_list.html'
    
    def get_queryset(self):
        if auth.is_student(self.request.user):
            return self.request.user.enrollingCourses.order_by('-create_date')
        elif auth.is_instructor(self.request.user):
            return self.request.user.instructingCourses.order_by('-create_date')
        elif auth.is_administrator(self.request.user):
            return self.model.objects.all()
        else:
            None;

class CourseCreate(generic.CreateView):
    model = models.Course
    form_class = forms.CourseForm
    template_name = 'courses/course_form.html'
    success_url = reverse_lazy('courses:course.list')
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.create_date = datetime.now()
        
        response = super(CourseCreate, self).form_valid(form)
        
        # Assign permissions
        for user in form.instance.instructors.all():
            assign_perm('change_course', user, form.instance)
            assign_perm('view_course', user, form.instance)
        for user in form.instance.students.all():
            assign_perm('view_course', user, form.instance)
        
        return response

class CourseUpdate(PermissionRequiredMixin, generic.UpdateView):
    model = models.Course
    #fields = [ 'title', 'instructors', 'description', 'students' ]
    form_class = forms.CourseForm
    template_name = 'courses/course_form.html'
    success_url = reverse_lazy('courses:course.list')
    permission_required = 'courses.change_course'
    raise_exception = True

class CourseDetail(PermissionRequiredMixin, generic.DetailView):
    model = models.Course
    template_name = 'courses/course_detail.html'
    permission_required = 'courses.view_course'
    raise_exception = True

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

class AssignmentManagementList(generic.ListView):
    model = models.Assignment
    template_name = 'courses/assignment_management_list.html'
    
    def get_context_data(self, **kwargs):
        context = super(AssignmentManagementList, self).get_context_data(**kwargs)
        context['course'] = models.Course.objects.get(id=self.kwargs['pk'])
        return context
    
    def get_queryset(self):
        return models.Assignment.objects.filter(course__id=self.kwargs['pk'])

class AssignmentCreate(generic.CreateView):
    model = models.Assignment
    form_class = forms.AssignmentForm
    template_name = 'courses/assignment_form.html'
    
    def get_success_url(self):
        return reverse_lazy('courses:manage.assignment.list', kwargs={'pk' : self.kwargs['pk']})
    
    def get_context_data(self, **kwargs):
        context = super(AssignmentCreate, self).get_context_data(**kwargs)
        context['course'] = get_object_or_404(models.Course, pk=self.kwargs['pk'])
        return context
    
    def form_valid(self, form):
        form.instance.course = get_object_or_404(models.Course, pk=self.kwargs['pk'])
        form.instance.created_by = models.CustomUser.objects.get(pk = self.request.user.id)
        form.instance.create_date = datetime.now()
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
        return reverse_lazy('courses:manage.assignment.list', kwargs={'pk' : course_id})

# Submission Period

class SubmissionPeriodCreate(AjaxableResponseMixin, generic.CreateView):
    model = models.SubmissionPeriod
    form_class = forms.SubmissionPeriodForm
    success_url = reverse_lazy('courses:course.list')

class SubmissionPeriodDelete(AjaxableResponseMixin, generic.DeleteView):
    model = models.SubmissionPeriod
    success_url = reverse_lazy('courses:course.list')

# Article

class ArticleOriginCreate(generic.CreateView):
    model = models.Article
    form_class = forms.ArticleForm
    template_name = 'courses/article_form.html'

#     def get_initial(self):
#         assignment = get_object_or_404(models.SubmissionPeriod, pk=self.kwargs['pk'])
#         return { 'submission_period' : period }

    def get_context_data(self, **kwargs):
        context = super(ArticleOriginCreate, self).get_context_data(**kwargs)
        assignment = get_object_or_404(models.Assignment, pk=self.kwargs['pk'])
        context['assignment'] = assignment
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.assignment = get_object_or_404(models.Assignment, pk=self.kwargs['pk'])
        current_date = datetime.now()
        form.instance.create_date = current_date
        form.instance.last_modified_date = current_date
        
        #period = get_object_or_404(models.SubmissionPeriod, pk=self.kwargs['pk'])
        #if not period:
        #    return False
        #form.instance.assignment = assignment
        
        return super(ArticleOriginCreate, self).form_valid(form)
    
    def get_success_url(self):
        assignment_id = self.get_form().instance.assignment.id
        return reverse_lazy('courses:article.list', kwargs={'pk' : assignment_id})

class ArticleRevisionCreate(generic.CreateView):
    form_class = forms.ArticleForm
    template_name = 'courses/article_revision_form.html'

    def get_initial(self):
        attempt = get_object_or_404(models.GradingAttempt, pk=self.kwargs['pk'])
        return { 'content': attempt.article.content }

    def get_context_data(self, **kwargs):
        context = super(ArticleRevisionCreate, self).get_context_data(**kwargs)
        context['gradingattempt'] = get_object_or_404(models.GradingAttempt, pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user  
        attempt = get_object_or_404(models.GradingAttempt, pk = self.kwargs['pk'])
        if not attempt:
            return False
        form.instance.parent_attempt = attempt
        form.instance.assignment = attempt.article.assignment
        current_date = datetime.now()
        form.instance.create_date = current_date
        form.instance.last_modified_date = current_date
        
        return super(ArticleRevisionCreate, self).form_valid(form)
    
    def get_success_url(self):
        assignment_id = self.get_form().instance.assignment.id
        return reverse_lazy('courses:article.list', kwargs={'pk' : assignment_id})

class ArticleCreate(generic.base.RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        assignment = get_object_or_404(models.Assignment, pk = self.kwargs['pk'])
        last_article = assignment.article_set.filter(author = self.request.user).order_by('-last_modified_date').first()
        if last_article is None:
            return reverse_lazy('courses:article.origin.create', kwargs = {'pk' : assignment.id})
        elif hasattr(last_article, 'gradingattempt'):
            return reverse_lazy('courses:article.revision.create', kwargs = {'pk' : last_article.gradingattempt.id})
        else:
            return reverse_lazy('courses:article.update', kwargs = {'pk' : last_article.id})

class ArticleUpdate(generic.UpdateView):
    model = models.Article
    form_class = forms.ArticleForm
    template_name = 'courses/article_form.html'
    
    def get_context_data(self, **kwargs):
        context = super(ArticleUpdate, self).get_context_data(**kwargs)
        context['assignment'] = self.get_form().instance.assignment
        return context
    
    def form_valid(self, form):
        form.instance.last_modified_date = datetime.now()
        return super(ArticleUpdate, self).form_valid(form)
    
    def get_success_url(self):
        assignment_id = self.get_form().instance.assignment.id
        return reverse_lazy('courses:article.list', kwargs={'pk' : assignment_id})

class ArticleDetail(generic.DetailView):
    model = models.Article
    template_name = 'courses/article_detail.html'

class ArticleList(generic.ListView):
    model = models.Article
    template_name = 'courses/article_list.html'
    
    def get_context_data(self, **kwargs):
        context = super(ArticleList, self).get_context_data(**kwargs)
        context['assignment'] = models.Assignment.objects.get(id=self.kwargs['pk'])
        return context

    def get_queryset(self):
        return models.Article.objects.filter(assignment__id=self.kwargs['pk']).filter(author=self.request.user).order_by('last_modified_date')

class GradeList(generic.ListView):
    model = models.Article
    template_name = 'courses/grade_list.html'
    
    def get_context_data(self, **kwargs):
        context = super(GradeList, self).get_context_data(**kwargs)
        course = get_object_or_404(models.Course, pk=self.kwargs['pk'])
        context['course'] = course
        return context
    
    def get_queryset(self):
        return models.Article.objects.filter(assignment__course__id = self.kwargs['pk']).order_by('-last_modified_date')

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

# class CommentTemplateList(generic.ListView):
#     model = models.CommentTemplateClass
#     template_name = 'courses/comment_template_list.html'
#      
#     def get_queryset(self):
#         return models.CommentTemplateClass.objects.filter(parent_class__isnull=True)
# 
# class CommentTemplateClassCreate(generic.CreateView):
#     model = models.CommentTemplateClass
#     fields = [ 'title', 'is_end_class', 'parent_class']
#     template_name = 'courses/comment_template_class_form.html'
#     success_url = reverse_lazy('courses:commenttemplate.list')
# 
# class CommentTemplateCreate(generic.CreateView):
#     form_class = forms.CommentTemplateForm
#     template_name = 'courses/comment_template_form.html'
#     success_url = reverse_lazy('courses:commenttemplate.list')

class PredefinedCommentList(generic.TemplateView):
    template_name = 'courses/predefined_comment_list.html'
     
    def get_context_data(self, **kwargs):
        context = super(PredefinedCommentList, self).get_context_data(**kwargs)
        context['categories'] = models.PredefinedCommentCategory.objects.exclude(parent__isnull=False).order_by('create_date')
        return context

class PredefinedCommentCategoryCreate(AjaxableResponseMixin, generic.CreateView):
    model = models.PredefinedCommentCategory
    form_class = forms.PredefinedCommentCategoryForm
    success_url = reverse_lazy('courses:predefined_comment.list')
    
    def form_valid(self, form):
        form.instance.create_date = datetime.now()
        return super(PredefinedCommentCategoryCreate, self).form_valid(form)

class PredefinedCommentSubCategoryList(View):
    def get(self, request, pk):
        sub_categories = models.PredefinedCommentCategory.objects.filter(parent__id = pk).order_by('create_date')
        data = [ { 'id': sub_category.id, 'title': sub_category.title } for sub_category in sub_categories]
        return JsonResponse({ 'list': data})

class PredefinedCommentCategoryDelete(SingleObjectMixin, View):
    model = models.PredefinedCommentCategory
    
    def post(self, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return JsonResponse({ })