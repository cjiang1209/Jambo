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