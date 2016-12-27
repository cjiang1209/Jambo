from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from guardian.shortcuts import assign_perm
from guardian.shortcuts import remove_perm
from datetime import datetime
from django.utils import timezone

class CustomUser(User):
    class Meta:
        proxy = True
    
    def full_name(self):
        return self.first_name + ' ' + self.last_name
    
    def __str__(self):
        return self.full_name()
    
    def __unicode__(self):
        return self.full_name()

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    instructors = models.ManyToManyField(CustomUser, related_name='instructingCourses', blank=True)
    status = models.BooleanField(default=True, help_text='This field denotes if the course is active.')
    students = models.ManyToManyField(CustomUser, related_name='enrollingCourses', blank=True)
    create_date = models.DateTimeField()
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    
#     __original_instructors = None
#     __original_students = None
    
    class Meta:
        permissions = (
            ('view_course', 'Can view course'),
            ('instruct_course', 'Instruct course'),
            ('enroll_course', 'Enroll in course'),
        )
    
#     def __init__(self, *args, **kwargs):
#         super(Course, self).__init__(*args, **kwargs)
#         if self.instructors is None:
#             self.__original_instructors = None
#         else:
#             self.__original_instructors = self.instructors
#         if self.students is None:
#             self.__original_students = None
#         else:
#             self.__original_students = self.students
    
    def __str__(self):
        return self.title

class Assignment(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    create_date = models.DateTimeField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title
    
    def active_stage(self):
        current = timezone.now()
        try:
            return Stage.objects.get(assignment__id = self.id, start_date__lte = current,
                grace_period_end_date__gte = current)
        except Stage.DoesNotExist:
            return None
    
#     def last_grading_attempt(self):
#         try:
#             grading = GradingAttempt.objects.filter(article__assignment__id = self.id).latest('create_date')
#             print(grading)
#             return grading
#         except GradingAttempt.DoesNotExist:
#             return None

class Article(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    number = models.IntegerField()
    content = models.TextField()
    create_date = models.DateTimeField()
    last_modified_date = models.DateTimeField()
    status = models.BooleanField(default=False, help_text="This field denotes if the article has been reviewed.")
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    is_late = models.BooleanField(default=False, help_text="This field denotes if the article is created or modified after the end date.")
    #submission_period = models.ForeignKey(SubmissionPeriod, on_delete=models.CASCADE)
    parent_attempt = models.ForeignKey('GradingAttempt', on_delete=models.CASCADE, null=True, related_name='+')
    
    def __str__(self):
        return self.assignment.title + ' - ' + self.author.full_name() + ' - #' + str(self.number)
    
    def get_absolute_url(self):
        return reverse('courses:article.detail', kwargs={'pk': self.pk})

class Stage(models.Model):
    #title = models.CharField(max_length=200)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    grace_period_end_date = models.DateTimeField()
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.assignment.title + ' - ' + str(self.start_date) + ' - ' + str(self.end_date)
    
    def status(self):
        current = timezone.now()
        if current < self.start_date:
            return 'Not Started'
        elif current < self.end_date:
            return 'In Process'
        elif current < self.grace_period_end_date:
            return 'In Grace Period'
        else:
            return 'Ended'
    
#     def article(self):
#         try:
#             article = Article.objects.get(assignment__id = self.assignment.id,
#                 create_date__gte = self.start_date,
#                 create_date__lte = self.grace_period_end_date)
#             return article
#         except Article.DoesNotExist:
#             return None

class GradingAttempt(models.Model):
    article = models.OneToOneField(Article, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    last_modified_date = models.DateTimeField()
    grade = models.IntegerField(default=0)
    visible = models.BooleanField(default=False)
    
    def __str__(self):
        return "Grading Attempt - " + self.article.__str__()

class Comment(models.Model):
    content = models.TextField()
    attempt = models.ForeignKey(GradingAttempt, on_delete=models.CASCADE)
    create_date = models.TextField()

class PredefinedCommentCategory(models.Model):
    title = models.CharField(max_length=200)
    is_terminal = models.BooleanField(default=False)
    parent = models.ForeignKey('PredefinedCommentCategory', on_delete=models.CASCADE, null=True, blank=True)
    create_date = models.DateTimeField()
    
    def __str__(self):
        return self.title

class PredefinedComment(models.Model):
    #title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.OneToOneField(PredefinedCommentCategory, on_delete=models.CASCADE, related_name='comment')
    create_date = models.DateTimeField()
    
    def __str__(self):
        return self.content
