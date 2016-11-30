from django.views.generic import TemplateView
from django.views import generic
from courses import models
import csv
import os
from courses.models import CustomUser
from django.contrib.auth.models import Group
from django.db import transaction, IntegrityError
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import FormView
from common import forms
from helper import auth
from django.conf import settings

class Index(TemplateView):
    template_name = 'index.html'

class UserList(generic.ListView):
    model = models.CustomUser
    template_name = 'user/user_list.html'

class AddUser(FormView):
    template_name = 'user/add_user.html'
    success_url = reverse_lazy('user.list')
    form_class = forms.AddUserForm
    
    def addUsersFromCSV(self, filename):
        with open(filename, 'r') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
            try:
                with transaction.atomic():
                    for row in reader:
                        user = CustomUser.objects.create_user(row['username'], row['email'], row['password'])
                        user.first_name = row['firstname']
                        user.last_name = row['lastname']
                        group = Group.objects.get(name = row['group'])
                        user.groups.set([group])
                        user.save()
            except IntegrityError:
                return False
        return True
    
    def form_valid(self, form):
        uploadFile = self.request.FILES['upload']
        filename = os.path.join(settings.MEDIA_ROOT, uploadFile.name)
        with open(filename, 'w') as destination:
            for chunk in uploadFile.chunks():
                destination.write(chunk)
        success = self.addUsersFromCSV(filename)
        os.remove(filename)
        if success:
            return super(AddUser, self).form_valid(form)
        else:
            form.add_error('upload', 'Import failed')
            return super(AddUser, self).form_invalid(form)
