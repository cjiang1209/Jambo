from django.views import generic
from django.contrib.auth.decorators import login_required, permission_required
from courses import models
from helper import auth
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from courses import forms
from django.views.generic.base import View, TemplateView
from guardian.shortcuts import assign_perm, remove_perm
from guardian.mixins import LoginRequiredMixin
from guardian.mixins import PermissionRequiredMixin
from django.views.generic.detail import SingleObjectMixin
import os
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.http import HttpResponse
from django.utils import timezone
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

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

class InstructCoursePermissionRequiredMixin(PermissionRequiredMixin):
    permission_required = 'courses.instruct_course'
    raise_exception = True
    
    def get_permission_object(self):
        return get_object_or_404(models.Course, pk=self.kwargs['pk'])

class EnrollCoursePermissionRequiredMixin(PermissionRequiredMixin):
    permission_required = 'courses.enroll_course'
    raise_exception = True
    
    def get_permission_object(self):
        return get_object_or_404(models.Course, pk=self.kwargs['pk'])

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
        form.instance.create_date = timezone.now()
        
        response = super(CourseCreate, self).form_valid(form)
        
        # Assign permissions
        for user in form.instance.instructors.all():
            assign_perm('change_course', user, form.instance)
            assign_perm('view_course', user, form.instance)
            assign_perm('instruct_course', user, form.instance)
        for user in form.instance.students.all():
            assign_perm('view_course', user, form.instance)
            assign_perm('enroll_course', user, form.instance)
        
        return response

class CourseUpdate(PermissionRequiredMixin, generic.UpdateView):
    model = models.Course
    form_class = forms.CourseForm
    template_name = 'courses/course_form.html'
    success_url = reverse_lazy('courses:course.list')
    permission_required = 'courses.change_course'
    raise_exception = True
    
    def form_valid(self, form):
        old_course = models.Course.objects.get(pk=form.instance.pk)
        initial_instructors = list(old_course.instructors.all())
        initial_students = list(old_course.students.all())
        
        response = super(CourseUpdate, self).form_valid(form)
        
        instructors = form.instance.instructors.all()
        students = form.instance.students.all()
        
        # print(initial_instructors)
        # print(instructors)
        # print(initial_students)
        # print(students)
        
        # Revoke permissions
        for user in initial_instructors:
            remove_perm('change_course', user, form.instance)
            remove_perm('view_course', user, form.instance)
            remove_perm('instruct_course', user, form.instance)
        for user in initial_students:
            remove_perm('view_course', user, form.instance)
            remove_perm('enroll_course', user, form.instance)
        
        # Assign permissions
        for user in instructors:
            assign_perm('change_course', user, form.instance)
            assign_perm('view_course', user, form.instance)
            assign_perm('instruct_course', user, form.instance)
        for user in students:
            assign_perm('view_course', user, form.instance)
            assign_perm('enroll_course', user, form.instance)
        
        return response

class CourseDetail(PermissionRequiredMixin, generic.DetailView):
    model = models.Course
    template_name = 'courses/course_detail.html'
    permission_required = 'courses.view_course'
    raise_exception = True

# Assignment

class AssignmentList(EnrollCoursePermissionRequiredMixin, generic.ListView):
    model = models.Assignment
    template_name = 'courses/assignment_list.html'
    
    def get_context_data(self, **kwargs):
        context = super(AssignmentList, self).get_context_data(**kwargs)
        context['course'] = models.Course.objects.get(id=self.kwargs['pk'])
        return context
    
    def get_queryset(self):
        return models.Assignment.objects.filter(course__id=self.kwargs['pk'])

class AssignmentManagementList(InstructCoursePermissionRequiredMixin, generic.ListView):
    model = models.Assignment
    template_name = 'courses/assignment_management_list.html'
    
    def get_context_data(self, **kwargs):
        context = super(AssignmentManagementList, self).get_context_data(**kwargs)
        context['course'] = models.Course.objects.get(id=self.kwargs['pk'])
        return context
    
    def get_queryset(self):
        return models.Assignment.objects.filter(course__id=self.kwargs['pk'])

class AssignmentCreate(InstructCoursePermissionRequiredMixin, generic.CreateView):
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
        form.instance.create_date = timezone.now()
        return super(AssignmentCreate, self).form_valid(form)

class AssignmentUpdate(InstructCoursePermissionRequiredMixin, generic.UpdateView):
    model = models.Assignment
    form_class = forms.AssignmentForm
    template_name = 'courses/assignment_form.html'
    
    def get_permission_object(self):
        #return self.get_form().instance.course
        return self.get_object().course

    def get_context_data(self, **kwargs):
        context = super(AssignmentUpdate, self).get_context_data(**kwargs)
        context['course'] = self.get_object().course
        return context

    def get_success_url(self):
        course_id = self.get_object().course.id
        return reverse_lazy('courses:manage.assignment.list', kwargs={'pk' : course_id})

# Submission Period

# class SubmissionPeriodCreate(AjaxableResponseMixin, generic.CreateView):
#     model = models.SubmissionPeriod
#     form_class = forms.SubmissionPeriodForm
#     success_url = reverse_lazy('courses:course.list')
# 
# class SubmissionPeriodDelete(AjaxableResponseMixin, generic.DeleteView):
#     model = models.SubmissionPeriod
#     success_url = reverse_lazy('courses:course.list')

# Stage

class StageCreate(AjaxableResponseMixin, generic.CreateView):
    model = models.Stage
    form_class = forms.StageForm
    success_url = reverse_lazy('courses:course.list')

class StageDelete(SingleObjectMixin, View):
    model = models.Stage

    def post(self, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return JsonResponse({ })

# Article

class ArticleOriginCreate(EnrollCoursePermissionRequiredMixin, generic.CreateView):
    model = models.Article
    form_class = forms.ArticleForm
    template_name = 'courses/article_form.html'

    def get_permission_object(self):
        return get_object_or_404(models.Assignment, pk=self.kwargs['pk']).course

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
        current_date = timezone.now()
        form.instance.create_date = current_date
        form.instance.last_modified_date = current_date
        form.parent_attempt = None
        form.instance.number = 1
        
        stage = form.instance.assignment.active_stage()
        if stage is None:
            return HttpResponse(status=400)
        elif current_date < stage.start_date or current_date > stage.grace_period_end_date:
            return HttpResponse(status=400)
        
        form.instance.is_late = (current_date > stage.end_date)
        
        #period = get_object_or_404(models.SubmissionPeriod, pk=self.kwargs['pk'])
        #if not period:
        #    return False
        #form.instance.assignment = assignment
        
        response = super(ArticleOriginCreate, self).form_valid(form)
        
        assign_perm('articles.change_article', self.request.user, form.instance)
        
        return response
    
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
        current_date = timezone.now()
        form.instance.create_date = current_date
        form.instance.last_modified_date = current_date
        form.instance.number = attempt.article.number + 1
        
        stage = form.instance.assignment.active_stage()
        if stage is None:
            return HttpResponse(status=400)
        elif current_date < stage.start_date or current_date > stage.grace_period_end_date:
            return HttpResponse(status=400)
        
        form.instance.is_late = (current_date > stage.end_date)
        
        response = super(ArticleRevisionCreate, self).form_valid(form)
        
        assign_perm('articles.change_article', self.request.user, form.instance)
        
        return response
    
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
        current_date = timezone.now()
        form.instance.last_modified_date = current_date
        
        stage = form.instance.assignment.active_stage()
        if stage is None:
            return HttpResponse(status=400)
        elif current_date < stage.start_date or current_date > stage.grace_period_end_date:
            return HttpResponse(status=400)
        
        form.instance.is_late = (current_date > stage.end_date)
        
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
        
        assignment = models.Assignment.objects.get(id=self.kwargs['pk'])
        context['assignment'] = assignment
        
        try:
            last_grading_attempt = models.GradingAttempt.objects.filter(article__assignment__id = assignment.id,
                article__author=self.request.user).latest('create_date')
            context['last_grading_attempt'] = last_grading_attempt
        except models.GradingAttempt.DoesNotExist:
            context['last_grading_attempt'] = None
        
        active_stage = assignment.active_stage()
        if active_stage is not None:
            # assignment has an active stage
            try:
                active_article = models.Article.objects.get(assignment__id = assignment.id,
                    author = self.request.user,
                    create_date__gte = active_stage.start_date,
                    create_date__lte = active_stage.grace_period_end_date)
                context['active_article'] = active_article
            except models.Article.DoesNotExist:
                context['active_article'] = None
        else:
            context['active_article'] = None
        
        return context

    def get_queryset(self):
        return models.Article.objects.filter(assignment__id = self.kwargs['pk'],
            author = self.request.user).order_by('-create_date')

class GradeList(InstructCoursePermissionRequiredMixin, generic.ListView):
    model = models.Article
    template_name = 'courses/grade_list.html'
    
    def get_context_data(self, **kwargs):
        context = super(GradeList, self).get_context_data(**kwargs)
        context['course'] = get_object_or_404(models.Course, pk=self.kwargs['pk'])
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
            current_date = timezone.now()
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
        form.instance.last_modified_date = timezone.now()
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
        form.instance.last_modified_date = timezone.now()
        return super(GradingAttemptContentUpdate, self).form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('courses:grading_attempt.update', kwargs={'pk' : self.kwargs['pk']})

class GradingAttemptDetail(generic.DetailView):
    model = models.GradingAttempt
    template_name = 'courses/grading_attempt_detail.html'

class GradingAttemptToggleVisibility(AjaxableResponseMixin, View):
    def post(self, request, *args, **kwargs):
        try:
            attempt = models.GradingAttempt.objects.get(pk=kwargs['pk'])
            attempt.visible = not attempt.visible
            attempt.save()
            return JsonResponse({'visible': attempt.visible})
        except ObjectDoesNotExist:
            return JsonResponse({'visible': False})

# Comment

class CommentCreate(AjaxableResponseMixin, generic.CreateView):
    model = models.Comment
    fields = [ 'content', 'attempt' ]
    success_url = reverse_lazy('courses:course.list')
    
    def form_valid(self, form):
        form.instance.create_date = timezone.now()
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

class PredefinedCommentBrowse(generic.TemplateView):
    template_name = 'courses/predefined_comment_browse.html'
     
    def get_context_data(self, **kwargs):
        context = super(PredefinedCommentBrowse, self).get_context_data(**kwargs)
        context['categories'] = models.PredefinedCommentCategory.objects.exclude(parent__isnull=False).order_by('create_date')
        context['CKEditorFuncNum'] = self.request.GET.get('CKEditorFuncNum')
        return context
    
    def post(self, *args, **kwargs):
        comment = get_object_or_404(models.PredefinedComment, pk = self.request.POST['predefinedcomment_id'])
        return HttpResponse('<script type="text/javascript">' +
            'window.parent.CKEDITOR.tools.callFunction("' + self.request.GET.get('CKEditorFuncNum') + '", "' +
            comment.content + '");</script>')

class PredefinedCommentCategoryCreate(AjaxableResponseMixin, generic.CreateView):
    model = models.PredefinedCommentCategory
    form_class = forms.PredefinedCommentCategoryForm
    success_url = reverse_lazy('courses:predefined_comment.list')
    
    def form_valid(self, form):
        form.instance.create_date = timezone.now()
        return super(PredefinedCommentCategoryCreate, self).form_valid(form)

class PredefinedCommentSubCategoryList(View):
    def get(self, request, pk):
        sub_categories = models.PredefinedCommentCategory.objects.filter(parent__id = pk).order_by('create_date')
        data = [ { 'id': sub_category.id, 'title': sub_category.title, 'is_terminal': sub_category.is_terminal } for sub_category in sub_categories]
        return JsonResponse({ 'list': data})

class PredefinedCommentCategoryDelete(SingleObjectMixin, View):
    model = models.PredefinedCommentCategory
    
    def post(self, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return JsonResponse({ })

class PredefinedCommentCategoryTerminate(SingleObjectMixin, View):
    model = models.PredefinedCommentCategory
    
    def post(self, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_terminal = True
        self.object.predefinedcommentcategory_set.clear()
        self.object.save()
        
        comment = models.PredefinedComment(content='',
            category = self.object,
            create_date = timezone.now())
        comment.save()
        
        return JsonResponse({ })

class PredefinedCommentDetail(View): 
    def get(self, request, pk):
        category = models.PredefinedCommentCategory.objects.get(id = pk)
        assert category.is_terminal
        comment = category.comment
        data = { 'id': comment.id, 'content': comment.content }
        return JsonResponse(data)

class PredefinedCommentUpdate(AjaxableResponseMixin, generic.UpdateView):
    model = models.PredefinedComment
    form_class = forms.PredefinedCommentForm
    success_url = reverse_lazy('courses:predefined_comment.list')

class FileUpload(View):
    root = settings.MEDIA_ROOT
    relative_path = '/'
    
    def post(self, *args, **kwargs):
        uploadFile = self.request.FILES['upload']
        filename = self.request.FILES['upload'].name
        path = os.path.join(self.root, self.relative_path)
        with open(os.path.join(path, filename), 'wb') as destination:
            for chunk in uploadFile.chunks():
                destination.write(chunk)
        return HttpResponse('<script type="text/javascript">' +
            'window.parent.CKEDITOR.tools.callFunction("' + self.request.GET.get('CKEditorFuncNum') + '", "' +
            settings.MEDIA_URL + self.relative_path + filename + '", "");</script>')

class FileBrowseMixin(object):
    root = settings.MEDIA_ROOT
    relative_path = '/'

    def get_context_data(self, **kwargs):
        context = super(FileBrowseMixin, self).get_context_data(**kwargs)
        
        path = os.path.join(self.root, self.relative_path)
        files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        context['objects'] = [ { 'title': f, 'url': settings.MEDIA_URL + self.relative_path + f } for f in files]
        context['CKEditorFuncNum'] = self.request.GET.get('CKEditorFuncNum')
        return context

class ImageUpload(FileUpload):
    relative_path = 'image/'

class ImageBrowse(FileBrowseMixin, generic.TemplateView):
    template_name = 'courses/image_browse.html'
    relative_path = 'image/'

class AudioUpload(FileUpload):
    relative_path = 'audio/'

class AudioBrowse(FileBrowseMixin, generic.TemplateView):
    template_name = 'courses/audio_browse.html'
    relative_path = 'audio/'

class PeopleList(TemplateView):
    template_name = 'courses/people_list.html'
    
    def get_context_data(self, **kwargs):
        context = super(PeopleList, self).get_context_data(**kwargs)
        course = get_object_or_404(models.Course, pk=self.kwargs['pk'])
        context['course'] = course
        return context