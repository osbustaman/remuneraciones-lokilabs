# -*- encoding: utf-8 -*-
from django.core.management.base import BaseCommand
from app01.functions import load_data_base

from applications.base.models import Cliente, ParametrosIndicadoresPrevisionales

class Command(BaseCommand):

    help = 'ingresa el nombre de la nueva base'

    def add_arguments(self, parser):
        parser.add_argument('base', type=str, help='ingresa el nombre de la nueva base')

    def handle(self, *args, **kwargs):

        load_data_base()

        # python manage.py migrate_indicadores_previsionales
        if kwargs['base'] == 'all_bases':
            lista = Cliente.objects.all()
        else:
            lista = Cliente.objects.filter(nombre_bd = kwargs['base'])


        seguro_cesantia = [
            {
                "pip_codigo": "PI",
                "contrato": "Plazo Indefinido",
                "empleador": 2.4,
                "empleado": 0.6
            },{
                "pip_codigo": "PF",
                "contrato": "Plazo Fijo",
                "empleador": 3.0,
                "empleado": 0
            },{
                "pip_codigo": "PI11",
                "contrato": "Plazo Indefinido 11 años o más",
                "empleador": 0.8,
                "empleado": 0
            },{
                "pip_codigo": "TCP",
                "contrato": "Trabajador de Casa Particular",
                "empleador": 3.0,
                "empleado": 0
            }
        ]

        for base in lista:
            nombre_bd = base.nombre_bd
            print(f" ********** Cargando datos para {nombre_bd} ********** ")

            for value in seguro_cesantia:
                tc = ParametrosIndicadoresPrevisionales.objects.using(nombre_bd).filter(pip_codigo=value['pip_codigo'])
                pip_codigo = value['pip_codigo']
                if not tc.exists():
                    pip = ParametrosIndicadoresPrevisionales()

                    pip.pip_codigo = value['pip_codigo']
                    pip.pip_descripcion = value['contrato']
                    pip.pip_valor = ""
                    pip.pip_rangoini = value['empleador']
                    pip.pip_rangofin = value['empleado']
                    pip.pip_factor = ""
                    pip.pip_activo = "S"
                    pip.save(using=nombre_bd)
                    print(f"El parámetro {pip_codigo} fue creado con éxito")
                else:
                    print(f"El parámetro {pip_codigo} ya existe")