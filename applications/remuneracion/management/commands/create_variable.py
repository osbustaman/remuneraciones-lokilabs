# -*- encoding: utf-8 -*-
from django.core.management.base import BaseCommand
from app01.functions import load_data_base
from applications.base.models import Cliente, TablaGeneral

from lxml import html
import requests
import json

from applications.remuneracion.indicadores import IndicatorEconomic

class Command(BaseCommand):

    help = 'ingresa el nombre de la nueva base'

    def add_arguments(self, parser):
        parser.add_argument('base', type=str, help='ingresa el nombre de la nueva base')
    
    page = requests.get('https://www.previred.com/indicadores-previsionales/')
    
    def obtener_valor(self, cadena, separador_uno, separador_dos):
        
        tree = html.fromstring(self.page.content)  
        xpath_cadena = tree.xpath(f"{cadena}/text()")[0]
        return float((((xpath_cadena.split(separador_uno)[0]).split(separador_dos)[0]).replace(",","."))[:-1])
    
    def de_string_float_porcentaje(self, texto_numero):
        numero = float(texto_numero.replace(",",".")[:-1])
        return numero


    def handle(self, *args, **kwargs):

        load_data_base()

        if kwargs['base'] == 'all_bases':
            lista = Cliente.objects.all()
        else:
            lista = Cliente.objects.filter(nombre_bd = kwargs['base'])

        # Import required modules
        
        list_variables = []
        # Request the page
        page = self.page
        
        tree = html.fromstring(page.content)  

        uf_presente_mes = IndicatorEconomic.get_uf_value_last_day()
        valor_uf = float(uf_presente_mes['Valor'].replace('.', '').replace(',', '.'))
        
        # Get element using XPath
        xpath_afiliados_afp = tree.xpath('//*[@id="p_p_id_56_INSTANCE_KQr4e6mJcSti_"]/div/div/div[1]/table/tbody/tr[2]/td[1]/text()')[0]
        tope_afiliados_afp = float(((xpath_afiliados_afp.split("(")[1]).split(" ")[0]).replace(",","."))

        xpath_afiliados_ips = tree.xpath('//*[@id="p_p_id_56_INSTANCE_KQr4e6mJcSti_"]/div/div/div[1]/table/tbody/tr[3]/td[1]/text()')[0]
        tope_afiliados_ips = float(((xpath_afiliados_ips.split(") (")[1]).split(" ")[0]).replace(",","."))

        xpath_afiliados_cesantia = tree.xpath('//*[@id="p_p_id_56_INSTANCE_KQr4e6mJcSti_"]/div/div/div[1]/table/tbody/tr[4]/td[1]/text()')[0]
        tope_afiliados_cesantia = float(((xpath_afiliados_cesantia.split("(")[1]).split(" ")[0]).replace(",","."))

        list_variables.append({
            "cvr_name": "Renta topes imponibles",
            "cvr_value": [
                {
                    "name": f"Para afiliados a una AFP ({tope_afiliados_afp} UF)",
                    "value": int(round((tope_afiliados_afp * valor_uf), 0)),
                },{
                    "name": f"Para afiliados al IPS (ex INP) ({tope_afiliados_ips} UF)",
                    "value": int(round((tope_afiliados_ips * valor_uf), 0)),
                },{
                    "name": f"Para Seguro de Cesantía ({tope_afiliados_cesantia} UF)",
                    "value": int(round((tope_afiliados_cesantia * valor_uf), 0)),
                }
            ],
            "cvr_vartype": 1,
            "cvr_dict": False,
        })




        """
        **************************************************
        RENTAS MÍNIMAS IMPONIBLES
        **************************************************
        """

        # Utiliza el XPath para obtener la tabla
        xpath_afp_capital = '//*[@id="p_p_id_56_INSTANCE_z00IZRTURtAo_"]/div/div/div[1]/table'
        tabla = tree.xpath(xpath_afp_capital)

        # Asegúrate de que se haya encontrado la tabla
        if tabla:
            # Selecciona todos los elementos 'tr' dentro de la tabla
            tr_elementos = tabla[0].xpath('.//tr')

            # Inicializa la lista de filas
            filas = []
            list_data_rentas_minimas_imponibles = []
            for tr in tr_elementos:
                # Selecciona todos los elementos 'td' dentro de la fila que no tienen la clase 'encabezado_tabla_ind'
                td_elementos = tr.xpath('.//td[not(@class="encabezado_tabla_ind")]')
                fila = [td.text_content().strip() for td in td_elementos]

                # Agrega la fila a la lista de filas
                if fila:
                    filas.append(fila)

            # Imprime las filas
            for fila in filas:
                valor = int((fila[1].split(" ")[1]).replace(".", ""))
                list_data_rentas_minimas_imponibles.append({
                    "name": fila[0],
                    "value": valor,
                })

            list_variables.append({
                "cvr_name": "Rentas mínimas imponibles",
                "cvr_value": list_data_rentas_minimas_imponibles,
                "cvr_vartype": 1,
                "cvr_dict": False,
            })

                
        else:
            print("No se encontró la tabla con el XPath proporcionado.")


        xpath_ahorro_previsional_mensual = tree.xpath('//*[@id="p_p_id_56_INSTANCE_3WYryRoUZVvN_"]/div/div/div[1]/table/tbody/tr[2]/td[1]/text()')[0]
        ahorro_previsional_mensual = float(((xpath_ahorro_previsional_mensual.split("(")[1]).split(" ")[0]).replace(",","."))

        xpath_ahorro_previsional_anual = tree.xpath('//*[@id="p_p_id_56_INSTANCE_3WYryRoUZVvN_"]/div/div/div[1]/table/tbody/tr[3]/td[1]/text()')[0]
        ahorro_previsional_anual = float(((xpath_ahorro_previsional_anual.split("(")[1]).split(" ")[0]).replace(",","."))

        list_variables.append({
            "cvr_name": "Ahorro previsional voluntario (APV)",
            "cvr_value": [
                {
                    "name": f"Tope Mensual ({ahorro_previsional_mensual} UF)",
                    "value": int(round((ahorro_previsional_mensual * valor_uf), 0)),
                },{
                    "name": f"Tope Anual ({ahorro_previsional_anual} UF)",
                    "value": int(round((ahorro_previsional_anual * valor_uf), 0)),
                }
            ],
            "cvr_vartype": 1,
            "cvr_dict": False,
        })


        xpath_deposito_convenido = tree.xpath('//*[@id="p_p_id_56_INSTANCE_4jdY7Es6TfZ9_"]/div/div/div[1]/table/tbody/tr[2]/td[1]/text()')[0]
        deposito_convenido = float(((xpath_deposito_convenido.split("(")[1]).split(" ")[0]).replace(",","."))

        list_variables.append({
            "cvr_name": "Deposito convenido",
            "cvr_value": [{
                "name": f"Tope anual ({deposito_convenido} UF)",
                "value": int(round((deposito_convenido * valor_uf), 0)),
            }],
            "cvr_vartype": 1,
            "cvr_dict": False,
        })


        """
        **************************************************
        SEGURO DE CESANTÍA
        **************************************************
        """
        xpath_ss_monto_empleador_plazo_indefinido = '//*[@id="p_p_id_56_INSTANCE_88CmNZaRxRaO_"]/div/div/div/table/tbody/tr[4]/td[2]/strong'
        xpath_ss_monto_trabajador_plazo_indefinido = '//*[@id="p_p_id_56_INSTANCE_88CmNZaRxRaO_"]/div/div/div/table/tbody/tr[4]/td[3]/strong'

        xpath_ss_monto_empleador_plazo_fijo = '//*[@id="p_p_id_56_INSTANCE_88CmNZaRxRaO_"]/div/div/div/table/tbody/tr[5]/td[2]/strong'
        xpath_ss_monto_empleador_plazo_indefinido_11anios = '//*[@id="p_p_id_56_INSTANCE_88CmNZaRxRaO_"]/div/div/div/table/tbody/tr[6]/td[2]/strong'
        xpath_ss_monto_empleador_trabajador_casa_particular = '//*[@id="p_p_id_56_INSTANCE_88CmNZaRxRaO_"]/div/div/div/table/tbody/tr[7]/td[2]/strong'

        dict_seguro_sesantia = [
            {
                "contrato": "Plazo indefinido",
                "financiamiento": {
                    "empleador": self.obtener_valor(xpath_ss_monto_empleador_plazo_indefinido, " ", " "),
                    "trabajador": self.obtener_valor(xpath_ss_monto_trabajador_plazo_indefinido, " ", " "),
                }
            },{
                "contrato": "Plazo fijo",
                "financiamiento": {
                    "empleador": self.obtener_valor(xpath_ss_monto_empleador_plazo_fijo, " ", " "),
                    "trabajador": "-",
                }
            },{
                "contrato": "Plazo Indefinido 11 años o más",
                "financiamiento": {
                    "empleador": self.obtener_valor(xpath_ss_monto_empleador_plazo_indefinido_11anios, " ", " "),
                    "trabajador": "-",
                }
            },{
                "contrato": "Trabajador de Casa Particular",
                "financiamiento": {
                    "empleador": self.obtener_valor(xpath_ss_monto_empleador_trabajador_casa_particular, " ", " "),
                    "trabajador": "-",
                }
            }
        ]

        list_variables.append({
            "cvr_name": "Seguro de cesantía",
            "cvr_value": dict_seguro_sesantia,
            "cvr_vartype": 1,
            "cvr_dict": False,
        })


        """
        **************************************************
        TASA COTIZACIÓN OBLIGATORIO AFP
        **************************************************
        """

        # Utiliza el XPath para obtener la tabla
        xpath_afp_capital = '//*[@id="p_p_id_56_INSTANCE_wHYq7KvidomO_"]/div/div/div[1]/table'
        tabla = tree.xpath(xpath_afp_capital)

        # Asegúrate de que se haya encontrado la tabla
        if tabla:
            # Selecciona todos los elementos 'tr' dentro de la tabla
            tr_elementos = tabla[0].xpath('.//tr')

            # Inicializa la lista de filas
            filas = []
            list_data_afp = []
            for tr in tr_elementos:
                # Selecciona todos los elementos 'td' dentro de la fila que no tienen la clase 'encabezado_tabla_ind'
                td_elementos = tr.xpath('.//td[not(@class="encabezado_tabla_ind")]')
                fila = [td.text_content().strip() for td in td_elementos]

                # Agrega la fila a la lista de filas
                if fila:
                    filas.append(fila)

            # Imprime las filas
            for fila in filas:
                list_data_afp.append({
                    "afp": fila[0],
                    "trabajador_dependiente": {
                        "tasa_afp": self.de_string_float_porcentaje(fila[1]),
                        "tasa_sis": self.de_string_float_porcentaje(fila[2])
                    },
                    "trabajador_independiente": {
                        "tasa_afp": self.de_string_float_porcentaje(fila[3]),
                    }
                })
                
        else:
            print("No se encontró la tabla con el XPath proporcionado.")

        list_variables.append({
            "cvr_name": "Tasa cotización obligatoria AFP",
            "cvr_value": list_data_afp,
            "cvr_vartype": 1,
            "cvr_dict": False,
        })


        """
        **************************************************
        ASIGNACION FAMILIAR
        **************************************************
        """
        # Utiliza el XPath para obtener la tabla
        xpath_asignacion_familiar = '//*[@id="p_p_id_56_INSTANCE_BAg5Kc9VLFPt_"]/div/div/div[1]/table'
        tabla = tree.xpath(xpath_asignacion_familiar)

        # Asegúrate de que se haya encontrado la tabla
        if tabla:
            # Selecciona todos los elementos 'tr' dentro de la tabla
            tr_elementos = tabla[0].xpath('.//tr')

            # Inicializa la lista de filas
            filas = []
            list_data_asignacion_familiar = []
            for tr in tr_elementos:
                # Selecciona todos los elementos 'td' dentro de la fila que no tienen la clase 'encabezado_tabla_ind'
                td_elementos = tr.xpath('.//td[not(@class="encabezado_tabla_ind")]')
                fila = [td.text_content().strip() for td in td_elementos]

                # Agrega la fila a la lista de filas
                if fila:
                    filas.append(fila)

            # Imprime las filas
            contador = 1
            for fila in filas:
                tramo = fila[0].split(" ")[1]
                try:
                    monto = int((fila[1].split(" ")[1]).replace(".", ""))
                except:
                    monto = 0

                desde_hasta = fila[2].split(" ")
                
                hasta = int((desde_hasta[len(desde_hasta)-1]).replace(".", ""))
                

                if contador > 1 and contador < len(desde_hasta):
                    desde = int(desde_hasta[3].replace(".", ""))
                else:
                    desde = 0

                list_data_asignacion_familiar.append({
                    "tramo": tramo,
                    "monto": monto,
                    "requisitos": {
                        "desde": desde,
                        "hasta": hasta
                    },
                })

                contador+=1

            list_variables.append({
                "cvr_name": "asignación familiar",
                "cvr_value": list_data_asignacion_familiar,
                "cvr_vartype": 1,
                "cvr_dict": False,
            })

        else:
            print("No se encontró la tabla con el XPath proporcionado.")


        """
        **************************************************
        COTIZACIÓN PARA TRABAJOS PESADOS 
        **************************************************
        """
        # Utiliza el XPath para obtener la tabla
        xpath_trabajos_pesados = '//*[@id="p_p_id_56_INSTANCE_z7eabFMiT8St_"]/div/div[1]/div/table'
        tabla = tree.xpath(xpath_trabajos_pesados)

        # Asegúrate de que se haya encontrado la tabla
        if tabla:
            # Selecciona todos los elementos 'tr' dentro de la tabla
            tr_elementos = tabla[0].xpath('.//tr')

            # Inicializa la lista de filas
            filas = []
            list_data_cotizacion_trabajos_pesados = []
            for tr in tr_elementos:
                # Selecciona todos los elementos 'td' dentro de la fila que no tienen la clase 'encabezado_tabla_ind'
                td_elementos = tr.xpath('.//td[not(@class="encabezado_tabla_ind")]')
                fila = [td.text_content().strip() for td in td_elementos]

                # Agrega la fila a la lista de filas
                if fila:
                    filas.append(fila)

            # Imprime las filas
            contador = 1
            for fila in filas:

                porcentaje_puesto_trabajo = int((fila[2].split(" ")[0])[:-1]) + int((fila[3].split(" ")[0])[:-1])
                
                list_data_cotizacion_trabajos_pesados.append({
                    "puesto_trabajo": fila[0],
                    "porcentaje_puesto_trabajo": f"{porcentaje_puesto_trabajo}%",
                    "financiamiento": {
                        "empleador": int((fila[2].split(" ")[0])[:-1]),
                        "trabajador": int((fila[3].split(" ")[0])[:-1])
                    }
                })

            list_variables.append({
                "cvr_name": "cotizacion trabajos pesados",
                "cvr_value": list_data_cotizacion_trabajos_pesados,
                "cvr_vartype": 1,
                "cvr_dict": False,
            })

        else:
            print("No se encontró la tabla con el XPath proporcionado.")


        """
        **************************************************
        DISTRIBUCIÓN DEL 7% SALUD, PARA EMPLEADORES AFILIADO A CCAF (*)
        **************************************************
        """

        # Utiliza el XPath para obtener la tabla
        xpath_trabajos_pesados = '//*[@id="p_p_id_56_INSTANCE_3WYryRoUZVvN_"]/div/div/div/table'
        tabla = tree.xpath(xpath_trabajos_pesados)

        # Asegúrate de que se haya encontrado la tabla
        if tabla:

            xpath_valor_1 = tree.xpath('//*[@id="p_p_id_56_INSTANCE_3WYryRoUZVvN_"]/div/div/div/table/tbody/tr[2]/td[2]/strong/text()')[1]
            xpath_valor_2 = tree.xpath('//*[@id="p_p_id_56_INSTANCE_3WYryRoUZVvN_"]/div/div/div/table/tbody/tr[3]/td[2]/b/text()')[0]

            list_variables.append({
                "cvr_name": f"distribucion  7% salud empleadores afiliado ccaf",
                "cvr_value": [
                    {
                        "ccaf": int(xpath_valor_1.split(" ")[0]),
                        "fonasa": int(xpath_valor_2.split(" ")[0])
                    }
                ],
                "cvr_vartype": 1,
                "cvr_dict": False,
            })

        else:
            print("No se encontró la tabla con el XPath proporcionado.")


        cadena_json = json.dumps(list_variables)

        print(cadena_json)
        
    

    

        """MINIMUM_SALARY = 460000
        TOPE_GRATIFICATION = 4.75
        CLOSE_DATE = 20
        TIEMPO_COLACION = 30
        HORA_ENTRADA = "08:30"
        HORA_SALIDA = "17:30"
        RANGO_HORAS_ATRASO = 1.5
        SE_REALIZAN_CARGOS_POR_ATRASOS = True
        SE_AUTORIZO_HORAS_EXTRAS = True"""