# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.contrib.auth.models import User
from django.shortcuts import render


@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]
        
        print("Loading template:", load_template)
    
        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def list_users(request):
    context = {'segment': 'tables'}
    html_template = loader.get_template('home/view_users.html')
    
    users = User.objects.all()
    context['users'] = users
    
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def add_user(request):
    context = {'segment': 'add_user'}
    html_template = loader.get_template('home/form.html')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        
        if username and password and email:
            user = User.objects.create_user(username=username, password=password, email=email)
            user.save()
            return HttpResponseRedirect(reverse('table_user'))
    
    return HttpResponse(html_template.render(context, request))