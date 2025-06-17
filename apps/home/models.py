from django.db import models
from django.contrib.auth.models import User
import os

class Factura(models.Model):
    ESTATUS_CHOICES = [
        ('subida', 'Subida'),
        ('aprueba', 'Aprobada'),
        ('deniega','Denegada')
    ]
    id = models.BigAutoField(primary_key=True)
    estatus = models.CharField(
        max_length=10, 
        choices=ESTATUS_CHOICES, 
        default='subida'
    )
    fecha = models.DateTimeField(auto_now_add=True)
    cliente = models.CharField(max_length=100)
    usuario = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='facturas'
    )
    nombre_archivo = models.CharField(max_length=255, editable=False) 
    archivo = models.FileField(upload_to='facturas/')
    total = models.DecimalField(max_digits=10, decimal_places=2)
    direccion = models.TextField()
    concepto = models.TextField()

    def save(self, *args, **kwargs):
        if self.archivo and not self.nombre_archivo:
            nombre_completo = self.archivo.name
            nombre_base, extension = os.path.splitext(nombre_completo)
            self.nombre_archivo = nombre_base
            self.extension = extension[1:] 
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre_archivo}.{self.extension} - {self.cliente}"

