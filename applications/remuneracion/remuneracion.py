import json
import requests

from datetime import datetime, timedelta
from decouple import config
from applications.base.models import TablaGeneral

from applications.empresa.models import Afp, Salud
from applications.remuneracion.indicadores import IndicatorEconomic

class Remunerations():

    MINIMUM_SALARY = 460000
    TOPE_GRATIFICATION = 4.75


    def __calculate_amount_range(utm_value, utm_quantity, more_one = 0):
        """
        Calucula el monto a rebajar

        :param utm_value: valor de la utm
        :param utm_quantity: cantidad de utm
        :param more_one: mas uno para el tope del siguiente
        :return 
            retorna el monto a rebajar
        """
        return (utm_value * utm_quantity) + more_one
    
    def __to_string_float(string):
        """
        Obtiene el numero float en string y lo retorna en float

        :param string: valor utm en string
        :return 
            retorna la utm en float
        """
        return float(string.replace(".", ""))

    @classmethod
    def monthly_income_tax_parameters(self, salary_imponible_mount):
        """
        parametros_impuesto_renta_mensual - Funcion que retorna el impuesto a la renta

        :param salary_imponible_mount: sueldo base imponible
        :return
        """

        get_utm = IndicatorEconomic.get_utm()


        parametros_impuesto_renta_mensual = [
            {
                "desde": 0,
                "hasta": self.__calculate_amount_range(self.__to_string_float(get_utm['Valor']), 13.50),
                "factor": 0,
                "cantidad_a_rebajar": 0,
                "tipo_impuesto": 0
            },{
                "desde": self.__calculate_amount_range(self.__to_string_float(get_utm['Valor']), 13.50, 1),
                "hasta": self.__calculate_amount_range(self.__to_string_float(get_utm['Valor']), 30),
                "factor": 0.04,
                "cantidad_a_rebajar": (self.__to_string_float(get_utm['Valor']) * 0.54),
                "tipo_impuesto": 2.20
            },{
                "desde": self.__calculate_amount_range(self.__to_string_float(get_utm['Valor']), 30, 1),
                "hasta": self.__calculate_amount_range(self.__to_string_float(get_utm['Valor']), 50),
                "factor": 0.08,
                "cantidad_a_rebajar": (self.__to_string_float(get_utm['Valor']) * 1.74),
                "tipo_impuesto": 4.52
            },{
                "desde": self.__calculate_amount_range(self.__to_string_float(get_utm['Valor']), 50, 1),
                "hasta": self.__calculate_amount_range(self.__to_string_float(get_utm['Valor']), 70),
                "factor": 0.135,
                "cantidad_a_rebajar": (self.__to_string_float(get_utm['Valor']) * 4.49),
                "tipo_impuesto": 7.09
            },{
                "desde": self.__calculate_amount_range(self.__to_string_float(get_utm['Valor']), 70, 1),
                "hasta": self.__calculate_amount_range(self.__to_string_float(get_utm['Valor']), 90),
                "factor": 0.23,
                "cantidad_a_rebajar": (self.__to_string_float(get_utm['Valor']) * 11.14),
                "tipo_impuesto": 10.62
            },{
                "desde": self.__calculate_amount_range(self.__to_string_float(get_utm['Valor']), 90, 1),
                "hasta": self.__calculate_amount_range(self.__to_string_float(get_utm['Valor']), 120),
                "factor": 0.304,
                "cantidad_a_rebajar": (self.__to_string_float(get_utm['Valor']) * 17.80),
                "tipo_impuesto": 15.57
            },{
                "desde": self.__calculate_amount_range(self.__to_string_float(get_utm['Valor']), 120, 1),
                "hasta": self.__calculate_amount_range(self.__to_string_float(get_utm['Valor']), 310),
                "factor": 0.35,
                "cantidad_a_rebajar": (self.__to_string_float(get_utm['Valor']) * 23.32),
                "tipo_impuesto": 27.48
            },{
                "desde": self.__calculate_amount_range(self.__to_string_float(get_utm['Valor']), 310, 1),
                "hasta": self.__calculate_amount_range(self.__to_string_float(get_utm['Valor']), 310, 1),
                "factor": 0.4,
                "cantidad_a_rebajar": (self.__to_string_float(get_utm['Valor']) * 38.82),
                "tipo_impuesto": 27.48
            },
        ]




    @classmethod
    def translate_month(self, month, language = 'es_cl'):

        idioms = {
            'es_cl': {
                'january': 'enero',
                'february': 'febrero',
                'march': 'marzo',
                'april': 'abril',
                'may': 'mayo',
                'june': 'junio',
                'july': 'julio',
                'august': 'agosto',
                'september': 'septiembre',
                'october': 'octubre',
                'november': 'noviembre',
                'december': 'diciembre',
            }
        }

        month_lower = month.lower()
        translation = idioms.get(language, {}).get(month_lower, month)

        return translation

    @classmethod
    def calculate_sesantia_insurance(self, salary_imponible_mount, contract_type):

        obj_contract_type = TablaGeneral.objects.get(tg_nombretabla='tb_unemployment_insurance', tg_idelemento=contract_type)
        json_contract_type = json.loads(obj_contract_type.tg_value_one)

        tabla_general = TablaGeneral.objects.get(tg_nombretabla='tb_salary_cap', tg_idelemento='3')
        get_uf = IndicatorEconomic.get_uf_value_last_day()
        valor_str = get_uf['Valor'].replace('.', '').replace(',', '.')

        uf_tope = float(tabla_general.tg_descripcion) * float(valor_str)
        if float(salary_imponible_mount) > uf_tope:
            salary_imponible_mount = int(uf_tope)
        
        employee_contribution = int(salary_imponible_mount * (json_contract_type['empleado'] / 100))
        employer_contribution = int(salary_imponible_mount * (json_contract_type['empleador'] / 100))

        concept = f"Seguro de Cesantia: {json_contract_type['empleado']}% sobre {salary_imponible_mount}"
        return {
            'employee_contribution': int(employee_contribution), 
            'employer_contribution': int(employer_contribution),
            'concept': concept
        }


    @classmethod
    def calculate_afp_quote(self, afp_id, type_of_work, desired_salary):
        objects_afp = Afp.objects.filter(afp_id=afp_id)
        for value in objects_afp:
            if int(type_of_work) == 1:
                quote_rate = value.afp_tasatrabajadordependiente
            else:
                quote_rate = value.afp_tasatrabajadorindependiente

        tabla_general = TablaGeneral.objects.get(tg_nombretabla='tb_salary_cap', tg_idelemento='1')

        get_uf = IndicatorEconomic.get_uf_value_last_day()
        valor_str = get_uf['Valor'].replace('.', '').replace(',', '.')

        description_tope = False
        uf_tope = float(tabla_general.tg_descripcion) * float(valor_str)
        if float(desired_salary) > uf_tope:
            desired_salary = uf_tope
            description_tope = True

        quote_afp = int(float(desired_salary) * (quote_rate / 100))
        return {
            'discount_afp': quote_afp,
            'afp_nombre': objects_afp[0].afp_nombre,
            'quote_rate': quote_rate,
            'description_tope': description_tope
        }
    
    @classmethod
    def calculate_health_discount(self, desired_salary, health_entity, quantity_uf_health):
        # La tasa de descuento máxima para la salud en Chile es del 7%
        maximum_discount_rate = 0.07
        health_discount = int(desired_salary) * maximum_discount_rate
        difference_of_amount = 0
        health_discount_uf = 0

        object_healt = Salud.objects.filter(sa_id = int(health_entity))

        if not int(health_entity) == 1:
            get_uf = IndicatorEconomic.get_uf_value_last_day()
            valor_str = get_uf['Valor'].replace('.', '').replace(',', '.')
            valor_float = float(valor_str)

            health_discount_uf = int(float(quantity_uf_health) * valor_float)         
            difference_of_amount = health_discount_uf - health_discount

        return {
            'health_discount': int(health_discount),
            'difference_of_amount': int(difference_of_amount),
            'sa_nombre': object_healt[0].sa_nombre,
            'quantity_uf_health':quantity_uf_health,
            'health_discount_uf':health_discount_uf,
        }
    

    @classmethod
    def obtain_legal_bonus_cap(self, type_tope, base_salary, has_fratification = True):
        """
        type_tope:
            1 = MENSUAL
            2 = ANUAL

        base_salary:
            Monto del sueldo liquido (Amount of net salary)

        has_fratification:
            tiene gratificacion?
            True o False
        """

        if has_fratification:

            gratification_amount = (int(base_salary) * 12) * 0.25
            amount = self.MINIMUM_SALARY * self.TOPE_GRATIFICATION

            if gratification_amount > amount:
                a_payment = amount
            else:
                a_payment = gratification_amount

            if int(type_tope) == 1:
                a_payment = round((a_payment/12), 0)

            return {
                'legal_bonus_cap': int(round(a_payment, 0))
            }

        else:
            return False