import json
import requests

from datetime import datetime, timedelta
from decouple import config

from applications.empresa.models import Afp
from applications.remuneracion.indicadores import IndicatorEconomic

class Remunerations():

    MINIMUM_SALARY = 460000
    TOPE_GRATIFICATION = 4.75


    @classmethod
    def calculate_afp_quote(self, afp_id, type_of_work, desired_salary):
        objects_afp = Afp.objects.filter(afp_id=afp_id)
        for value in objects_afp:
            if int(type_of_work) == 1:
                quote_rate = value.afp_tasatrabajadordependiente
            else:
                quote_rate = value.afp_tasatrabajadorindependiente

        quote_afp = float(desired_salary) * (quote_rate / 100)
        return {
            'discount_afp': round(quote_afp, 2)
        }
    
    @classmethod
    def calculate_health_discount(self, desired_salary, health_entity, quantity_uf_health):
        # La tasa de descuento máxima para la salud en Chile es del 7%
        maximum_discount_rate = 0.07
        health_discount = int(desired_salary) * maximum_discount_rate
        difference_of_amount = 0

        if not int(health_entity) == 1:
            get_uf = IndicatorEconomic.get_uf_value_last_day()

            health_discount_uf = quantity_uf_health * get_uf            
            difference_of_amount = health_discount_uf - health_discount
            health_discount = health_discount_uf

        return {
            'health_discount': round(health_discount, 2),
            'difference_of_amount': round(difference_of_amount, 2)
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