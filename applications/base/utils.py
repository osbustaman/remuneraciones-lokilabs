import re
import django
import psycopg2
import os
import json
import requests
import datetime


import pandas as pd
import pdfkit
import base64

from django.core.management import call_command
from django.template.loader import get_template
from django import conf

from decouple import config
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from app01.settings.local import WKHTMLTOPDF_BIN_PATH

from applications.base.models import Cliente, Comuna, Pais, Region


def indicadores_economicos(indicador):
    indicadores = [
        'uf'
        , 'ivp'
        , 'dolar'
        , 'dolar_intercambio'
        , 'euro'
        , 'ipc'
        , 'utm'
        , 'imacec'
        , 'tpm'
        , 'libra_cobre'
        , 'tasa_desempleo'
        , 'bitcoin'
    ]

    fecha_actual = datetime.datetime.now()

    dia_actual = fecha_actual.day
    mes_actual = fecha_actual.month
    anio_actual = fecha_actual.year
    fecha_formateada = fecha_actual.strftime("%d-%m-%Y")

    url = f'https://mindicador.cl/api/{indicador}/{fecha_formateada}'
    response = requests.get(url)
    data = json.loads(response.text.encode("utf-8"))
    pretty_json = json.dumps(data, indent=2)
    return data

def getCliente(request):
    return Cliente.objects.filter(rut_cliente = request['rut_cliente']).exists()

def validarRut(rut):
    rut = rut.replace(".", "").replace("-", "") # Eliminar puntos y guiones
    if not re.match(r'^\d{1,8}[0-9K]$', rut): # Verificar formato
        return False
    rut_sin_dv = rut[:-1]
    dv = rut[-1].upper() # Obtener dígito verificador
    multiplicador = 2
    suma = 0
    for r in reversed(rut_sin_dv):
        suma += int(r) * multiplicador
        multiplicador += 1
        if multiplicador == 8:
            multiplicador = 2
    resto = suma % 11
    dv_calculado = 11 - resto
    if dv_calculado == 11:
        dv_calculado = '0'
    elif dv_calculado == 10:
        dv_calculado = 'K'
    else:
        dv_calculado = str(dv_calculado)
    return dv == dv_calculado

def create_database(request):

    ba_nombre = request['nombre_bd'].lower()

    try:
        # se crea la conexion
        conexion = psycopg2.connect(
            dbname='postgres', 
            user=config('USER'), 
            host=config('HOST'), 
            password=config('PASSWORD')
        )

        conexion.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    except Exception as inst:
        return {
            'label': 'DATABASE',
            'error': str(inst),
            'isError': True
        }


    cur = conexion.cursor()
    # se crea la base
    try:
        # se crea la base
        cur.execute("CREATE DATABASE %s ;" % ba_nombre)
    except Exception as inst:
        return {
            'label': 'CREATE DATABASE',
            'error': type(inst),
            'isError': True
        }

    return { 'isError': False }

def crearMigrate(request):

    try:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app01.settings.local")
        django.setup()

        nombre_bd = request['nombre_bd'].lower()

        nueva_base = {
            'ENGINE': conf.settings.DATABASES['default']['ENGINE'],
            'HOST': config('HOST'),
            'NAME': nombre_bd,
            'USER': config('USER'),
            'PASSWORD': config('PASSWORD'),
            'PORT': config('PORT')
        }
        conf.settings.DATABASES[nombre_bd] = nueva_base

        call_command('migrate', database=f'{nombre_bd}'.lower())
    except Exception as err:
        print(f'Error al conectar con el servidor: {err}')

def generate_pdf(html, isTemplate = False, name_template = False, data = {}):
    
    options = {
            'page-size': 'Letter',
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
        }

    pdfkit_config = pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_BIN_PATH)

    if isTemplate:
        file_template = f'pdf/{name_template}'
        template = get_template(file_template)
        html = template.render(data)

    pdf = pdfkit.from_string(html, False, options=options, configuration=pdfkit_config)
    pdf_base64 = base64.b64encode(pdf).decode('utf-8')

    return pdf_base64

def elige_choices(obj_choice, str):
    valor = ""
    for key, value in obj_choice:
        if key == str:
            valor = value
    return valor

def armarParametrosGeneralesDelSistema(request):

    nombre_bd = request['nombre_bd'].lower()

    la_base = Cliente.objects.get(nombre_bd=nombre_bd)
    ba_nombre = la_base.nombre_bd
    lst_log = []

    p = Pais.objects.using(ba_nombre).filter(pa_codigo=56)
    if not p.exists():
        pa = Pais()
        pa.pa_nombre = 'Chile'
        pa.pa_codigo = 56
        pa.save(using=ba_nombre)
        pais = pa
    else:
        pais = p[0]

    lst_regiones = [{
        're_nombre': 'Tarapacá',
        're_numeroregion': 'I',
        're_numero': 1,
        'comunas': [
            {'com_nombre': 'Iquique'},
            {'com_nombre': 'Alto Hospicio'},
            {'com_nombre': 'Pozo Almonte'},
            {'com_nombre': 'Camiña'},
            {'com_nombre': 'Colchane'},
            {'com_nombre': 'Huara'},
            {'com_nombre': 'Pica'},
        ]
    }, {
        're_nombre': 'Antofagasta',
        're_numeroregion': 'II',
        're_numero': 2,
        'comunas': [
            {'com_nombre': 'Antofagasta'},
            {'com_nombre': 'Mejillones'},
            {'com_nombre': 'Sierra Gorda'},
            {'com_nombre': 'Taltal'},
            {'com_nombre': 'Calama'},
            {'com_nombre': 'Ollagüe'},
            {'com_nombre': 'San Pedro de Atacama'},
            {'com_nombre': 'Tocopilla'},
            {'com_nombre': 'María Elena'},

        ]
    }, {
        're_nombre': 'Atacama',
        're_numeroregion': 'III',
        're_numero': 3,
        'comunas': [
            {'com_nombre': 'Copiapó'},
            {'com_nombre': 'Caldera'},
            {'com_nombre': 'Tierra Amarilla'},
            {'com_nombre': 'Chañaral'},
            {'com_nombre': 'Diego de Almagro'},
            {'com_nombre': 'Vallenar'},
            {'com_nombre': 'Alto del Carmen'},
            {'com_nombre': 'Freirina'},
            {'com_nombre': 'Huasco'},

        ]
    }, {
        're_nombre': 'Coquimbo',
        're_numeroregion': 'IV',
        're_numero': 4,
        'comunas': [
            {'com_nombre': 'Huasco'},
            {'com_nombre': 'La Serena'},
            {'com_nombre': 'Coquimbo'},
            {'com_nombre': 'Andacollo'},
            {'com_nombre': 'La Higuera'},
            {'com_nombre': 'Paiguano'},
            {'com_nombre': 'Vicuña'},
            {'com_nombre': 'Illapel'},
            {'com_nombre': 'Canela'},
            {'com_nombre': 'Los Vilos'},
            {'com_nombre': 'Salamanca'},
            {'com_nombre': 'Ovalle'},
            {'com_nombre': 'Combarbalá'},
            {'com_nombre': 'Monte Patria'},
            {'com_nombre': 'Punitaqui'},
            {'com_nombre': 'Río Hurtado'},

        ]
    }, {
        're_nombre': 'Valparaiso',
        're_numeroregion': 'V',
        're_numero': 5,
        'comunas': [
            {'com_nombre': 'Río Hurtado'},
            {'com_nombre': 'Valparaíso'},
            {'com_nombre': 'Casablanca'},
            {'com_nombre': 'Concón'},
            {'com_nombre': 'Juan Fernández'},
            {'com_nombre': 'Puchuncaví'},
            {'com_nombre': 'Quilpué'},
            {'com_nombre': 'Quintero'},
            {'com_nombre': 'Villa Alemana'},
            {'com_nombre': 'Viña del Mar'},
            {'com_nombre': 'Isla de Pascua'},
            {'com_nombre': 'Los Andes'},
            {'com_nombre': 'Calle Larga'},
            {'com_nombre': 'Rinconada'},
            {'com_nombre': 'San Esteban'},
            {'com_nombre': 'La Ligua'},
            {'com_nombre': 'Cabildo'},
            {'com_nombre': 'Papudo'},
            {'com_nombre': 'Petorca'},
            {'com_nombre': 'Zapallar'},
            {'com_nombre': 'Quillota'},
            {'com_nombre': 'Calera'},
            {'com_nombre': 'Hijuelas'},
            {'com_nombre': 'La Cruz'},
            {'com_nombre': 'Limache'},
            {'com_nombre': 'Nogales'},
            {'com_nombre': 'Olmué'},
            {'com_nombre': 'San Antonio'},
            {'com_nombre': 'Algarrobo'},
            {'com_nombre': 'Cartagena'},
            {'com_nombre': 'El Quisco'},
            {'com_nombre': 'El Tabo'},
            {'com_nombre': 'Santo Domingo'},
            {'com_nombre': 'San Felipe'},
            {'com_nombre': 'Catemu'},
            {'com_nombre': 'Llaillay'},
            {'com_nombre': 'Panquehue'},
            {'com_nombre': 'Putaendo'},
            {'com_nombre': 'Santa María'},

        ]
    }, {
        're_nombre': 'Metropolitana de Santiago',
        're_numeroregion': 'RM',
        're_numero': 13,
        'comunas': [
            {'com_nombre': 'Santiago'},
            {'com_nombre': 'Cerrillos'},
            {'com_nombre': 'Cerro Navia'},
            {'com_nombre': 'Conchalí'},
            {'com_nombre': 'El Bosque'},
            {'com_nombre': 'Estación Central '},
            {'com_nombre': 'Huechuraba'},
            {'com_nombre': 'Independencia'},
            {'com_nombre': 'La Cisterna'},
            {'com_nombre': 'La Florida'},
            {'com_nombre': 'La Pintana'},
            {'com_nombre': 'La Granja'},
            {'com_nombre': 'La Reina'},
            {'com_nombre': 'Las Condes'},
            {'com_nombre': 'Lo Barnechea'},
            {'com_nombre': 'Lo Espejo'},
            {'com_nombre': 'Lo Prado'},
            {'com_nombre': 'Macul'},
            {'com_nombre': 'Maipú'},
            {'com_nombre': 'Ñuñoa'},
            {'com_nombre': 'Pedro Aguirre Cerda'},
            {'com_nombre': 'Peñalolén'},
            {'com_nombre': 'Providencia'},
            {'com_nombre': 'Pudahuel'},
            {'com_nombre': 'Quilicura'},
            {'com_nombre': 'Quinta Normal'},
            {'com_nombre': 'Recoleta'},
            {'com_nombre': 'Renca'},
            {'com_nombre': 'San Joaquín'},
            {'com_nombre': 'San Miguel'},
            {'com_nombre': 'San Ramón'},
            {'com_nombre': 'Vitacura'},
            {'com_nombre': 'Puente Alto'},
            {'com_nombre': 'Pirque'},
            {'com_nombre': 'San José de Maipo'},
            {'com_nombre': 'Colina'},
            {'com_nombre': 'Lampa'},
            {'com_nombre': 'Tiltil'},
            {'com_nombre': 'San Bernardo'},
            {'com_nombre': 'Buin'},
            {'com_nombre': 'Calera de Tango'},
            {'com_nombre': 'Paine'},
            {'com_nombre': 'Melipilla'},
            {'com_nombre': 'Alhué'},
            {'com_nombre': 'Curacaví'},
            {'com_nombre': 'María Pinto'},
            {'com_nombre': 'San Pedro'},
            {'com_nombre': 'Talagante'},
            {'com_nombre': 'El Monte'},
            {'com_nombre': 'Isla de Maipo'},
            {'com_nombre': 'Padre Hurtado'},
            {'com_nombre': 'Peñaflor'},

        ]
    }, {
        're_nombre': 'Libertador General Bernardo O\'Higgins',
        're_numeroregion': 'VI',
        're_numero': 6,
        'comunas': [
            {'com_nombre': 'Rancagua'},
            {'com_nombre': 'Codegua'},
            {'com_nombre': 'Coinco'},
            {'com_nombre': 'Coltauco'},
            {'com_nombre': 'Doñihue'},
            {'com_nombre': 'Graneros'},
            {'com_nombre': 'Las Cabras'},
            {'com_nombre': 'Machalí'},
            {'com_nombre': 'Malloa'},
            {'com_nombre': 'Mostazal'},
            {'com_nombre': 'Olivar'},
            {'com_nombre': 'Peumo'},
            {'com_nombre': 'Pichidegua'},
            {'com_nombre': 'Quinta de Tilcoco'},
            {'com_nombre': 'Rengo'},
            {'com_nombre': 'Requínoa'},
            {'com_nombre': 'San Vicente'},
            {'com_nombre': 'Pichilemu'},
            {'com_nombre': 'La Estrella'},
            {'com_nombre': 'Litueche'},
            {'com_nombre': 'Marchihue'},
            {'com_nombre': 'Navidad'},
            {'com_nombre': 'Paredones'},
            {'com_nombre': 'San Fernando'},
            {'com_nombre': 'Chépica'},
            {'com_nombre': 'Chimbarongo'},
            {'com_nombre': 'Lolol'},
            {'com_nombre': 'Nancagua'},
            {'com_nombre': 'Palmilla'},
            {'com_nombre': 'Peralillo'},
            {'com_nombre': 'Placilla'},
            {'com_nombre': 'Pumanque'},
            {'com_nombre': 'Santa Cruz'},
        ]
    }, {
        're_nombre': 'Maule',
        're_numeroregion': 'VII',
        're_numero': 7,
        'comunas': [
            {'com_nombre': 'Talca'},
            {'com_nombre': 'Constitución'},
            {'com_nombre': 'Curepto'},
            {'com_nombre': 'Empedrado'},
            {'com_nombre': 'Maule'},
            {'com_nombre': 'Pelarco'},
            {'com_nombre': 'Pencahue'},
            {'com_nombre': 'Río Claro'},
            {'com_nombre': 'San Clemente'},
            {'com_nombre': 'San Rafael'},
            {'com_nombre': 'Cauquenes'},
            {'com_nombre': 'Chanco'},
            {'com_nombre': 'Pelluhue'},
            {'com_nombre': 'Curicó'},
            {'com_nombre': 'Hualañé'},
            {'com_nombre': 'Licantén'},
            {'com_nombre': 'Molina'},
            {'com_nombre': 'Rauco'},
            {'com_nombre': 'Romeral'},
            {'com_nombre': 'Sagrada Familia'},
            {'com_nombre': 'Teno'},
            {'com_nombre': 'Vichuquén'},
            {'com_nombre': 'Linares'},
            {'com_nombre': 'Colbún'},
            {'com_nombre': 'Longaví'},
            {'com_nombre': 'Parral'},
            {'com_nombre': 'Retiro'},
            {'com_nombre': 'San Javier'},
            {'com_nombre': 'Villa Alegre'},
            {'com_nombre': 'Yerbas Buenas'},
        ]
    }, {
        're_nombre': 'Biobío',
        're_numeroregion': 'VIII',
        're_numero': 8,
        'comunas': [
            {'com_nombre': 'Concepción'},
            {'com_nombre': 'Coronel'},
            {'com_nombre': 'Chiguayante'},
            {'com_nombre': 'Florida'},
            {'com_nombre': 'Hualqui'},
            {'com_nombre': 'Lota'},
            {'com_nombre': 'Penco'},
            {'com_nombre': 'San Pedro de la Paz'},
            {'com_nombre': 'Santa Juana'},
            {'com_nombre': 'Talcahuano'},
            {'com_nombre': 'Tomé'},
            {'com_nombre': 'Hualpén'},
            {'com_nombre': 'Lebu'},
            {'com_nombre': 'Arauco'},
            {'com_nombre': 'Cañete'},
            {'com_nombre': 'Contulmo'},
            {'com_nombre': 'Curanilahue'},
            {'com_nombre': 'Los Álamos'},
            {'com_nombre': 'Tirúa'},
            {'com_nombre': 'Los Ángeles'},
            {'com_nombre': 'Antuco'},
            {'com_nombre': 'Cabrero'},
            {'com_nombre': 'Laja'},
            {'com_nombre': 'Mulchén'},
            {'com_nombre': 'Nacimiento'},
            {'com_nombre': 'Negrete'},
            {'com_nombre': 'Quilaco'},
            {'com_nombre': 'Quilleco'},
            {'com_nombre': 'San Rosendo'},
            {'com_nombre': 'Santa Bárbara'},
            {'com_nombre': 'Tucapel'},
            {'com_nombre': 'Yumbel'},
            {'com_nombre': 'Alto Bío-Bío'},
            {'com_nombre': 'Chillán'},
            {'com_nombre': 'Bulnes'},
            {'com_nombre': 'Cobquecura'},
            {'com_nombre': 'Coelemu'},
            {'com_nombre': 'Coihueco'},
            {'com_nombre': 'Chillán Viejo'},
            {'com_nombre': 'El Carmen'},
            {'com_nombre': 'Ninhue'},
            {'com_nombre': 'Ñiquén'},
            {'com_nombre': 'Pemuco'},
            {'com_nombre': 'Pinto'},
            {'com_nombre': 'Portezuelo'},
            {'com_nombre': 'Quillón'},
            {'com_nombre': 'Quirihue'},
            {'com_nombre': 'Ránquil'},
            {'com_nombre': 'San Carlos'},
            {'com_nombre': 'San Fabián'},
            {'com_nombre': 'San Ignacio'},
            {'com_nombre': 'San Nicolás'},
            {'com_nombre': 'Treguaco'},
            {'com_nombre': 'Yungay'},
        ]
    }, {
        're_nombre': 'La Araucanía',
        're_numeroregion': 'IX',
        're_numero': 9,
        'comunas': [
            {'com_nombre': 'Temuco'},
            {'com_nombre': 'Carahue'},
            {'com_nombre': 'Cunco'},
            {'com_nombre': 'Curarrehue'},
            {'com_nombre': 'Freire'},
            {'com_nombre': 'Galvarino'},
            {'com_nombre': 'Gorbea'},
            {'com_nombre': 'Lautaro'},
            {'com_nombre': 'Loncoche'},
            {'com_nombre': 'Melipeuco'},
            {'com_nombre': 'Nueva Imperial'},
            {'com_nombre': 'Padre las Casas'},
            {'com_nombre': 'Perquenco'},
            {'com_nombre': 'Pitrufquén'},
            {'com_nombre': 'Pucón'},
            {'com_nombre': 'Saavedra'},
            {'com_nombre': 'Teodoro Schmidt'},
            {'com_nombre': 'Toltén'},
            {'com_nombre': 'Vilcún'},
            {'com_nombre': 'Villarrica'},
            {'com_nombre': 'Cholchol'},
            {'com_nombre': 'Angol'},
            {'com_nombre': 'Collipulli'},
            {'com_nombre': 'Curacautín'},
            {'com_nombre': 'Ercilla'},
            {'com_nombre': 'Lonquimay'},
            {'com_nombre': 'Los Sauces'},
            {'com_nombre': 'Lumaco'},
            {'com_nombre': 'Purén'},
            {'com_nombre': 'Renaico'},
            {'com_nombre': 'Traiguén'},
            {'com_nombre': 'Victoria'},
        ]
    }, {
        're_nombre': 'Los Lagos',
        're_numeroregion': 'X',
        're_numero': 10,
        'comunas': [
            {'com_nombre': 'Puerto Montt'},
            {'com_nombre': 'Calbuco'},
            {'com_nombre': 'Cochamó'},
            {'com_nombre': 'Fresia'},
            {'com_nombre': 'Frutillar'},
            {'com_nombre': 'Los Muermos'},
            {'com_nombre': 'Llanquihue'},
            {'com_nombre': 'Maullín'},
            {'com_nombre': 'Puerto Varas'},
            {'com_nombre': 'Castro'},
            {'com_nombre': 'Ancud'},
            {'com_nombre': 'Chonchi'},
            {'com_nombre': 'Curaco de Vélez'},
            {'com_nombre': 'Dalcahue'},
            {'com_nombre': 'Puqueldón'},
            {'com_nombre': 'Queilén'},
            {'com_nombre': 'Quellón'},
            {'com_nombre': 'Quemchi'},
            {'com_nombre': 'Quinchao'},
            {'com_nombre': 'Osorno'},
            {'com_nombre': 'Puerto Octay'},
            {'com_nombre': 'Purranque'},
            {'com_nombre': 'Puyehue'},
            {'com_nombre': 'Río Negro'},
            {'com_nombre': 'San Juan de La Costa'},
            {'com_nombre': 'San Pablo'},
            {'com_nombre': 'Chaitén'},
            {'com_nombre': 'Futaleufú'},
            {'com_nombre': 'Hualaihué'},
            {'com_nombre': 'Palena'},
        ]
    }, {
        're_nombre': 'Aisén del General Carlos Ibáñez del Campo',
        're_numeroregion': 'XI',
        're_numero': 11,
        'comunas': [
            {'com_nombre': 'Coihaique'},
            {'com_nombre': 'Lago Verde'},
            {'com_nombre': 'Aysen'},
            {'com_nombre': 'Cisnes'},
            {'com_nombre': 'Guaitecas'},
            {'com_nombre': 'Cochrane'},
            {'com_nombre': 'O\'Higgins'},
            {'com_nombre': 'Tortel'},
            {'com_nombre': 'Chile Chico'},
            {'com_nombre': 'Río Ibáñez'},
        ]
    }, {
        're_nombre': 'Magallanes y de la Antártica Chilena',
        're_numeroregion': 'XII',
        're_numero': 12,
        'comunas': [
            {'com_nombre': 'Punta Arenas'},
            {'com_nombre': 'Laguna Blanca'},
            {'com_nombre': 'Río Verde'},
            {'com_nombre': 'San Gregorio'},
            {'com_nombre': 'Cabo de Hornos'},
            {'com_nombre': 'Antártica'},
            {'com_nombre': 'Porvenir'},
            {'com_nombre': 'Primavera'},
            {'com_nombre': 'Timaukel'},
            {'com_nombre': 'Natales'},
            {'com_nombre': 'Torres del Paine'},
        ]
    }, {
        're_nombre': 'Los Ríos',
        're_numeroregion': 'XIV',
        're_numero': 14,
        'comunas': [
            {'com_nombre': 'Valdivia'},
            {'com_nombre': 'Corral'},
            {'com_nombre': 'Lanco'},
            {'com_nombre': 'Los Lagos'},
            {'com_nombre': 'Máfil'},
            {'com_nombre': 'Mariquina'},
            {'com_nombre': 'Paillaco'},
            {'com_nombre': 'Panguipulli'},
            {'com_nombre': 'La Unión'},
            {'com_nombre': 'Futrono'},
            {'com_nombre': 'Lago Ranco'},
            {'com_nombre': 'Río Bueno'},
        ]
    }, {
        're_nombre': 'Arica y Parinacota',
        're_numeroregion': 'XV',
        're_numero': 15,
        'comunas': [
            {'com_nombre': 'Arica'},
            {'com_nombre': 'Camarones'},
            {'com_nombre': 'Putre'},
            {'com_nombre': 'General Lagos'},
        ]
    }]
    #

    for r in lst_regiones:
        re = Region.objects.using(ba_nombre).filter(re_numero=r['re_numero'])
        if not re.exists():
            re = Region()
            re.re_nombre = r['re_nombre']
            re.pais = pais
            re.re_numeroregion = r['re_numeroregion']
            re.re_numero = r['re_numero']
            re.save(using=ba_nombre)

            for c in r['comunas']:
                co = Comuna()
                co.com_nombre = c['com_nombre']
                co.region = re
                co.save(using=ba_nombre)
        else:
            pass


