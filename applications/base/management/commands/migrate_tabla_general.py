# -*- encoding: utf-8 -*-
from django.core.management.base import BaseCommand
from app01.functions import load_data_base
from applications.base.models import Cliente, TablaGeneral

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

        # causas legales de terminación de contrato
        causas_finiquito = [
            {
                'tg_nombretabla': 'tb_causas_legales_finiquito',
                'tg_idelemento': '1',
                'tg_descripcion': '(artículo 159) Mutuo acuerdo de las partes.'
            },
            {
                'tg_nombretabla': 'tb_causas_legales_finiquito',
                'tg_idelemento': '2',
                'tg_descripcion': '(artículo 159) Renuncia del trabajador, dando aviso a su empleador con treinta días de anticipación, a lo menos.'
            },
            {
                'tg_nombretabla': 'tb_causas_legales_finiquito',
                'tg_idelemento': '3',
                'tg_descripcion': '(artículo 159) Muerte del trabajador.'
            },
            {
                'tg_nombretabla': 'tb_causas_legales_finiquito',
                'tg_idelemento': '4',
                'tg_descripcion': '(artículo 159) Vencimiento del plazo convenido en el contrato.'
            },
            {
                'tg_nombretabla': 'tb_causas_legales_finiquito',
                'tg_idelemento': '5',
                'tg_descripcion': '(artículo 159) Conclusión del trabajo o servicio que dio origen al contrato.'
            },
            {
                'tg_nombretabla': 'tb_causas_legales_finiquito',
                'tg_idelemento': '6',
                'tg_descripcion': '(artículo 159) Caso fortuito o fuerza mayor, es decir, una situación ajena a las partes, que no es posible de prevenir y que hace imposible realizar el trabajo convenido, como un terremoto, un incendio o una inundación que destruyen el local de la empresa.'
            },


            {
                'tg_nombretabla': 'tb_causas_legales_finiquito',
                'tg_idelemento': '7',
                'tg_descripcion': '(artículo 160) Alguna de las conductas indebidas de carácter grave, debidamente comprobadas,'+
                                    'que a continuación se señalan:'+
                                    'a) Falta de probidad del trabajador en el desempeño de sus funciones;'+
                                    'b) Conductas de acoso sexual;'+
                                    'c) Vías de hecho ejercidas por el trabajador en contra del empleador o de cualquier trabajador que se desempeñe en la misma empresa;'+
                                    'd) Injurias proferidas por el trabajador al empleador, y'+
                                    'e) Conducta inmoral del trabajador que afecte a la empresa donde se desempeña.'+
                                    'f) Conductas de acoso laboral.'
            },
            {
                'tg_nombretabla': 'tb_causas_legales_finiquito',
                'tg_idelemento': '8',
                'tg_descripcion': '(artículo 160) egociaciones que ejecute el trabajador dentro del giro del negocio y que hubieren sido prohibidas por escrito en el respectivo contrato por el empleador.'
            },
            {
                'tg_nombretabla': 'tb_causas_legales_finiquito',
                'tg_idelemento': '9',
                'tg_descripcion': '(artículo 160) No concurrencia del trabajador a sus labores sin causa justificada durante dos días seguidos, dos lunes en el mes o un total de tres días durante igual período de tiempo; asimismo, la falta injustificada, o sin aviso previo de parte del trabajador que tuviere a su cargo una actividad, faena o máquina cuyo abandono o paralización signifique una perturbación grave en la marcha de la obra.'
            },
            {
                'tg_nombretabla': 'tb_causas_legales_finiquito',
                'tg_idelemento': '10',
                'tg_descripcion': '(artículo 160) Abandono del trabajo por parte del trabajador, entendiéndose por tal: a) la salida intempestiva e injustificada del trabajador del sitio de la faena y durante las horas de trabajo, sin permiso del empleador o de quien lo represente, y b) la negativa a trabajar sin causa justificada en las faenas convenidas en el contrato. '
            },
            {
                'tg_nombretabla': 'tb_causas_legales_finiquito',
                'tg_idelemento': '11',
                'tg_descripcion': '(artículo 160) Actos, omisiones o imprudencias temerarias que afecten a la seguridad o al funcionamiento del establecimiento, a la seguridad o a la actividad de los trabajadores, o a la salud de éstos.'
            },
            {
                'tg_nombretabla': 'tb_causas_legales_finiquito',
                'tg_idelemento': '12',
                'tg_descripcion': '(artículo 160) El perjuicio material causado intencionalmente en las instalaciones, maquinarias, herramientas, útiles de trabajo, productos o mercaderías.'
            },
            {
                'tg_nombretabla': 'tb_causas_legales_finiquito',
                'tg_idelemento': '13',
                'tg_descripcion': '(artículo 160) Incumplimiento grave de las obligaciones que impone el contrato.'
            },
            {
                'tg_nombretabla': 'tb_causas_legales_finiquito',
                'tg_idelemento': '14',
                'tg_descripcion': '(artículo 161) El empleador podrá poner término al contrato invocando como causal las necesidades de la empresa, establecimiento o servicio, tales como las derivadas de la racionalización o modernización de los mismos, bajas en la productividad, cambios en las condiciones del mercado o de la economía, que hagan necesaria la separación de uno o más trabajadores. En caso de trabajadores que tengan poder para representar al empleador, tales como gerentes, subgerentes, agentes o apoderados, siempre que, en todos estos casos, estén dotados, a lo menos, de facultades generales de administración, y en el caso de trabajadoras de casa particular, el contrato podrá, además, terminar por desahucio escrito del empleador. Rige también esta norma tratándose de cargos o empleos de la exclusiva confianza del empleador, cuyo carácter de tales emane de la naturaleza de los mismos.'
            },
            {
                'tg_nombretabla': 'tb_causas_legales_finiquito',
                'tg_idelemento': '15',
                'tg_descripcion': '(Causal del artículo 163 bis) La que se configura por haber sido sometido el empleador, mediante resolución judicial, a un procedimiento concursal de liquidación de sus bienes. Su invocación corresponde efectuarla al liquidador designado en dicho procedimiento. Esta causal opera aún cuando se apruebe la continuación de las actividades económicas del deudor, caso en el cual el liquidador deberá celebrar los nuevos contratos de trabajo que estime necesarios para llevar adelante tal continuación.'
            },
        ]

        for base in lista:
            nombre_bd = base.nombre_bd
            print(f" ********** Cargando datos para {nombre_bd} ********** ")

            for value in causas_finiquito:
                tg = TablaGeneral.objects.using(nombre_bd).filter(tg_nombretabla=value['tg_nombretabla'], tg_idelemento=value['tg_idelemento'])
                if not tg.exists():
                    tbg = TablaGeneral()
                    tbg.tg_nombretabla = value['tg_nombretabla']
                    tbg.tg_idelemento = value['tg_idelemento']
                    tbg.tg_descripcion = value['tg_descripcion']
                    tbg.save(using=nombre_bd)
                else:
                    tg_nombretabla = value['tg_nombretabla']
                    tg_idelemento = value['tg_idelemento']
                    print(f"El elemento {tg_nombretabla} - {tg_idelemento} ya existe")

            print(f" ********** Carga de datos para {nombre_bd} terminada********** ")