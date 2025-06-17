# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Factura(models.Model):
    ESTATUS_CHOICES = [
        ('subida', 'Subida'), 
        ('valida', 'Validada'),
        ('aprueba', 'Aprobada'),
    ]

    estatus = models.CharField(
        max_length=10, 
        choices=ESTATUS_CHOICES,
        default='subida',
    )
    fecha = models.DateTimeField(auto_now_add=True)
    cliente = models.CharField(max_length=100)
    usuario = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='facturas',
    )
    nombreArchivo = models.CharField(max_length=75)
    extension = models.FileField(upload_to='facturas/')
    total = models.DecimalField(max_digits=10, decimal_places=2)
    direccion = models.TextField()
    concepto = models.TextField()

    def __str__(self):
        return f"{self.nombreArchivo}.{self.extension} - {self.cliente}"
    

    