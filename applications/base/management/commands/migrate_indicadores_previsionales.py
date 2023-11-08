# -*- encoding: utf-8 -*-
import json

from django.core.management.base import BaseCommand
from app01.functions import load_data_base

from applications.base.models import Cliente, ParametrosIndicadoresPrevisionales, TablaGeneral
from applications.remuneracion.indicadores import IndicatorEconomic

class Command(BaseCommand):

    help = 'ingresa el nombre de la nueva base'

    def add_arguments(self, parser):
        parser.add_argument('base', type=str, help='ingresa el nombre de la nueva base')

    def calculate_amount_range(self, utm_value, utm_quantity, more_one = 0):
        """
        Calucula el monto a rebajar

        :param utm_value: valor de la utm
        :param utm_quantity: cantidad de utm
        :param more_one: mas uno para el tope del siguiente
        :return 
            retorna el monto a rebajar
        """

        _round = 2
        more_one = float(f"0.{more_one}")

        value = (utm_value * utm_quantity) + more_one

        return round(value, _round)
    
    def to_string_float(self, string):
        """
        Obtiene el numero float en string y lo retorna en float

        :param string: valor utm en string
        :return 
            retorna la utm en float
        """
        return float(string.replace(".", ""))


    def handle(self, *args, **kwargs):

        load_data_base()

        # python manage.py migrate_indicadores_previsionales
        if kwargs['base'] == 'all_bases':
            lista = Cliente.objects.all()
        else:
            lista = Cliente.objects.filter(nombre_bd = kwargs['base'])


        get_utm = IndicatorEconomic.get_utm()