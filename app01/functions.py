import django.conf as conf
from decouple import config
from django.db import connections
from app01.settings.local import DATABASES

from applications.base.models import Cliente


def elige_choices(obj_choice, str):
    valor = ""
    for key, value in obj_choice:
        if key == str:
            valor = value
    return valor

def load_data_base():
    # lista = {}
    lista = Cliente.objects.using('default').all()

    for base in lista:

        domain = base.cli_link
        subdomain = (domain.split('.')[0]).split('//')[1]

        nueva_base = {}
        nueva_base['ENGINE'] = config('ENGINE')
        nueva_base['HOST'] = config('HOST')
        nueva_base['NAME'] = base.nombre_cliente
        nueva_base['USER'] = config('USER')
        nueva_base['PASSWORD'] = config('PASSWORD')
        nueva_base['PORT'] = config('PORT')

        conf.settings.DATABASES[subdomain] = nueva_base

def get_current_database_name():
    default_database_name = connections['paula'].settings_dict['NAME']
    return default_database_name

