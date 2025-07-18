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

    path('usuarios/editar/<int:id>', views.edit_user, name='edit_user'),

    path('usuarios/rol/<int:id>', views.edit_role_user, name='edit_role_user'),

    path('usuarios/eliminar/<int:id>', views.desactivate_or_activate_user, name='delete_or_active_user'),

    #facturas
    path('facturas', views.validar_factura, name='validar_factura'),
    
    #facturas
    path('facturas/detalles/', views.detalles_factura, name='detalles_factura'),

    #formulario de facturas 
    path('facturas/formulario/', views.form_facturas, name='form_facturas'),

    # función facturas
    path('facturas/agregar/', views.agregar_factura, name='agregar_facturas'),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),
]


