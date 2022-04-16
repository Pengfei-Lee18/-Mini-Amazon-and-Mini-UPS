from unicodedata import name
from django.shortcuts import render
from django.shortcuts import redirect
from . import models
from . import forms
from django.db.models import Q
import json
from django.conf import settings


# Create your views here.

def index(request):
    islogin = request.session.get('is_login', None)
    packagelist = None
    searchres = None
    if islogin:
        cur_user = models.User.objects.get(id=request.session['user_id'])
        packagelist = models.Package.objects.filter(user_id=cur_user)
    if request.method == 'POST':
        tracknum_form = forms.TrackForm(request.POST)
        if tracknum_form.is_valid():
            tracknum = tracknum_form.cleaned_data.get('tracknum')
            searchlist = models.Package.objects.filter(tracking_id=tracknum)
            if(searchlist):
                searchres = searchlist[0]
            else:
                message = 'cannot find any package'
                return render(request, 'upswebsite/index.html', locals())
            return render(request, 'upswebsite/index.html', locals())
        else:
            message = 'check your input!'
            return render(request, 'upswebsite/index.html', locals())
    tracknum_form = forms.TrackForm()
    return render(request, 'upswebsite/index.html', locals())

def login(request):
    if request.session.get('is_login', None):  
        return redirect('/index/')
    if request.method == 'POST':
        login_form = forms.UserForm(request.POST)
        message = 'check your input!'
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            try:
                user = models.User.objects.get(name=username)
            except :
                message = 'invalid user'
                return render(request, 'upswebsite/login.html', locals())
            if user.password == password:
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                return redirect('/index/')
            else:
                message = 'invalid password'
                return render(request, 'upswebsite/login.html', locals())
        else:
            return render(request, 'upswebsite/login.html', locals())
    login_form = forms.UserForm()
    return render(request, 'upswebsite/login.html', locals())


def logout(request):
    request.session.flush()
    return redirect("/index/")


def register(request):
    if request.method == 'POST':
        register_form = forms.RegisterForm(request.POST)
        message = "check your input"
        if register_form.is_valid():
            username = register_form.cleaned_data.get('username')
            password1 = register_form.cleaned_data.get('password1')
            password2 = register_form.cleaned_data.get('password2')
            email = register_form.cleaned_data.get('email')
            if password1 != password2:
                message = 'diff between your two password'
                return render(request, 'upswebsite/register.html', locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:
                    message = 'exist username'
                    return render(request, 'upswebsite/register.html', locals())
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:
                    message = 'exist email'
                    return render(request, 'upswebsite/register.html', locals())
                new_user = models.User()
                new_user.name = username
                new_user.password = password1
                new_user.email = email
                new_user.save()
                return redirect('/login/')
        else:
            return render(request, 'upswebsite/register.html', locals())
    register_form = forms.RegisterForm()
    return render(request, 'upswebsite/register.html', locals())


def bind(request, tracking_id):
    res = models.Package.objects.get(tracking_id=tracking_id)
    cur_user = models.User.objects.get(id=request.session['user_id'])
    res.user_id = cur_user
    res.save()
    return redirect('/index/')

def unbind(request, tracking_id):
    res = models.Package.objects.get(tracking_id=tracking_id)
    res.user_id = None
    res.save()
    return redirect('/index/')