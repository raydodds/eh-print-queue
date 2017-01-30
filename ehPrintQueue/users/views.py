from django.shortcuts import render, render_to_response, redirect, HttpResponseRedirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, PermissionDenied
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate  # maybe works
import datetime
from .forms import *
from . import models
from django.template import RequestContext
from django.views.decorators.csrf import requires_csrf_token
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import EmailMessage

def get_date():
    return datetime.datetime.now()


def log_event(user, event):
    """
    :param user: The endUser object of the user doing the action
    :param event: A string describing the event happening
    :return:
    """
    models.log.objects.create(user=user,
                              event=event,
                              date=str(datetime.datetime.now().date()),
                              time=str(datetime.datetime.now().time()))


def send_email(request):
   user = request.user
   to = []
   to.append(user.email)
   email = EmailMessage('Subject', 'Body', to=to)
   email.send()
   return HttpResponseRedirect('/home')


@login_required(login_url='login')
def show_activity_log(request):
    """
    Shows the event log to administrators, if user is not admin,
    will instead render invalid.
    :param request:
    :return:
    """
    user = request.user
    loop = []
    for obj in models.log.objects.all():
        try:
            loop.append(str(obj))
        except:
            pass
    loop.reverse()
    if user.enduser.isAdmin:
        return render(request, 'users/activityLog.html', {'loop': loop, 'user': user})
    else:
        return render(request, 'users/invalid.html', {'d': get_date()})


def login(request):
    """
    Used to login, uses the LoginForm in users/forms.py
    :param request:
    :return:
    """
    if request.method == 'POST':
        form = LoginForm(request.POST)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        if not (username and password):
            return None, "Please enter a username and password"
        user = authenticate(username=username, password=password)
        if user:
            # log action
            try:
                profile = User.objects.get(username=username)
                log_event(event="Logged In", user=profile.enduser)
            except:
                pass
            login(request, user)

    return render(request, 'users/templates/registration/login.html')


@login_required(login_url='login')
def home(request):
    """
    Displays the home screen of the user, changes dynamically
    based on what type of user is viewing.
    :param request:
    :return:
    """
    user = request.user
    return render(request, "users/home.html", {'user': user})


def index(request):
    """
    The home page of the website, used to access registration and login screens.
    :param request:
    :return:
    """
    return render(request, 'users/index.html')


@login_required(login_url='login')
def profile(request):
    user = request.user
    if user.is_authenticated():
        return render(request, "users/profile.html", {'user': user})

    else:
        raise PermissionDenied


@login_required(login_url='login')
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        form = editProfile(request.POST)
        if form.is_valid():
            user.email = form.cleaned_data.get('email')
            user.save()
            user.enduser.save()
            log_event(event="edited their profile", user=user.enduser)
            return redirect('/home')
    else:
        form = editProfile(
            initial={'email': user.email})
    token = {}
    token.update(request)
    token['form'] = form
    token['user'] = user
    return render(request, "users/editProfile.html", token)


@requires_csrf_token
@login_required(login_url='login')
def register(request):
    user = request.user
    if user.enduser.isAdmin:
        if request.method == 'POST':
            form = RegisterForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = make_password(form.cleaned_data['password1'])
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                email = form.cleaned_data['email']
                new_user = User.objects.create(username=username, password=password, first_name=first_name,
                                               last_name=last_name, email=email)
                new_user.save()
                new_e_user = new_user.enduser
                if user.enduser.isCC:
                    new_e_user.isAdmin = form.cleaned_data['isAdmin']
                    new_e_user.isCC = form.cleaned_data['isCC']
                new_e_user.save()
                log_event(event="registered" + new_user.first_name + " " + new_user.last_name, user=user.enduser)
                return redirect('home')
        else:
            form = RegisterForm()
            token = {}
            token.update(request)
            token['form'] = form
            token['user'] = request.user
            return render(request, 'users/register.html', token)
    else:
        token = {}
        token['user'] = request.user
        return render(request, 'users/invalid.html', token)


@login_required(login_url='login')
def printer_view(request):
    user = request.user
    log_event(event="viewed the live printer view.", user=user.enduser)
    return render(request, 'users/printer_view.html', {'user': user})
