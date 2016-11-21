from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.Index.as_view(), name='index'),
    url(r'^', include('django.contrib.auth.urls')),
    
    url(r'^users/userlist', views.UserList.as_view(), name='user.list'),
    url(r'^users/adduser', views.AddUser.as_view(), name='user.create'),
]