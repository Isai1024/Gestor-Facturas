# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),

    path('profile/', views.profile_view, name='profile'),

    # User management
    path('usuarios', views.list_users, name='table_user'),
    
    path('usuarios/agregar', views.view_user, name='view_user'),

    #facturas
    path('facturas', views.validar_factura, name='validar_factura'),
    
    #facturas
    path('facturas/detalles/', views.detalles_factura, name='detalles_factura'),

    #formulario de facturas 
    path('facturas/agregar/', views.form_facturas, name='form_facturas'),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),
]


