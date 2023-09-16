import json
import requests

from datetime import datetime, timedelta
from decouple import config

from applications.empresa.models import Afp, Salud
from applications.remuneracion.indicadores import IndicatorEconomic

class Remunerations():

    MINIMUM_SALARY = 460000
    TOPE_GRATIFICATION = 4.75

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
    def calculate_afp_quote(self, afp_id, type_of_work, desired_salary):
        objects_afp = Afp.objects.filter(afp_id=afp_id)
        for value in objects_afp:
            if int(type_of_work) == 1:
                quote_rate = value.afp_tasatrabajadordependiente
            else:
                quote_rate = value.afp_tasatrabajadorindependiente

        quote_afp = int(float(desired_salary) * (quote_rate / 100))
        return {
            'discount_afp': quote_afp,
            'afp_nombre': objects_afp[0].afp_nombre,
            'quote_rate': quote_rate,
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