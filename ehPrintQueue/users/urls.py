#!python
# log/urls.py
from django.conf.urls import url
from . import views
from users.forms import LoginForm


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^home/$', views.home, name='home'),
    url(r'^profile$', views.profile, name='profile'),
    url(r'^profile/edit/$', views.edit_profile, name='UpdateProfile'),
    url(r'^log/$', views.show_activity_log, name='log'),
    url(r'^accounts/register/$', views.register, name='register'),
    url(r'live-cam', views.printer_view, name='printer_view'),
    url(r'^send_email', views.send_email, name='send_email'),
]
