import json
import math
import requests

from datetime import datetime, timedelta
from decouple import config

from django.utils import timezone
from django.db.models import F

from applications.attendance.models import MarkAttendance
from applications.base.models import TablaGeneral

from applications.empresa.models import Afp, Salud
from applications.remuneracion.indicadores import IndicatorEconomic
from applications.usuario.models import ConceptUser, UsuarioEmpresa

from pytz import utc, timezone as pytz_timezone

class Remunerations():

    MINIMUM_SALARY = 460000
    TOPE_GRATIFICATION = 4.75
    CLOSE_DATE = 20
    TIEMPO_COLACION = 30
    HORA_ENTRADA = "08:30"
    HORA_SALIDA = "17:30"
    RANGO_HORAS_ATRASO = 1.5
    SE_REALIZAN_CARGOS_POR_ATRASOS = True
    SE_AUTORIZO_HORAS_EXTRAS = True


    @classmethod
    def format_number(self, number):
        """
        Toma un número y devuelve una cadena con separadores de miles (comas).
        """
        return ('{:,}'.format(number)).replace(',', '.')

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
        :return: 
            valor del impuesto en int
        """
        
        monthly_income_tax_parameters = TablaGeneral.objects.filter(tg_nombretabla = 'tb_tax_second_category')
        list_income_tax_percentage = []

        for value in monthly_income_tax_parameters:
            value_one = value.tg_value_one
            
            # Reemplazar comillas simples por comillas dobles
            string_json = value_one.replace("'", "\"")

            # Analizar el string JSON y convertirlo en un diccionario de Python
            dictionary = json.loads(string_json)

            list_income_tax_percentage.append(dictionary)

        porcentaje_impuesto_renta = 0
        for value in list_income_tax_percentage:
            if value['desde'] <= salary_imponible_mount <= value['hasta']:
                porcentaje_impuesto_renta = salary_imponible_mount * value['factor'] - value['cantidad_a_rebajar']

        return {
            'amount_tax': int(porcentaje_impuesto_renta),
            'concept': f'Impuesto a la renta (sobre: {salary_imponible_mount})'
        }
        
    @classmethod
    def translate_month(self, month, language = 'es_cl'):
        """
        translate_month - Funcion obtiene el mes en español

        :param month: mes a consultar
        :param language: lenguaje a traducir, por defecto es en español chileno
        :return: 
            translation retorna el mes consultado
        """

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
        """
        calculate_sesantia_insurance - Funcion que calcula el valor del seguro de cesantia
        
        :param salary_imponible_mount: monto del salario imponible
        :param contract_type: tipo de contrarto para determinar el porcentaje del descuento
        :return: 
            un diccionario con los montos correspondientes al aporte del empleado y el empleador
        """

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
    def calculate_afp_quote(self, afp_id, type_of_work, salary_imponible_mount):
        """
        calculate_afp_quote - Funcion que se encarga de ontener el monto a descontar de una AFP
        
        :param afp_id: ID de la AFP
        :param type_of_work: tipo de trabajador puede ser independiente o dependiente
        :param salary_imponible_mount: monto de salario imponible
        :return: 
            un diccionario con los montos y datos de el descuento y la AFP
        """

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
        if float(salary_imponible_mount) > uf_tope:
            salary_imponible_mount = uf_tope
            description_tope = True

        quote_afp = int(float(salary_imponible_mount) * (quote_rate / 100))
        return {
            'discount_afp': quote_afp,
            'afp_nombre': objects_afp[0].afp_nombre,
            'quote_rate': quote_rate,
            'description_tope': description_tope
        }
    
    @classmethod
    def calculate_health_discount(self, salary_imponible_mount, health_entity, quantity_uf_health):

        """
        calculate_health_discount - Funcion que se encarga de ontener el monto a descontar de salud
        
        :param salary_imponible_mount: monto de salario imponible
        :param health_entity: ID de la entidad de salud
        :param quantity_uf_health: cantidad de uf para el caso de las isapres
        :return: 
            un diccionario con los montos y datos de el descuento de salud
        """

        # La tasa de descuento máxima para la salud en Chile es del 7%
        maximum_discount_rate = 0.07
        health_discount = int(salary_imponible_mount) * maximum_discount_rate
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
        
    @classmethod
    def ordinary_hour_value(self, hours, rent):
        """
        ordinary_hour_value - Funcion para calcular el valor de la hora oridinaria
        
        :param hours(float): horas extras trabajadas
        :param rent: Renta del colaborador
        
        :return: 
            el monto de la hora ordinaria
        """
        pass

        
    @classmethod
    def calculate_overtime_hour(self, hours, rent, days_work=30, weekly_hours=45):
        """
        calculate_overtime_hour - Funcion para calcular el valor de la hora extra, y el valor de las hora extras
        
        :param user_id: id del usuario
        :param hours(float): horas extras trabajadas
        :param rent: Renta del colaborador
        
        :return: 
            un diccionario con el valor de la hora extra y el valor total de las horas extras trabajadas
        """

        #extra_hour_value = int(math.ceil(rent / days_work * 7 / weekly_hours * 1.5))
        # total_value_extra_hour = int(math.ceil(extra_hour_value * hours))
        extra_hour_value = int(rent / days_work * 7 / weekly_hours * 1.5)
        total_value_extra_hour = int(math.ceil(extra_hour_value * hours))

        return {
            "extra_hour_value": extra_hour_value,
            "total_value_extra_hour": total_value_extra_hour
        }

    @classmethod
    def get_detail_of_hours_worked(self, user_id):
        """
        get_detail_of_hours_worked - Funcion que se encarga de obtener el detalle de las horas trabajadas
        
        :param user_id: id del usuario
        
        :return: 
            un diccionario con la informacion de las horas trabajadas, horas de atraso, y horas de sobra
        """

        minutos_a_restar = self.TIEMPO_COLACION

        # Obtiene la fecha y hora actual
        current_date = datetime.now()

        # Obtiene el año actual
        current_year = datetime.now().year

        # Obtiene el dia actual
        current_day = datetime.now().day

        # Obtiene el número del mes actual
        current_month = current_date.month

        # Calcula el número del mes anterior prev_month
        if current_month == 1:
            prev_month = 12
        else:
            prev_month = current_month - 1

        # Define el rango de fechas deseado en UTC-3
        fecha_inicio_utc3 = pytz_timezone("America/Santiago").localize(datetime(current_year, prev_month, (self.CLOSE_DATE+1), 0, 0, 0))
        fecha_fin_utc3 = pytz_timezone("America/Santiago").localize(datetime(current_year, current_month, self.CLOSE_DATE, 23, 59, 59))

        # Filtra las marcas de asistencia dentro del rango de fechas y convierte a UTC-3
        marcas_en_rango = MarkAttendance.objects.filter(
            ma_datemark__gte=fecha_inicio_utc3.astimezone(utc),
            ma_datemark__lt=fecha_fin_utc3.astimezone(utc),
            ma_typeattendance__in=[1, 2],
            user_id = user_id
        ).order_by('ma_datemark')

        days_worked = int((marcas_en_rango.count()) / 2)

        resultados = []

        # Procesa las marcas de asistencia para calcular horas y minutos entre ellas
        delay_sum = 0 # aqui se acomula el total de los atrasos
        sum_overtime_hours = 0 # aqui se acomula el total de las horas extras
        
        for i in range(0, len(marcas_en_rango), 2):

            marca_entrada = marcas_en_rango[i]
            marca_salida = marcas_en_rango[i + 1]

            # Convierte las fechas a UTC-3
            fecha_entrada_utc3 = marca_entrada.ma_datemark.astimezone(pytz_timezone("America/Santiago"))
            fecha_salida_utc3 = marca_salida.ma_datemark.astimezone(pytz_timezone("America/Santiago"))

            horario_entrada = datetime.strptime(f"{fecha_entrada_utc3.year}-{fecha_entrada_utc3.month}-{fecha_entrada_utc3.day} {self.HORA_ENTRADA}", "%Y-%m-%d %H:%M").astimezone(pytz_timezone("America/Santiago"))
            horario_salida = datetime.strptime(f"{fecha_entrada_utc3.year}-{fecha_entrada_utc3.month}-{fecha_entrada_utc3.day} {self.HORA_SALIDA}", "%Y-%m-%d %H:%M").astimezone(pytz_timezone("America/Santiago"))

            # Calcula la diferencia de tiempo entre la marca de entrada y salida
            tiempo_transcurrido = fecha_salida_utc3 - fecha_entrada_utc3

            minutos_totales = tiempo_transcurrido.total_seconds() / 60

            # Restar los minutos deseados
            minutos_restantes = minutos_totales - minutos_a_restar

            if minutos_restantes < 0:
                minutos_restantes = 0

            horas_resultantes = minutos_restantes // 60
            minutos_resultantes = minutos_restantes % 60

            
            if fecha_entrada_utc3 >= horario_entrada:
                atraso = max((fecha_entrada_utc3 - horario_entrada).seconds // 60, 0)
            else:
                atraso = 0
            # Calcular atraso y horas extras
            
            delay_sum += int(atraso)

            if fecha_salida_utc3 > horario_salida:
                overtime_hours = max((fecha_salida_utc3 - horario_salida).seconds // 60, 0)
            else:
                overtime_hours = 0

            sum_overtime_hours += overtime_hours
            
            resultado = {
                "fecha_entrada": fecha_entrada_utc3.strftime("%Y-%m-%d %H:%M"),
                "fecha_salida": fecha_salida_utc3.strftime("%Y-%m-%d %H:%M"),
                "horas": horas_resultantes,
                "minutos": minutos_resultantes,
                "atraso": atraso,
                "horas_extras": overtime_hours,
            }

            resultados.append(resultado)

        return {
            "total_horas_atraso": round((delay_sum/60), 1),
            "total_horas_extras": round((sum_overtime_hours/60), 1),
            "dias_trabajados": days_worked,
            "detalle": resultados,
        }
    
    @classmethod
    def calculate_delay_value(self, hours_delay, taxable_assets, days_work=30, weekly_hours=45):
        """
        calculate_delay_value - Funcion que se encarga calcular el valor total de las horas de atraso a descontar
        
        :param hours_delay: cantidad de horas de atrasos
        :param taxable_assets: Es la suma de todos los habere imponibles, denominandoze como sueldo base
        :param ue_horassemanales: horas semanales del colaborador
        
        :return: 
            monto total de horas para descontar
        """
        hours_value = (taxable_assets/days_work*7/weekly_hours) * hours_delay

        return int(math.ceil(hours_value))

    @classmethod
    def generate_remunaration(self, user_id):

        """
        generate_remunaration - Funcion que se encarga de generar la remuneracion del colaborador
        
        :param user_id: id del usuario
        
        :return: 
            un diccionario con toda la información de la remuneracion
        """

        object_concept_user = ConceptUser.objects.filter(user_id = user_id)
        object_usuario_empresa = UsuarioEmpresa.objects.filter(user_id = user_id).first()

        object_taxable_assets = object_concept_user.filter(concept__conc_clasificationconcept = 1, concept__conc_typeconcept = 1) # obtiene los haberes imponibles

        taxable_assets = 0 # variable que almacena el total de haberes imponibles
        for obj in object_taxable_assets:
            taxable_assets += int(obj.cu_value)
        taxable_assets2 = taxable_assets

        object_monthly_salary = object_taxable_assets.filter(concept__conc_remuneration_type = 1)

        monthly_salary = 0 # sueldo mensual
        for obj in object_monthly_salary:
            monthly_salary += int(obj.cu_value)

        response_hours = self.get_detail_of_hours_worked(user_id)

        total_value_extra_hour = 0
        if self.SE_AUTORIZO_HORAS_EXTRAS: # -- VARIABLE DE ENTORNO QUE SE DEBE CREAR PARA VERIFICAR SI TIENE HORA EXTRA AUTORIZADA
            overtime_hours = self.calculate_overtime_hour(response_hours['total_horas_extras'], taxable_assets) # ***

            taxable_assets = taxable_assets + overtime_hours['total_value_extra_hour']
            total_value_extra_hour = overtime_hours['total_value_extra_hour']

        
        # el cliente determina si quiere descontar los atrasos
        if self.SE_REALIZAN_CARGOS_POR_ATRASOS:

            # desde aqui se valida el rango minimo de horas permitidas de atraso para realizar descuentos por atrasos
            if response_hours['total_horas_atraso'] > self.RANGO_HORAS_ATRASO:

                delay_value = self.calculate_delay_value(response_hours['total_horas_atraso'], taxable_assets2)  # ******
                taxable_assets -= delay_value


        objects_non_taxable_income = object_concept_user.filter(concept__conc_clasificationconcept = 1, concept__conc_typeconcept = 2) # obtiene los haberes no imponibles

        non_taxable_income = 0 # total haberes no imponibles
        for obj in objects_non_taxable_income:
            non_taxable_income += int(obj.cu_value)

        total_gross_salary = taxable_assets + non_taxable_income

        response_data = {
            "success": True,
            "status": 200,
            "total_haberes_imponibles": taxable_assets,
            "total_haberes_no_imponibles": non_taxable_income,
            "total_bruto": total_gross_salary,
            "valor_hora_ordinaria": total_gross_salary,
            "total_valor_hora_extra": total_value_extra_hour,
        }

        return response_data