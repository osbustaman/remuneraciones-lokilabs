import re
import django
import psycopg2
import os
import json
import requests
import datetime


import pandas as pd
import pdfkit
import base64
import re

from django.conf import settings

from django.core.management import call_command
from django.template.loader import get_template
from django import conf

from decouple import config
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from app01.settings.local import WKHTMLTOPDF_BIN_PATH

from applications.base.models import Cliente, Comuna, Pais, Region


def indicadores_economicos(indicador):
    indicadores = [
        'uf', 'ivp', 'dolar', 'dolar_intercambio', 'euro', 'ipc', 'utm', 'imacec', 'tpm', 'libra_cobre', 'tasa_desempleo', 'bitcoin'
    ]

    fecha_actual = datetime.datetime.now()

    dia_actual = fecha_actual.day
    mes_actual = fecha_actual.month
    anio_actual = fecha_actual.year
    fecha_formateada = fecha_actual.strftime("%d-%m-%Y")

    url = f'https://mindicador.cl/api/{indicador}/{fecha_formateada}'
    response = requests.get(url)
    data = json.loads(response.text.encode("utf-8"))
    pretty_json = json.dumps(data, indent=2)
    return data


def getCliente(request):
    return Cliente.objects.filter(rut_cliente=request['rut_cliente']).exists()


def validarRut(rut):
    rut = rut.replace(".", "").replace("-", "")  # Eliminar puntos y guiones
    if not re.match(r'^\d{1,8}[0-9K]$', rut):  # Verificar formato
        return False
    rut_sin_dv = rut[:-1]
    dv = rut[-1].upper()  # Obtener dígito verificador
    multiplicador = 2
    suma = 0
    for r in reversed(rut_sin_dv):
        suma += int(r) * multiplicador
        multiplicador += 1
        if multiplicador == 8:
            multiplicador = 2
    resto = suma % 11
    dv_calculado = 11 - resto
    if dv_calculado == 11:
        dv_calculado = '0'
    elif dv_calculado == 10:
        dv_calculado = 'K'
    else:
        dv_calculado = str(dv_calculado)
    return dv == dv_calculado


def validate_mail(correo):
    # Patrón de expresión regular para validar un correo electrónico
    patron = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

    # Se compila el patrón
    patron_compilado = re.compile(patron)

    # Se verifica si el correo coincide con el patrón
    if patron_compilado.match(correo):
        return True
    else:
        return False