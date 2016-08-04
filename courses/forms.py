from django.forms import ModelForm
from . import models
from common import widgets

class ArticleForm(ModelForm):
    class Meta:
        model = models.Article
        fields = [ 'content' ]
        widgets = {
            'content' : widgets.RichTextEditor(),
        }

class CommentTemplateForm(ModelForm):
    class Meta:
        model = models.CommentTemplate
        fields = [ 'title', 'template_class', 'content' ]
        widgets = {
            'content' : widgets.RichTextEditor(),
        }