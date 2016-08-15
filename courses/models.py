from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.template.defaultfilters import default

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    instructors = models.ManyToManyField(User, related_name='instructions')
    status = models.BooleanField(default=True, help_text='This field denotes if the course is active.')
    students = models.ManyToManyField(User, related_name='enrollments')
    create_date = models.DateTimeField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title

class Assignment(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    create_date = models.DateTimeField()
    due_date = models.DateTimeField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title

class SubmissionPeriod(models.Model):
    title = models.CharField(max_length=200)
    start_date = models.DateTimeField()
    end_date = models.DateField()
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)

class Article(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    status = models.BooleanField(default=False, help_text="This field denotes if the article has been reviewed.")
    #assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    submission_period = models.ForeignKey(SubmissionPeriod, on_delete=models.CASCADE)
    #parent = models.ForeignKey('GradingAttempt', on_delete=models.CASCADE, null=True)
    
    def get_absolute_url(self):
        return reverse('courses:article.detail', kwargs={'pk': self.pk})

class GradingAttempt(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    last_modified_date = models.DateTimeField()
    grade = models.IntegerField()

class Comment(models.Model):
    content = models.TextField()
    attempt = models.ForeignKey(GradingAttempt, on_delete=models.CASCADE)
    create_date = models.TextField()

class CommentTemplateClass(models.Model):
    title = models.CharField(max_length=200)
    is_end_class = models.BooleanField(default=True)
    parent_class = models.ForeignKey("CommentTemplateClass", on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return self.title

class CommentTemplate(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    template_class = models.ForeignKey(CommentTemplateClass, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title
