# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),

    # List users
    path('usuarios', views.list_users, name='table_user'),
    
    path('usuarios/agregar', views.add_user, name='add_user'),

    #facturas
    path('facturas', views.validar_factura, name='validar_factura'),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),
]
