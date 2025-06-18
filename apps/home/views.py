# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.contrib.auth.models import User, Group
from django.shortcuts import render
from .models import Factura
from django.utils import timezone
from datetime import timedelta

def index(request):
    ahora = timezone.now()
    inicio_mes_actual = ahora.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    inicio_mes_pasado = (inicio_mes_actual - timedelta(days=1)).replace(day=1)
    fin_mes_pasado = inicio_mes_actual - timedelta(seconds=1)

    # Conteos para el mes actual
    facturas_este_mes = Factura.objects.filter(fecha__gte=inicio_mes_actual)
    total_este_mes = facturas_este_mes.count()
    aprobadas_este_mes = facturas_este_mes.filter(estatus='aprueba').count()
    denegadas_este_mes = facturas_este_mes.filter(estatus='deniega').count()
    pendientes_este_mes = facturas_este_mes.filter(estatus='subida').count()

    # Conteos para el mes pasado2
    facturas_mes_pasado = Factura.objects.filter(fecha__range=(inicio_mes_pasado, fin_mes_pasado))
    total_mes_pasado = facturas_mes_pasado.count()
    aprobadas_mes_pasado = facturas_mes_pasado.filter(estatus='aprueba').count()
    denegadas_mes_pasado = facturas_mes_pasado.filter(estatus='deniega').count()
    pendientes_mes_pasado = facturas_mes_pasado.filter(estatus='subida').count()

    def calcular_porcentaje(actual, anterior):
        if anterior > 0:
            return round(((actual - anterior) / anterior) * 100, 2)
        return 100.0 if actual > 0 else 0.0

    context = {
        'segment': 'index',
        'total_facturas': total_este_mes,
        'facturas_pendientes': pendientes_este_mes,
        'facturas_aprobadas': aprobadas_este_mes,
        'facturas_denegadas': denegadas_este_mes,
        'cambio_total': calcular_porcentaje(total_este_mes, total_mes_pasado),
        'cambio_pendientes': calcular_porcentaje(pendientes_este_mes, pendientes_mes_pasado),
        'cambio_aprobadas': calcular_porcentaje(aprobadas_este_mes, aprobadas_mes_pasado),
        'cambio_denegadas': calcular_porcentaje(denegadas_este_mes, denegadas_mes_pasado),
    }

    return render(request, 'home/index.html', context)

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

# Show all users order by ID
@login_required(login_url="/login/")
def list_users(request):
    context = {'segment': 'tables'}
    html_template = loader.get_template('home/view_users.html')
    
    # Fetch all users and order them by ID
    users = User.objects.all().order_by('id')
    context['users'] = users
    
    return HttpResponse(html_template.render(context, request))

# Add a new user
"""
request body {
    "username": "username",
    "first_name": "First Name",
    "last_name": "Last Name",
    "email": "A valid email",
    "password": "Password",
    "role": "Role Name"  # This should be an existing group name
}
"""
@login_required(login_url="/login/")
def view_user(request):
    print("Adding user ", request.method)
    
    if request.method == 'POST':
        print("POST request received to add user")
    
        # Get user data from the form
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')
        
        # Validate that the role exists
        group = Group.objects.get(name=role)
        
        # Create the user
        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password
        )
            
        user.save()
            
        # Add the user to the specified group
        user.groups.add(group)
            
        return HttpResponseRedirect(reverse('table_user'))
        
    context = {'segment': 'Agregar'}
    html_template = loader.get_template('home/form.html')
    
    return HttpResponse(html_template.render(context, request))

# Edit a user
"""
request body {
    "username": "New Username",
    "first_name": "New First Name",
    "last_name": "New Last Name",
    "email": "New valid email",
    "password": "New Password" # Password can be empty to keep the old one
}
"""
@login_required(login_url="/login/")
def edit_user(request, id):
    print("Edit user ", request.method)
    
    if request.method == 'POST':
        print("POST request received for editing user")
    
        # Get user data from the form
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Fetch the user by ID
        user = User.objects.get(id=id)
        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        if password.strip():  # Only set password if it's not empty
            user.set_password(password)
        
        user.save()
            
        return HttpResponseRedirect(reverse('table_user'))
        
    context = {'segment': 'Editar'}
    html_template = loader.get_template('home/form.html')
    
    user = User.objects.get(id=id)
    context['user'] = user

    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def edit_role_user(request, id):
    print("Edit user role ", request.method)
    
    if request.method == 'POST':
        print("POST request received for editing user role")
    
        # Get the new role from the form
        new_role = request.POST.get('role')
        
        # Validate that the new role exists
        group = Group.objects.get(name=new_role)
        
        # Fetch the user by ID
        user = User.objects.get(id=id)
        
        # Clear existing groups and add the new one
        user.groups.clear()
        user.groups.add(group)
        
        user.save()
            
        return HttpResponseRedirect(reverse('table_user'))

    return HttpResponseRedirect(reverse('table_user'))  

@login_required(login_url="/login/")
def desactivate_or_activate_user(request, id):
    print("Desactivating or Activating user ", request.method)
    
    if request.method == 'POST':
        print("POST request received to desactivate or activate user")
    
        # Fetch the user by ID
        user = User.objects.get(id=id)
        
        # Desactivate or Activate the user
        user.is_active = not user.is_active
        user.save()
        
        return HttpResponseRedirect(reverse('table_user'))
    
    return HttpResponseRedirect(reverse('table_user'))

@login_required(login_url="/login/")
def validar_factura(request):
    context = {'segment': 'Facturas'}

    html_template = loader.get_template('home/validarFacturas.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def detalles_factura(request):
    context = {'segment': 'Facturas'}

    html_template = loader.get_template('home/visualizacionFactura.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def form_facturas(request):
    context = {'segment': 'Facturas'}

    html_template = loader.get_template('home/form-facturas.html')
    return HttpResponse(html_template.render(context, request))
