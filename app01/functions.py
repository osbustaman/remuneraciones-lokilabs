import django.conf as conf
from decouple import config
from django.db import connections
from app01.settings.local import DATABASES

from geopy.geocoders import Nominatim

from applications.base.models import Cliente

def getLatitudeLongitude(address):
    # Crear un objeto geolocator utilizando el proveedor Nominatim
    geolocator = Nominatim(user_agent="Nominatim")

    # Obtener la ubicación (latitud, longitud) a partir de la dirección
    location = geolocator.geocode(address)

    if location:
        latitude = location.latitude
        longitude = location.longitude
        return latitude, longitude
    else:
        return None, None

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

