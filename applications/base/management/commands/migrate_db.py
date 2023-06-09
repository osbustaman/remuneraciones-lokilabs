from django import conf
from django.core.management.base import BaseCommand
from decouple import config
from django.core.management import call_command
from applications.base.models import Cliente

class Command(BaseCommand):
    help = 'Se inicia la migracion para todas las bases de datos'

    def handle(self, *args, **options):

        lista = Cliente.objects.all()

        for base in lista:

            domain = base.cli_link
            subdomain = (domain.split('.')[0]).split('//')[1]

            nombre_bd = base.nombre_bd

            nueva_base = {}
            nueva_base['ENGINE'] = config('ENGINE')
            nueva_base['HOST'] = config('HOST')
            nueva_base['NAME'] = nombre_bd.lower()
            nueva_base['USER'] = config('USER')
            nueva_base['PASSWORD'] = config('PASSWORD')
            nueva_base['PORT'] = config('PORT')

            conf.settings.DATABASES[subdomain] = nueva_base
            call_command('migrate', database=f'{nombre_bd.lower()}'.lower())

        self.stdout.write('¡La migracion para todas las bases de datos fue realizada con exito!')