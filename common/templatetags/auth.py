from django import template
from helper import auth

register = template.Library() 

@register.filter(name='is_instructor')
def is_instructor(user):
    return auth.is_instructor(user)

@register.filter(name='is_student')
def is_student(user):
    return auth.is_student(user)

@register.filter(name='is_administrator')
def is_administrator(user):
    return auth.is_administrator(user)