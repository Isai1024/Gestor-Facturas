from django.core.files.base import ContentFile
from django.contrib.auth.models import User
from apps.home.models import Factura
from datetime import datetime
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Crea datos de prueba para las gráficas'

    def handle(self, *args, **kwargs):
        usuario = User.objects.first()
        if not usuario:
            self.stdout.write(self.style.ERROR("No hay usuarios en la base de datos."))
            return

        # Simulación de archivo PDF falso (en memoria)
        archivo_simulado = ContentFile(b"%PDF-1.4\n%Fake PDF content\n", name="ejemplo.pdf")

        factura1 = Factura.objects.create(
            estatus='Subida',
            cliente='Empresa Falsa',
            usuario=usuario,
            archivo=archivo_simulado,
            total=4567.89,
            direccion='Calle Inventada 999',
            concepto='Servicios falsos para demo',
            fecha=datetime(2025, 6, 15, 10, 30)
        )

        self.stdout.write(self.style.SUCCESS(f"Factura creada: {factura1}"))
