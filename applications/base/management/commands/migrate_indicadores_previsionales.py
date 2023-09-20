# -*- encoding: utf-8 -*-
from django.core.management.base import BaseCommand
from app01.functions import load_data_base

from applications.base.models import Cliente, ParametrosIndicadoresPrevisionales, TablaGeneral
from applications.remuneracion.indicadores import IndicatorEconomic

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


        get_utm = IndicatorEconomic.get_utm()


        data_forecast_indicators = [
            # tb_salary_cap = renta tope
            {
                'tg_nombretabla': 'tb_salary_cap',
                'tg_idelemento': '1',
                'tg_short_description': 'afp',
                'tg_descripcion': '81.6'
            }, 
            {
                'tg_nombretabla': 'tb_salary_cap',
                'tg_idelemento': '2',
                'tg_short_description': 'ips',
                'tg_descripcion': '60'
            },
            {
                'tg_nombretabla': 'tb_salary_cap',
                'tg_idelemento': '3',
                'tg_short_description': 'ccf',
                'tg_descripcion': '122.6'
            },

            # tb_tope_apv = tb_tope_apv
            {
                'tg_nombretabla': 'tb_tope_apv',
                'tg_idelemento': '1',
                'tg_short_description': 'Tope Mensual',
                'tg_descripcion': '50'
            }, 
            {
                'tg_nombretabla': 'tb_tope_apv',
                'tg_idelemento': '2',
                'tg_short_description': 'Tope Anual',
                'tg_descripcion': '600'
            },

            # tb_deposit_agreement = tb_deposito_convenio
            {
                'tg_nombretabla': 'tb_deposit_agreement',
                'tg_idelemento': '1',
                'tg_short_description': 'Tope Anual',
                'tg_descripcion': '900'
            }, 

            # tb_unemployment_insurance = tb_seguro_cesantia
            {
                'tg_nombretabla': 'tb_unemployment_insurance',
                'tg_idelemento': '1',
                'tg_short_description': 'Plazo Indefinido',
                'tg_value_one': '{ "empleador": 2.4, "empleado": 0.6 }'
            },{
                'tg_nombretabla': 'tb_unemployment_insurance',
                'tg_idelemento': '2',
                'tg_short_description': 'Plazo Fijo',
                'tg_value_one': '{ "empleador": 3.0, "empleado": 0 }'
            },{
                'tg_nombretabla': 'tb_unemployment_insurance',
                'tg_idelemento': '3',
                'tg_short_description': 'Plazo Indefinido 11 años o más',
                'tg_value_one': '{ "empleador": 0.8, "empleado": 0 }'
            },{
                'tg_nombretabla': 'tb_unemployment_insurance',
                'tg_idelemento': '4',
                'tg_short_description': 'Trabajador de Casa Particular',
                'tg_value_one': '{ "empleador": 3.0 "empleado": 0 }'
            },

            # tb_tax_second_category = tb_impuesto_segunda_categoria
            {
                'tg_nombretabla': 'tb_tax_second_category',
                'tg_idelemento': '1',
                'tg_short_description': 'mensual',
                'tg_value_one': """
                                    {
                                        "desde": 0,
                                        "hasta": self.__calculate_amount_range(self.__to_string_float(get_utm['Valor']), 13.51),
                                        "factor": 0,
                                        "cantidad_a_rebajar": 0,
                                        "tipo_impuesto": 0
                                    }
                                """
            },
        ]

        for base in lista:
            nombre_bd = base.nombre_bd
            print(f" ********** Cargando datos para {nombre_bd} ********** ")

            for value in data_forecast_indicators:
                tg = TablaGeneral.objects.using(nombre_bd).filter(tg_nombretabla=value['tg_nombretabla'], tg_idelemento=value['tg_idelemento'])
                if not tg.exists():
                    tbg = TablaGeneral()
                    tbg.tg_nombretabla = value['tg_nombretabla']
                    tbg.tg_idelemento = value['tg_idelemento']
                    try:
                        tbg.tg_descripcion = value['tg_descripcion']
                    except:
                        pass
                    
                    try:
                        tbg.tg_short_description = value['tg_short_description']
                    except:
                        pass

                    try:
                        tbg.tg_value_one = value['tg_value_one']
                    except:
                        pass
                    tbg.save(using=nombre_bd)
                else:
                    tg_nombretabla = value['tg_nombretabla']
                    tg_idelemento = value['tg_idelemento']
                    print(f"El elemento {tg_nombretabla} - {tg_idelemento} ya existe")

            print(f" ********** Carga de datos para {nombre_bd} terminada********** ")