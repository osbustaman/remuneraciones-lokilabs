# -*- encoding: utf-8 -*-
from django.core.management.base import BaseCommand
from app01.functions import load_data_base
from applications.base.models import Cliente, TablaGeneral

from lxml import html
import requests

from applications.remuneracion.indicadores import IndicatorEconomic

class Command(BaseCommand):

    help = 'ingresa el nombre de la nueva base'

    """def add_arguments(self, parser):
        parser.add_argument('base', type=str, help='ingresa el nombre de la nueva base')"""

    def handle(self, *args, **kwargs):

        """load_data_base()

        if kwargs['base'] == 'all_bases':
            lista = Cliente.objects.all()
        else:
            lista = Cliente.objects.filter(nombre_bd = kwargs['base'])"""

        # Import required modules
        
        list_variables = []
        # Request the page
        page = requests.get('https://www.previred.com/indicadores-previsionales/')
        
        # Parsing the page
        # (We need to use page.content rather than 
        # page.text because html.fromstring implicitly
        # expects bytes as input.)
        tree = html.fromstring(page.content)  

        uf_presente_mes = IndicatorEconomic.get_uf_value_last_day()

        print(float(uf_presente_mes['Valor'].replace('.', '').replace(',', '.')))
        list_variables.append()
        
        # Get element using XPath
        xpath_afiliados_afp = tree.xpath('//*[@id="p_p_id_56_INSTANCE_KQr4e6mJcSti_"]/div/div/div[1]/table/tbody/tr[2]/td[1]/text()')[0]
        tope_afiliados_afp = float(((xpath_afiliados_afp.split("(")[1]).split(" ")[0]).replace(",","."))

        list_variables.append({
            "cvr_name": "Tope afiliados AFP",
            "cvr_value": tope_afiliados_afp,
        })

        xpath_afiliados_ips = tree.xpath('//*[@id="p_p_id_56_INSTANCE_KQr4e6mJcSti_"]/div/div/div[1]/table/tbody/tr[3]/td[1]/text()')[0]
        tope_afiliados_ips = float(((xpath_afiliados_ips.split(") (")[1]).split(" ")[0]).replace(",","."))

        list_variables.append({
            "cvr_name": "Tope afiliados IPS(ex INP)",
            "cvr_value": tope_afiliados_ips,
        })


        xpath_afiliados_cesantia = tree.xpath('//*[@id="p_p_id_56_INSTANCE_KQr4e6mJcSti_"]/div/div/div[1]/table/tbody/tr[4]/td[1]/text()')[0]
        tope_afiliados_cesantia = float(((xpath_afiliados_cesantia.split("(")[1]).split(" ")[0]).replace(",","."))

        list_variables.append({
            "cvr_name": "Tope afiliados Cesantía",
            "cvr_value": tope_afiliados_cesantia,
        })

        xpath_ahorro_previsional_mensual = tree.xpath('//*[@id="p_p_id_56_INSTANCE_3WYryRoUZVvN_"]/div/div/div[1]/table/tbody/tr[2]/td[1]/text()')[0]
        ahorro_previsional_mensual = float(((xpath_ahorro_previsional_mensual.split("(")[1]).split(" ")[0]).replace(",","."))

        list_variables.append({
            "cvr_name": "Tope Mensual",
            "cvr_value": ahorro_previsional_mensual,
        })

        xpath_ahorro_previsional_anual = tree.xpath('//*[@id="p_p_id_56_INSTANCE_3WYryRoUZVvN_"]/div/div/div[1]/table/tbody/tr[3]/td[1]/text()')[0]
        ahorro_previsional_anual = float(((xpath_ahorro_previsional_anual.split("(")[1]).split(" ")[0]).replace(",","."))

        list_variables.append({
            "cvr_name": "Tope anual",
            "cvr_value": ahorro_previsional_anual,
        })


        print(tope_afiliados_cesantia)


        print(list_variables)


        """MINIMUM_SALARY = 460000
        TOPE_GRATIFICATION = 4.75
        CLOSE_DATE = 20
        TIEMPO_COLACION = 30
        HORA_ENTRADA = "08:30"
        HORA_SALIDA = "17:30"
        RANGO_HORAS_ATRASO = 1.5
        SE_REALIZAN_CARGOS_POR_ATRASOS = True
        SE_AUTORIZO_HORAS_EXTRAS = True"""