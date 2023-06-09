from django.core.management.base import BaseCommand
from applications.base.models import Comuna, Pais, Region

class Command(BaseCommand):
    help = 'Se inicia la carga de datos para el administrador de clientes'

    def handle(self, *args, **options):

        listado_regiones = Region.objects.all()
        archi1=open("datos.sql","w") 
        for region in listado_regiones:
            # print(f'INSERT INTO `gp_region` (`pais_id`,`nombre_region`) VALUES (1, \'{region.re_nombre}\');')
            # archi1.write(f'INSERT INTO `gp_region` (`pais_id`,`nombre_region`) VALUES (1, \'{region.re_nombre}\');\n')
            listado_comunas = Comuna.objects.filter(region=region)
            for comuna in listado_comunas:
                #print(f'INSERT INTO `gp_comuna` (`region_id`,`nombre_comuna`) VALUES ({region.re_id}, \'{comuna.com_nombre}\');')
                
                archi1.write(f'INSERT INTO `gp_comuna` (`region_id`,`nombre_comuna`) VALUES ({region.re_id}, \'{comuna.com_nombre}\');\n')
        archi1.close()

        