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


        monthly_tranche_one = {
            'desde': 0,
            'hasta': self.calculate_amount_range(self.to_string_float(get_utm['Valor']), 13.51340383281851),
            'factor': 0,
            'cantidad_a_rebajar': 0,
            'tipo_impuesto': 0
        }
        monthly_tranche_one = json.dumps(monthly_tranche_one)

        monthly_tranche_two = {
            "desde": self.calculate_amount_range(self.to_string_float(get_utm['Valor']), 13.51340383281851, 1),
            "hasta": self.calculate_amount_range(self.to_string_float(get_utm['Valor']), 30.02978629515224),
            "factor": 0.04,
            "cantidad_a_rebajar": round((self.to_string_float(get_utm['Valor']) * 0.5405361533127403), 2),
            "tipo_impuesto": 2.20
        }
        monthly_tranche_two = json.dumps(monthly_tranche_two)


        monthly_tranche_tree = {
            "desde": self.calculate_amount_range(self.to_string_float(get_utm['Valor']), 30.02978629515224, 1),
            "hasta": self.calculate_amount_range(self.to_string_float(get_utm['Valor']), 50.04964382525374),
            "factor": 0.08,
            "cantidad_a_rebajar": round((self.to_string_float(get_utm['Valor']) * 1.74172760511883), 2),
            "tipo_impuesto": 4.52
        }
        monthly_tranche_tree = json.dumps(monthly_tranche_tree)


        monthly_tranche_four = {
            "desde": self.calculate_amount_range(self.to_string_float(get_utm['Valor']), 50.04964382525374, 1),
            "hasta": self.calculate_amount_range(self.to_string_float(get_utm['Valor']), 70.06950135535523),
            "factor": 0.135,
            "cantidad_a_rebajar": round((self.to_string_float(get_utm['Valor']) * 4.494458015507785), 2),
            "tipo_impuesto": 7.09
        }
        monthly_tranche_four = json.dumps(monthly_tranche_four)


        monthly_tranche_five = {
            "desde": self.calculate_amount_range(self.to_string_float(get_utm['Valor']), 70.06950135535523, 1),
            "hasta": self.calculate_amount_range(self.to_string_float(get_utm['Valor']), 90.08935888545672),
            "factor": 0.23,
            "cantidad_a_rebajar": round((self.to_string_float(get_utm['Valor']) * 11.15106064426653), 2),
            "tipo_impuesto": 10.62
        }
        monthly_tranche_five = json.dumps(monthly_tranche_five)


        monthly_tranche_six = {
            "desde": self.calculate_amount_range(self.to_string_float(get_utm['Valor']), 90.08935888545672, 1),
            "hasta": self.calculate_amount_range(self.to_string_float(get_utm['Valor']), 120.119145180609),
            "factor": 0.304,
            "cantidad_a_rebajar": round((self.to_string_float(get_utm['Valor']) * 17.81767320179033), 2),
            "tipo_impuesto": 15.57
        }
        monthly_tranche_six = json.dumps(monthly_tranche_six)


        monthly_tranche_seven = {
            "desde": self.calculate_amount_range(self.to_string_float(get_utm['Valor']), 120.119145180609, 1),
            "hasta": self.calculate_amount_range(self.to_string_float(get_utm['Valor']), 310.3077917165732),
            "factor": 0.35,
            "cantidad_a_rebajar": round((self.to_string_float(get_utm['Valor']) * 23.34315388009834), 2),
            "tipo_impuesto": 27.48
        }
        monthly_tranche_seven = json.dumps(monthly_tranche_seven)


        monthly_tranche_eight = {
            "desde": self.calculate_amount_range(self.to_string_float(get_utm['Valor']), 310.3077917165732, 1),
            "hasta": self.calculate_amount_range(self.to_string_float(get_utm['Valor']), 310.3077917165732, 1),
            "factor": 0.4,
            "cantidad_a_rebajar": round((self.to_string_float(get_utm['Valor']) * 38.858543465927), 2),
            "tipo_impuesto": 27.48
        }
        monthly_tranche_eight = json.dumps(monthly_tranche_eight)


        data_forecast_indicators = [

            # tb_tax_second_category = tb_impuesto_segunda_categoria
            {
                'tg_nombretabla': 'tb_tax_second_category',
                'tg_idelemento': '1',
                'tg_short_description': 'mensual',
                'tg_value_one': monthly_tranche_one
            },{
                'tg_nombretabla': 'tb_tax_second_category',
                'tg_idelemento': '2',
                'tg_short_description': 'mensual',
                'tg_value_one': monthly_tranche_two
            },{
                'tg_nombretabla': 'tb_tax_second_category',
                'tg_idelemento': '3',
                'tg_short_description': 'mensual',
                'tg_value_one': monthly_tranche_tree
            },{
                'tg_nombretabla': 'tb_tax_second_category',
                'tg_idelemento': '4',
                'tg_short_description': 'mensual',
                'tg_value_one': monthly_tranche_four
            },{
                'tg_nombretabla': 'tb_tax_second_category',
                'tg_idelemento': '5',
                'tg_short_description': 'mensual',
                'tg_value_one': monthly_tranche_five
            },{
                'tg_nombretabla': 'tb_tax_second_category',
                'tg_idelemento': '6',
                'tg_short_description': 'mensual',
                'tg_value_one': monthly_tranche_six
            },{
                'tg_nombretabla': 'tb_tax_second_category',
                'tg_idelemento': '7',
                'tg_short_description': 'mensual',
                'tg_value_one': monthly_tranche_seven
            },{
                'tg_nombretabla': 'tb_tax_second_category',
                'tg_idelemento': '8',
                'tg_short_description': 'mensual',
                'tg_value_one': monthly_tranche_eight
            },

            
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
        ]

        for base in lista:
            nombre_bd = base.nombre_bd
            print(f" ********** Cargando datos para {nombre_bd} ********** ")

            for value in data_forecast_indicators:

                try:

                    tbg = TablaGeneral.objects.using(nombre_bd).filter(tg_nombretabla=value['tg_nombretabla'], tg_idelemento=value['tg_idelemento'])
                    if not tbg.exists():
                        tbg = TablaGeneral()
                    else:
                        tbg = tbg.first()
                    
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

                    print(f"{tbg.tg_nombretabla} - {tbg.tg_idelemento}..........OK")
                except Exception as ex:
                    print(f"{value['tg_nombretabla']} - {value['tg_idelemento']}..........ERROR.......{str(ex)}")


            print(f" ********** Carga de datos para {nombre_bd} terminada********** ")