# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.contrib.auth.models import User, Group, Permission
from django.shortcuts import redirect


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
    
    users = User.objects.all().order_by('id')
    context['users'] = users
    
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def view_user(request):
    print("Adding user ", request.method)
    
    if request.method == 'POST':
        print("POST request received")
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')
        
        print("Username:", username)
        print("First Name:", first_name)
        print("Last Name:", last_name)
        print("Email:", email)
        print("Role:", role)  
        print("Password:", password)
        
        
        group = Group.objects.get(name=role)
        
        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password
        )
            
        user.save()
            
        user.groups.add(group)
            
        return HttpResponseRedirect(reverse('table_user'))
        
    context = {'segment': 'add_user'}
    html_template = loader.get_template('home/form.html')
    
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def validar_factura(request):
    context = {'segment': 'Facturas'}

    html_template = loader.get_template('home/validarFacturas.html')
    return HttpResponse(html_template.render(context, request))
