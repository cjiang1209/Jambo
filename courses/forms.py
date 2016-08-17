from . import models
from django import forms
from common import widgets

class CourseForm(forms.ModelForm):
    class Meta:
        model = models.Course
        fields = [ 'title', 'description', 'instructors', 'students' ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'instructors': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'students': forms.SelectMultiple(attrs={'class': 'form-control'})
        }

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = models.Assignment
        fields = [ 'title', 'description', 'course', 'due_date' ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'course': forms.Select(attrs={'class': 'form-control'}),
            'due_date': forms.TextInput(attrs={'class': 'form-control'})
        }

class ArticleForm(forms.ModelForm):
    class Meta:
        model = models.Article
        fields = [ 'content', 'submission_period' ]
        widgets = {
            'content': widgets.RichTextEditor(),
            'submission_period': forms.HiddenInput
        }

class GradingAttemptGradeForm(forms.ModelForm):
    class Meta:
        model = models.GradingAttempt
        fields = [ 'grade' ]
        widgets = {
            'grade': forms.NumberInput(attrs={'class': 'form-control'})
        }

class CommentTemplateForm(forms.ModelForm):
    class Meta:
        model = models.CommentTemplate
        fields = [ 'title', 'template_class', 'content' ]
        widgets = {
            'content': widgets.RichTextEditor(),
        }