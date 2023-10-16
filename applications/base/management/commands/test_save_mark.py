# -*- encoding: utf-8 -*-
from django.core.management.base import BaseCommand
from app01.functions import load_data_base
from applications.attendance.api.serializers import MarkAttendanceSerializer
from applications.attendance.models import MarkAttendance
from applications.base.models import Cliente, TablaGeneral
from django.contrib.auth.models import User

from datetime import date, datetime, timedelta
import random

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

        for base in lista:
            nombre_bd = base.nombre_bd

            user = User.objects.get(username='17452821-7')
            latitud = '-33.43476615714285'
            longitud = '-70.68733879999999'
            ma_place = 'oficina principal'
            ma_platformmark = 'oficina principal'
            ma_typemark = 3

            # Obtén la fecha actual y retrocede tres meses
            today = datetime.now() - timedelta(days=90)
            end_date = today + timedelta(days=30)

            while today < end_date:

                print(f' **** MARCAS DE ENTRADA Y SALIDA: {today.replace(hour=8, minute=30).strftime("%Y-%m-%d %H:%M")} == {today.replace(hour=17, minute=30).strftime("%Y-%m-%d %H:%M:%S")} **** ')

                # _mark_data_1 = {
                #     'user': user.id,
                #     'ma_typeattendance': 1,
                #     'ma_latitude': latitud,
                #     'ma_longitude': longitud,
                #     'ma_datemark': today.replace(hour=8, minute=30).strftime("%Y-%m-%d %H:%M:%S"),
                # }

                mark_data_1 = MarkAttendance()
                user = user
                mark_data_1.ma_typeattendance = 1
                mark_data_1.ma_latitude = latitud
                mark_data_1.ma_longitude = longitud
                mark_data_1.ma_datemark = today.replace(hour=8, minute=self.generate_random_integer()).strftime("%Y-%m-%d %H:%M")
                mark_data_1.save(using=nombre_bd)


                # _mark_data_2 = {
                #     'user': user.id,
                #     'ma_typeattendance': 1,
                #     'ma_latitude': latitud,
                #     'ma_longitude': longitud,
                #     'ma_datemark': today.replace(hour=8, minute=30).strftime("%Y-%m-%d %H:%M:%S"),
                # }

                mark_data_2 = MarkAttendance()
                user = user
                mark_data_2.ma_typeattendance = 1
                mark_data_2.ma_latitude = latitud
                mark_data_2.ma_longitude = longitud
                mark_data_2.ma_datemark = today.replace(hour=17, minute=self.generate_random_integer()).strftime("%Y-%m-%d %H:%M")
                mark_data_2.save(using=nombre_bd)

                today += timedelta(days=1)
            
            # Verificar que las marcas de asistencia se hayan guardado correctamente
            # self.assertEqual(MarkAttendance.objects.filter(user=self.user).count(), 60)  # 30 días * 2 marcas por día

    def generate_random_integer(self):
        # Genera un número entero aleatorio entre 0 y 59
        random_integer = random.randint(0, 59)
        return random_integer