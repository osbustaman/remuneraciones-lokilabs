import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from applications.empresa.models import Cargo, CentroCosto, Empresa, Sucursal
from applications.usuario.models import Colaborador, Pais, Region, Comuna, Rol, Banco, UsuarioEmpresa
from app01.functions import load_data_base
from applications.base.models import Cliente

from faker import Faker

fake = Faker()

class Command(BaseCommand):
    help = 'Crea datos de prueba simulados para Colaborador'


    def generar_rut_chileno(self):
        # Generar un número base aleatorio de 8 dígitos
        numero_base = random.randint(16000000, 29999999)

        # Calcular el dígito verificador usando el algoritmo de módulo 11
        digito_verificador = self.calcular_digito_verificador(numero_base)

        # Formatear el RUT con guion y devolverlo como cadena
        rut_generado = f"{numero_base}-{digito_verificador}"
        
        return rut_generado
    
    def calcular_digito_verificador(self, numero_base):
        # Convertir el número base a cadena y revertirlo
        reversed_numero_base = str(numero_base)[::-1]

        # Inicializar variables para el cálculo
        suma = 0
        multiplicador = 2

        # Calcular la suma ponderada de los dígitos
        for digito in reversed_numero_base:
            suma += int(digito) * multiplicador
            multiplicador += 1
            if multiplicador > 7:
                multiplicador = 2

        # Calcular el dígito verificador como el complemento a 11 de la suma
        digito_verificador = 11 - (suma % 11)

        # Manejar casos especiales para dígitos verificadores 10 y 11
        if digito_verificador == 10:
            return 'K'
        elif digito_verificador == 11:
            return '0'
        else:
            return str(digito_verificador)
        
    def generate_random_coordinates(self, base_latitude, base_longitude, radius=0.01):
        """
        Genera latitudes y longitudes aleatorias alrededor de una ubicación dada.

        Parameters:
            base_latitude (float): Latitud base.
            base_longitude (float): Longitud base.
            radius (float): Radio de variación. Por defecto, 0.01 grados.

        Returns:
            tuple: Tupla de latitud y longitud generadas aleatoriamente.
        """
        # Genera variaciones aleatorias dentro del radio especificado
        delta_latitude = random.uniform(-radius, radius)
        delta_longitude = random.uniform(-radius, radius)

        # Aplica las variaciones a las coordenadas base
        new_latitude = base_latitude + delta_latitude
        new_longitude = base_longitude + delta_longitude

        return new_latitude, new_longitude
        

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Creando datos de prueba...'))

        load_data_base()

        lista = Cliente.objects.all()

        for base in lista:
            nombre_bd = base.nombre_bd

            # Crea usuarios de Django
            for _ in range(10):
                username = self.generar_rut_chileno()
                last_name, first_name = (fake.name()).split(" ")
                email = fake.email()
                password = self.generar_rut_chileno()

                user = User()
                user.username = username
                user.first_name = first_name
                user.last_name = last_name
                user.email = email
                user.set_password(password)
                user.is_staff = True
                user.is_superuser = False
                user.save(using=nombre_bd)

                random_latitude, random_longitude = self.generate_random_coordinates(-33.427559271238664, -70.67932418948963)

                colaborador = Colaborador()
                colaborador.user = user
                colaborador.col_extranjero = random.choice([0, 1])
                colaborador.col_nacionalidad = "chileno"
                colaborador.col_rut = username
                colaborador.col_sexo = random.choice(['M', 'F'])
                colaborador.col_fechanacimiento = fake.date_of_birth(minimum_age=18, maximum_age=65)
                colaborador.col_estadocivil = random.choice([1, 2, 3, 4])
                colaborador.col_direccion = fake.address()
                colaborador.pais = Pais.objects.using(nombre_bd).order_by('?').first()
                colaborador.region = Region.objects.using(nombre_bd).order_by('?').first()
                colaborador.comuna = Comuna.objects.using(nombre_bd).order_by('?').first()
                colaborador.col_latitude = random_latitude
                colaborador.col_longitude = random_longitude
                colaborador.col_tipousuario = Rol.objects.using(nombre_bd).order_by('?').first()
                colaborador.col_estudios = random.choice([1, 2, 3])
                colaborador.col_estadoestudios = random.choice([1, 2])
                colaborador.col_titulo = fake.job()
                colaborador.col_formapago = random.choice([1, 2, 3, 4])
                colaborador.banco = Banco.objects.using(nombre_bd).order_by('?').first()
                colaborador.col_tipocuenta = random.choice([0, 1, 2, 3, 4, 5, 6, 7])
                colaborador.col_cuentabancaria = fake.unique.random_number(digits=10)
                colaborador.col_usuarioactivo = random.choice([0, 1])
                colaborador.col_licenciaconducir = random.choice([0, 1])
                colaborador.col_tipolicencia = fake.random_element(elements=('A', 'B', 'C'))
                colaborador.col_fotousuario = fake.image_url()
                colaborador.col_activo = random.choice([0, 1])

                colaborador.save(using=nombre_bd)

                usuario_empresa = UsuarioEmpresa()
                usuario_empresa.user = user
                usuario_empresa.empresa = Empresa.objects.using(nombre_bd).order_by('?').first()
                usuario_empresa.cargo = Cargo.objects.using(nombre_bd).order_by('?').first()
                usuario_empresa.centrocosto = CentroCosto.objects.using(nombre_bd).order_by('?').first()
                usuario_empresa.sucursal = Sucursal.objects.using(nombre_bd).order_by('?').first()
                usuario_empresa.ue_fechacontratacion = fake.date_this_decade(before_today=True, after_today=False)
                usuario_empresa.ue_fecharenovacioncontrato = fake.date_this_decade(before_today=True, after_today=False)

                usuario_empresa.save(using=nombre_bd)


                print(f"{username}...{last_name}...{first_name}...{email}...{password}...save OK!!")
            else:
                print(f"{username}...{last_name}...{first_name}...{email}...{password}...save ERROR!!")
            self.stdout.write(self.style.SUCCESS(f'Datos de prueba para el cliente {nombre_bd} creados con éxito.'))
