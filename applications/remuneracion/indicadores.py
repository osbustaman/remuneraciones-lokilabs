import json
import requests

from datetime import datetime, timedelta
from decouple import config

class IndicatorEconomic():

    url_base = 'https://api.cmfchile.cl/api-sbifv3/'
    api_key = config('API_KEY_INDICATORS')


    @classmethod
    def get_utm(self, date, format = 'json'):

        utm = f'{self.url_base}recursos_api/utm?apikey={self.api_key}&formato=json'
        data_utm = requests.get(utm) 
        data_utm_json = data_utm.json()

        x_value = {}
        for key, value in data_utm_json.items():
            for dicc in value:
                x_value = dicc

        return dict(x_value)


    @classmethod
    def get_uf(self, date, format = 'json'):

        year = date.year
        month = date.month
        day = date.day

        _url = f'{self.url_base}recursos_api/uf/{year}/{month}/dias/{day}?apikey={self.api_key}&formato={format}'

        data_uf = requests.get(_url)
        data_uf_json = data_uf.json()

        x_value = {}
        for key, value in data_uf_json.items():
            for dicc in value:
                x_value = dicc

        return dict(x_value)
    
    @classmethod
    def get_uf_value_last_day(self):
        # Obtener la fecha actual
        current_date = datetime.now()

        # Obtener el día actual y el día 9 del mes actual
        current_actual = current_date.day
        day_9_of_month = datetime(current_date.year, current_date.month, 9).day

        # Calcular la fecha del último día del mes actual
        last_day_of_current_month = datetime(current_date.year, current_date.month, 1) + timedelta(days=31)
        while last_day_of_current_month.month != current_date.month:
            last_day_of_current_month -= timedelta(days=1)

        # Calcular la fecha del último día del mes anterior
        last_day_of_previous_month = last_day_of_current_month - timedelta(days=last_day_of_current_month.day)

        # Obtener el valor de la UF según las condiciones
        if current_actual >= day_9_of_month:
            fecha = last_day_of_current_month

        else:
            fecha = last_day_of_previous_month

        response = self.get_uf(fecha)

        return response


    @classmethod
    def calcular_suma_uf(self, fecha_consulta):
        # Obtener el día actual y el día 9 del mes de la fecha de consulta
        dia_actual = fecha_consulta.day
        dia_9_del_mes = datetime(fecha_consulta.year, fecha_consulta.month, 9).day

        # Calcular la fecha del último día del mes de la fecha de consulta
        ultimo_dia_del_mes_actual = datetime(fecha_consulta.year, fecha_consulta.month, 1) + timedelta(days=31)
        while ultimo_dia_del_mes_actual.month != fecha_consulta.month:
            ultimo_dia_del_mes_actual -= timedelta(days=1)

        # Calcular la fecha del último día del mes anterior de la fecha de consulta
        ultimo_dia_del_mes_anterior = ultimo_dia_del_mes_actual - timedelta(days=ultimo_dia_del_mes_actual.day)

        # Obtener el valor de la UF según las condiciones
        if dia_actual >= dia_9_del_mes:
            # Usar el valor de la UF del último día del mes actual
            valor_uf = 12345  # Reemplaza esto con el valor real de la UF
        else:
            # Usar el valor de la UF del último día del mes anterior
            valor_uf = 67890  # Reemplaza esto con el valor real de la UF

        # Realizar la suma
        resultado = 1 + valor_uf

        return resultado