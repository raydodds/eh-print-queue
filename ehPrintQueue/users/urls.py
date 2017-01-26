#!python
# log/urls.py
from django.conf.urls import url
from . import views

# We are adding a URL called /home
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^home/$', views.home, name='home'),
    url(r'^profile$', views.profile, name='profile'),
    url(r'^profile/edit/$', views.edit_profile, name='UpdateProfile'),
    url(r'^log/$', views.show_activity_log, name='log'),
    url(r'^register/$', views.register, name='register')
]
