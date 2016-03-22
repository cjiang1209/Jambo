from django.forms.widgets import Textarea
from django.utils.safestring import mark_safe
from django.contrib.staticfiles.templatetags.staticfiles import static

class RichTextEditor(Textarea):
    def render(self, name, value, attrs=None):
        html = super(RichTextEditor, self).render(name, value, attrs)
        
        config_url = static('common/miscellaneous/ckeditor_edit_config.js')
        html = html + """<script>CKEDITOR.replace('""" + attrs['id'] + """', {
            customConfig: '""" + config_url + """'
        });</script>"""
        return mark_safe(html)