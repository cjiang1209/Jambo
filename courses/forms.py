from . import models
from django import forms
from common import widgets

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

class CommentTemplateForm(forms.ModelForm):
    class Meta:
        model = models.CommentTemplate
        fields = [ 'title', 'template_class', 'content' ]
        widgets = {
            'content': widgets.RichTextEditor(),
        }