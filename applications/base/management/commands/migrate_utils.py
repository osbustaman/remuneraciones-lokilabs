# -*- encoding: utf-8 -*-
from django.core.management.base import BaseCommand
from app01.functions import load_data_base

from applications.base.models import Cliente
from applications.empresa.models import Afp, Banco, TipoContrato, CajasCompensacion, Salud
from applications.remuneracion.models import Concept
from applications.security.models import Rol

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

        listado_roles = [
            {
                'rol_name': 'Super-Admin',
                'rol_nivel': 8,
                'rol_client': 'N',
            }, {
                'rol_name': 'Recursos Humanos',
                'rol_nivel': 2,
                'rol_client': 'Y',
            }, {
                'rol_name': 'Recursos Humanos Adm',
                'rol_nivel': 1,
                'rol_client': 'Y',
            }, {
                'rol_name': 'Jefatura',
                'rol_nivel': 3,
                'rol_client': 'Y',
            }, {
                'rol_name': 'Colaborador',
                'rol_nivel': 4,
                'rol_client': 'Y',
            }
        ]
        
        listado_conceptos_default = [
            {
                'conc_name': 'Sueldo Base',
                'conc_clasificationconcept': 1,
                'conc_typeconcept': 1,
                'conc_remuneration_type': 1,
                'conc_search_field': ''
            }, {
                'conc_name': 'Sobresueldo (Horas Extras)',
                'conc_clasificationconcept': 1,
                'conc_typeconcept': 1,
                'conc_remuneration_type': 2,
                'conc_search_field': ''
            }, {
                'conc_name': 'Recargo por Domingo',
                'conc_clasificationconcept': 1,
                'conc_typeconcept': 1,
                'conc_remuneration_type': 3,
                'conc_search_field': ''
            }, {
                'conc_name': 'Comisión',
                'conc_clasificationconcept': 1,
                'conc_typeconcept': 1,
                'conc_remuneration_type': 3,
                'conc_search_field': ''
            }, {
                'conc_name': 'Tratos',
                'conc_clasificationconcept': 1,
                'conc_typeconcept': 1,
                'conc_remuneration_type': 3,
                'conc_search_field': ''
            }, {
                'conc_name': 'Semana Corrida',
                'conc_clasificationconcept': 1,
                'conc_typeconcept': 1,
                'conc_remuneration_type': 3,
                'conc_search_field': ''
            }, {
                'conc_name': 'Bonos',
                'conc_clasificationconcept': 1,
                'conc_typeconcept': 1,
                'conc_remuneration_type': 4,
                'conc_search_field': ''
            }, {
                'conc_name': 'Participación',
                'conc_clasificationconcept': 1,
                'conc_typeconcept': 1,
                'conc_remuneration_type': 4,
                'conc_search_field': ''
            }, {
                'conc_name': 'Gratificación Mensual',
                'conc_clasificationconcept': 1,
                'conc_typeconcept': 1,
                'conc_remuneration_type': 5,
                'conc_search_field': ''
            }, {
                'conc_name': 'Gratificación Anual',
                'conc_clasificationconcept': 1,
                'conc_typeconcept': 1,
                'conc_remuneration_type': 5,
                'conc_search_field': ''
            }, {
                'conc_name': 'Asignación de Movilización',
                'conc_clasificationconcept': 1,
                'conc_typeconcept': 2,
                'conc_remuneration_type': 0,
                'conc_search_field': ''
            }, {
                'conc_name': 'Asignación de Colación',
                'conc_clasificationconcept': 1,
                'conc_typeconcept': 2,
                'conc_remuneration_type': 0,
                'conc_search_field': ''
            }, {
                'conc_name': 'Asignación Familiar',
                'conc_clasificationconcept': 1,
                'conc_typeconcept': 2,
                'conc_remuneration_type': 0,
                'conc_search_field': ''
            }, {
                'conc_name': 'Diferencia ISAPRE',
                'conc_clasificationconcept': 2,
                'conc_typeconcept': 1,
                'conc_remuneration_type': 6,
                'conc_search_field': 'ISAPRE'
            }, {
                'conc_name': 'Descuento Isapre',
                'conc_clasificationconcept': 2,
                'conc_typeconcept': 1,
                'conc_remuneration_type': 6,
                'conc_search_field': 'ISAPRE'
            }, {
                'conc_name': 'Descuento Fonasa',
                'conc_clasificationconcept': 2,
                'conc_typeconcept': 1,
                'conc_remuneration_type': 6,
                'conc_search_field': 'FONASA'
            }, {
                'conc_name': 'Descuento AFP',
                'conc_clasificationconcept': 2,
                'conc_typeconcept': 1,
                'conc_remuneration_type': 6,
                'conc_search_field': 'AFP'
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

            for value in listado_roles:
                r = Rol()
                r.rol_name = value['rol_name']
                r.rol_nivel = value['rol_nivel']
                r.rol_client = value['rol_client']
                r.save(using=nombre_bd)


            for value in listado_conceptos_default:
                c = Concept()
                c.conc_name = value['conc_name']
                c.conc_clasificationconcept = value['conc_clasificationconcept']
                c.conc_typeconcept = value['conc_typeconcept']
                c.conc_search_field = value['conc_search_field']
                c.conc_remuneration_type = value['conc_remuneration_type']
                c.conc_default = 'S'
                c.save(using=nombre_bd)

            print(f" ********** Finalizada la carga para {nombre_bd} **************** ")