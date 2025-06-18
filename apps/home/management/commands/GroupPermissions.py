from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission

class Command(BaseCommand):
    def handle(self, *args, **options):
        # Crear grupo si no existe
        groupAdmin, createdAdmin = Group.objects.get_or_create(name='admin')
        groupOperador, createdOperador = Group.objects.get_or_create(name='operador')
        groupCapturista, createdCapturista = Group.objects.get_or_create(name='capturista')

        if createdAdmin:
            self.stdout.write(self.style.SUCCESS(f'Grupo "{groupAdmin.name}" creado.'))
        
        if createdOperador:
            self.stdout.write(self.style.SUCCESS(f'Grupo "{groupOperador.name}" creado.'))

        if createdCapturista:
            self.stdout.write(self.style.SUCCESS(f'Grupo "{groupCapturista.name}" creado.'))

        # Lista de permisos a agregar (por codename)
        permisosAdmin = [
            'add_user',
            'change_user',
            'delete_user',
            'view_user',
            'add_factura',
            'change_factura',
            'delete_factura',
            'view_factura',
        ]

        permisosOperador = [
            'view_factura',
            'change_factura',
        ]

        permisosCapturista = [
            'view_factura',
            'add_factura',
            'delete_factura',
        ]

        for group in [groupAdmin, groupOperador, groupCapturista]:
            group_name = group.name

            if group_name == 'admin':
                permisos = permisosAdmin
            elif group_name == 'operador':
                permisos = permisosOperador
            elif group_name == 'capturistas':
                permisos = permisosCapturista

            for codename in permisos:
                try:
                    permiso = Permission.objects.get(codename=codename)
                    group.permissions.add(permiso)
                except Permission.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f'Permiso no encontrado: {codename}'))
            
            group.save()

            self.stdout.write(self.style.SUCCESS(f'Permisos asignados al grupo "{group_name}".'))