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

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

    
    path('', views.index, name='index'),
]
