# -*- encoding: utf-8 -*-
from django.core.management.base import BaseCommand
from app01.functions import load_data_base

from applications.base.models import Cliente
from applications.empresa.models import Afp, Banco, TipoContrato, CajasCompensacion, Salud

class Command(BaseCommand):

    help = 'ingresa el nombre de la nueva base'

    def add_arguments(self, parser):
        parser.add_argument('base', type=str, help='ingresa el nombre de la nueva base')

    def handle(self, *args, **kwargs):

        load_data_base()

        if kwargs['base'] == 'all_bases':
            lista = Cliente.objects.all()
        else:
            lista = Cliente.objects.filter(nombre_bd = kwargs['base'])

        listado_tipo_contratos = [
            {
                'tc_codcontrato': 'CI',
                'tc_nombrecontrato': 'Contrato duración indefinida'
            },
            {
                'tc_codcontrato': 'CPF',
                'tc_nombrecontrato': 'Contrato plazo fijo'
            },
            {
                'tc_codcontrato': 'CIT',
                'tc_nombrecontrato': 'Contrato individual de trabajo'
            },
            {
                'tc_codcontrato': 'CPO',
                'tc_nombrecontrato': 'Contrato por obra'
            },

            {
                'tc_codcontrato': 'CJP',
                'tc_nombrecontrato': 'Contrato jornada parcial'
            },
            {
                'tc_codcontrato': 'CPT',
                'tc_nombrecontrato': 'Contrato part-time'
            },
            {
                'tc_codcontrato': 'CE',
                'tc_nombrecontrato': 'Contrato especial'
            },
            {
                'tc_codcontrato': 'INA',
                'tc_nombrecontrato': 'Inactivo'
            },
        ]

        listado_bancos = [
            {
                'ban_nombre': 'BANCO DE CHILE / Edwards ',
                'ban_codigo': '001'
            },
            {
                'ban_nombre': 'BANCO INTERNACIONAL',
                'ban_codigo': '009'
            },
            {
                'ban_nombre': 'SCOTIABANK CHILE',
                'ban_codigo': '014'
            },
            {
                'ban_nombre': 'BANCO DE CREDITO E INVERSIONES',
                'ban_codigo': '016'
            },
            {
                'ban_nombre': 'BANCO BICE',
                'ban_codigo': '028'
            },
            {
                'ban_nombre': 'HSBC BANK (CHILE)',
                'ban_codigo': '031'
            },
            {
                'ban_nombre': 'BANCO SANTANDER-CHILE',
                'ban_codigo': '037'
            },
            {
                'ban_nombre': 'ITAÚ CORPBANCA',
                'ban_codigo': '039'
            },
            {
                'ban_nombre': 'BANCO SECURITY',
                'ban_codigo': '049'
            },
            {
                'ban_nombre': 'BANCO FALABELLA',
                'ban_codigo': '051'
            },
            {
                'ban_nombre': 'BANCO RIPLEY',
                'ban_codigo': '053'
            },
            {
                'ban_nombre': 'BANCO CONSORCIO',
                'ban_codigo': '055'
            },
            {
                'ban_nombre': 'SCOTIABANK AZUL',
                'ban_codigo': '504'
            },
            {
                'ban_nombre': 'BANCO BTG PACTUAL CHILE',
                'ban_codigo': '059'
            },
        ]

        listado_cajas_compensasion = [
            {
                'cc_nombre': 'Caja los Andes',
                'cc_codigo': '04',
            },{
                'cc_nombre': 'Caja Los Heroes',
                'cc_codigo': '05',
            }, {
                'cc_nombre': 'La Araucana',
                'cc_codigo': '06',
            }
        ]

        listado_entidades_salud = [
            {
                'sa_nombre': 'Fonasa',
                'sa_codigo': '100',
                'sa_tipo': 'F'
            },
            {
                'sa_nombre': 'Banmédica S.A.',
                'sa_codigo': '99',
                'sa_tipo': 'I'
            },
            {
                'sa_nombre': 'Isalud Ltda.',
                'sa_codigo': '63',
                'sa_tipo': 'I'
            },
            {
                'sa_nombre': 'Colmena Golden Cross S.A.',
                'sa_codigo': '67',
                'sa_tipo': 'I'
            },
            {
                'sa_nombre': 'Consalud S.A.',
                'sa_codigo': '107',
                'sa_tipo': 'I'
            },
            {
                'sa_nombre': 'Cruz Blanca S.A.',
                'sa_codigo': '78',
                'sa_tipo': 'I'
            },
            {
                'sa_nombre': 'Cruz del Norte Ltda.',
                'sa_codigo': '94',
                'sa_tipo': 'I'
            },
            {
                'sa_nombre': 'Nueva Masvida S.A.',
                'sa_codigo': '81',
                'sa_tipo': 'I'
            },
            {
                'sa_nombre': 'Fundación Ltda.',
                'sa_codigo': '76',
                'sa_tipo': 'I'
            },
            {
                'sa_nombre': 'Esencial S.A.',
                'sa_codigo': '108',
                'sa_tipo': 'I'
            }
        ]
        
        listado_prevision = [
            {
                'afp_codigoprevired': '33',
                'afp_nombre': 'Capital',
                'afp_tasatrabajadordependiente': 11.44,
                'afp_sis': 1.55,
                'afp_tasatrabajadorindependiente': 12.99
            },
            {
                'afp_codigoprevired': '03',
                'afp_nombre': 'Cuprum',
                'afp_tasatrabajadordependiente': 11.44,
                'afp_sis': 1.55,
                'afp_tasatrabajadorindependiente': 12.99
            },
            {
                'afp_codigoprevired': '05',
                'afp_nombre': 'Habitat',
                'afp_tasatrabajadordependiente': 11.27,
                'afp_sis': 1.55,
                'afp_tasatrabajadorindependiente': 12.82
            },
            {
                'afp_codigoprevired': '29',
                'afp_nombre': 'PlanVital',
                'afp_tasatrabajadordependiente': 11.16,
                'afp_sis': 1.55,
                'afp_tasatrabajadorindependiente': 12.71
            },
            {
                'afp_codigoprevired': '08',
                'afp_nombre': 'ProVida',
                'afp_tasatrabajadordependiente': 11.45,
                'afp_sis': 1.55,
                'afp_tasatrabajadorindependiente': 13.00
            },
            {
                'afp_codigoprevired': '34',
                'afp_nombre': 'Modelo',
                'afp_tasatrabajadordependiente': 10.58,
                'afp_sis': 1.55,
                'afp_tasatrabajadorindependiente': 12.13
            },
            {
                'afp_codigoprevired': '35',
                'afp_nombre': 'Uno',
                'afp_tasatrabajadordependiente': 10.69,
                'afp_sis': 1.55,
                'afp_tasatrabajadorindependiente': 12.24
            }
        ]
        
        for base in lista:
            nombre_bd = base.nombre_bd
            print(f" ********** Cargando datos para {nombre_bd} ********** ")

            for value in listado_tipo_contratos:
                tc = TipoContrato.objects.using(nombre_bd).filter(tc_codcontrato=value['tc_codcontrato'])
                if not tc.exists():
                    tipc = TipoContrato()
                    tipc.tc_codcontrato = value['tc_codcontrato']
                    tipc.tc_nombrecontrato = value['tc_nombrecontrato']
                    tipc.save(using=nombre_bd)
                else:
                    tc_codcontrato = value['tc_codcontrato']
                    print(f"Contrato para {tc_codcontrato} ya existe")

            for value in listado_bancos:
                b = Banco.objects.using(nombre_bd).filter(ban_codigo=value['ban_codigo'])
                if not b.exists():
                    ban = Banco()
                    ban.ban_nombre = value['ban_nombre']
                    ban.ban_codigo = value['ban_codigo']
                    ban.save(using=nombre_bd)
                else:
                    ban_codigo = value['ban_codigo']
                    print(f"el banco {ban_codigo} ya existe")

            for value in listado_cajas_compensasion:
                c = CajasCompensacion.objects.using(nombre_bd).filter(cc_codigo=value['cc_codigo'])
                if not c.exists():
                    cc = CajasCompensacion()
                    cc.cc_nombre = value['cc_nombre']
                    cc.cc_codigo = value['cc_codigo']
                    cc.save(using=nombre_bd)
                else:
                    cc_codigo = value['cc_codigo']
                    print(f"la caja de compensacion {cc_codigo} ya existe")

            for value in listado_entidades_salud:
                s = Salud.objects.using(nombre_bd).filter(sa_codigo=value['sa_codigo'])
                if not s.exists():
                    sa = Salud()
                    sa.sa_nombre = value['sa_nombre']
                    sa.sa_codigo = value['sa_codigo']
                    sa.sa_tipo = value['sa_tipo']
                    sa.save(using=nombre_bd)
                else:
                    sa_codigo = value['sa_codigo']
                    print(f"la entidad de salud {sa_codigo} ya existe")

            for value in listado_prevision:
                a = Afp.objects.using(nombre_bd).filter(afp_codigoprevired=value['afp_codigoprevired'])
                if not a.exists():
                    afp = Afp()
                    afp.afp_codigoprevired = value['afp_codigoprevired']
                    afp.afp_nombre = value['afp_nombre']
                    afp.afp_tasatrabajadordependiente = value['afp_tasatrabajadordependiente']
                    afp.afp_sis = value['afp_sis']
                    afp.afp_tasatrabajadorindependiente = value['afp_tasatrabajadorindependiente']
                    afp.save(using=nombre_bd)
                else:
                    afp_codigoprevired = value['afp_codigoprevired']
                    print(f"la entidad de AFP {afp_codigoprevired} ya existe")
            print(f" ********** Finalizada la carga para {nombre_bd} **************** ")