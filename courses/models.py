from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    instructors = models.ManyToManyField(User, related_name='instructions')
    status = models.BooleanField(default=True, help_text='This field denotes if the course is active.')
    students = models.ManyToManyField(User, related_name='enrollments')
    create_date = models.DateTimeField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)