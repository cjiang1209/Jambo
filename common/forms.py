from django import forms

class AddUserForm(forms.Form):
    upload = forms.FileField();