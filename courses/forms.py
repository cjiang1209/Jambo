from . import models
from django import forms
from common import widgets
from django.contrib.auth.models import Group

class CourseForm(forms.ModelForm):
    instructors = forms.ModelMultipleChoiceField(widget = forms.SelectMultiple(attrs = {'class': 'form-control'}),
        queryset = Group.objects.get(name='Instructor').user_set.all(),
        required = False);
    students = forms.ModelMultipleChoiceField(widget = forms.SelectMultiple(attrs = {'class': 'form-control'}),
        queryset = Group.objects.get(name='Student').user_set.all(),
        required = False);
    
    class Meta:
        model = models.Course
        fields = [ 'title', 'description', 'instructors', 'students' ]
        widgets = {
            'title': forms.TextInput(attrs = {'class': 'form-control'}),
            'description': forms.Textarea(attrs = {'class': 'form-control'})
        }

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = models.Assignment
        fields = [ 'title', 'description' ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'})
        }

class SubmissionPeriodForm(forms.ModelForm):
    class Meta:
        model = models.SubmissionPeriod
        fields = [ 'title', 'start_date', 'end_date', 'assignment' ]
    
    def clean(self):
        cleaned_data = super(SubmissionPeriodForm, self).clean()
         
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        if start_date and end_date:
            if start_date >= end_date:
                raise forms.ValidationError('Start date must be earlier than end date.')

class ArticleForm(forms.ModelForm):
    class Meta:
        model = models.Article
        fields = [ 'content' ]
#         widgets = {
#             'content': widgets.RichTextEditor(),
# #             'assignment': forms.HiddenInput
#         }

class GradingAttemptGradeForm(forms.ModelForm):
    class Meta:
        model = models.GradingAttempt
        fields = [ 'grade' ]
        widgets = {
            'grade': forms.NumberInput(attrs={'class': 'form-control'})
        }

class PredefinedCommentForm(forms.ModelForm):
    class Meta:
        model = models.PredefinedComment
        fields = [ 'title', 'category', 'content' ]
        widgets = {
            'content': widgets.RichTextEditor(),
        }

class PredefinedCommentCategoryForm(forms.ModelForm):
    class Meta:
        model = models.PredefinedCommentCategory
        fields = [ 'title', 'parent' ]