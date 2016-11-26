from django.conf.urls import url, include
from . import views
from django.contrib.auth.views import login, logout, password_change, password_change_done

urlpatterns = [
    url(r'^$', views.Index.as_view(), name='index'),
    #url(r'^', include('django.contrib.auth.urls')),
    
    url(r'^account/', include([
        url(r'^login/$', login, {'template_name': 'account/login.html'}, name='login'),
        url(r'^logout/$', logout, {'template_name': 'account/logout.html'}, name='logout'),
        url(r'^password_change/$', password_change, {'template_name': 'account/password_change.html'}, name='password_change'),
        url(r'^password_change/done/$', password_change_done, {'template_name': 'account/password_change_done.html'}, name='password_change_done'),
    ])),
    
    url(r'^users/userlist', views.UserList.as_view(), name='user.list'),
    url(r'^users/adduser', views.AddUser.as_view(), name='user.create'),
]