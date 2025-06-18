from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.contrib.auth.models import User
from apps.home.models import Factura
from decimal import Decimal
from datetime import datetime

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        try:
            usuario = User.objects.get(id=1)  
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR("El usuario con ID=1 no existe."))
            return

        factura1 = Factura.objects.create(
            estatus='deniega',
            fecha=datetime(2024, 4, 15, 10, 30),
            cliente='Empresa de Prueba S.A. de C.V.',
            usuario=usuario,
            nombreArchivo='factura_unica',
            extension=ContentFile(b'%PDF-1.4 ... contenido simulado ...', name='factura_unica.pdf'),
            total=Decimal('95344.56'),
            direccion='Av. Prueba #123, Ciudad Ejemplo, MX',
            concepto='Servicio de ejemplo por consultoría técnica',
        )

        self.stdout.write(self.style.SUCCESS(f"Factura creada: ID {factura1.id}, nombre {factura1.nombreArchivo}"))
