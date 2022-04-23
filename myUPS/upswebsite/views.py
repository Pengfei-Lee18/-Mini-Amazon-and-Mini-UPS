from unicodedata import name
from django.shortcuts import render
from django.shortcuts import redirect
from . import models
from . import forms
from django.db.models import Q
import json
from django.conf import settings
import threading
import sys 
sys.path.append("..")
from communication import resend_package
world_id = 1

# Create your views here.

def index(request):
    try:
        cur_world = models.World.objects.all()[0]
        global world_id 
        world_id = cur_world.world_id
        # world_id 
        cur_world.delete()
    except:
        print("还没生成worldid，暂且用1")
    islogin = request.session.get('is_login', None)
    packagelist = None
    searchres = None
    if islogin:
        cur_user = models.User.objects.get(id=request.session['user_id'], world_id=world_id)
        packagelist = models.Package.objects.filter(user_id=cur_user, world_id=world_id)
    if request.method == 'POST':
        tracknum_form = forms.TrackForm(request.POST)
        if tracknum_form.is_valid():
            tracknum = tracknum_form.cleaned_data.get('tracknum')
            searchlist = models.Package.objects.filter(tracking_id=tracknum, world_id=world_id)
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
                user = models.User.objects.get(name=username, world_id=world_id)
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
                same_name_user = models.User.objects.filter(name=username, world_id=world_id)
                if same_name_user:
                    message = 'exist username'
                    return render(request, 'upswebsite/register.html', locals())
                same_email_user = models.User.objects.filter(email=email, world_id=world_id)
                if same_email_user:
                    message = 'exist email'
                    return render(request, 'upswebsite/register.html', locals())
                new_user = models.User()
                new_user.name = username
                new_user.password = password1
                new_user.email = email
                new_user.world_id = world_id
                new_user.save()
                return redirect('/login/')
        else:
            return render(request, 'upswebsite/register.html', locals())
    register_form = forms.RegisterForm()
    return render(request, 'upswebsite/register.html', locals())


def bind(request, tracking_id):
    res = models.Package.objects.get(tracking_id=tracking_id, world_id=world_id)
    cur_user = models.User.objects.get(id=request.session['user_id'], world_id=world_id)
    res.user_id = cur_user
    res.save()
    return redirect('/index/')

def unbind(request, tracking_id):
    res = models.Package.objects.get(tracking_id=tracking_id, world_id=world_id)
    res.user_id = None
    res.save()
    return redirect('/index/')

def item(request, shipment_id):
    productlist = models.Product.objects.filter(shipment_id=shipment_id, world_id=world_id)
    return render(request, 'upswebsite/item.html', locals())

def changedest(request, tracking_id):
    if request.method == 'POST':
        dest_form = forms.DestForm(request.POST)
        message = "check your input"
        if dest_form.is_valid():
            
            x = dest_form.cleaned_data.get('x')
            y = dest_form.cleaned_data.get('y')
            cur_package = models.Package.objects.get(tracking_id=tracking_id, world_id=world_id)
            if cur_package.status == 'delivering' or cur_package.status == 'delivered':
                message = 'cannot change dest'
                return redirect('/index/')
            cur_package.x = x
            cur_package.y = y
            cur_package.save()
            return redirect('/index/')
        else:
            return render(request, 'upswebsite/dest.html', locals())
    dest_form = forms.DestForm()
    return render(request, 'upswebsite/dest.html', locals())

def resend(request, shipment_id):
    cur_package = models.Package.objects.get(shipment_id=shipment_id, world_id=world_id)
    cur_package.hasresend = True
    cur_package.save()
    models.Resend.objects.create(shipment_id=shipment_id, world_id=world_id)
    thread1 = threading.Thread(target=resend_package, args=(shipment_id,))
    thread1.start()
    return redirect('/index/')