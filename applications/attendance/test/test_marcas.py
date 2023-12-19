from django.test import TestCase
from django.contrib.auth.models import User
from datetime import date, datetime, timedelta

from applications.attendance.api.serializers import MarkAttendanceSerializer
from applications.attendance.models import MarkAttendance


class MarkAttendanceTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='19306862-6')
        self.latitud = '-33.43476615714285'
        self.longitud = '-70.68733879999999'
        self.ma_place = 'oficina principal'
        self.ma_platformmark = 'oficina principal'
        self.ma_typemark = 3

    def test_save_monthly_data(self):
        # Configuración de fechas
        today = datetime.now()
        end_date = today + timedelta(days=30)

        while today < end_date:

            print(f' **** MARCAS DE ENTRADA Y SALIDA: {today.replace(hour=8, minute=30).strftime("%Y-%m-%d %H:%M:%S")} == {today.replace(hour=17, minute=30).strftime("%Y-%m-%d %H:%M:%S")} **** ')

            mark_data_1 = {
                'user': self.user.id,
                'ma_typeattendance': 1,
                'ma_latitude': self.latitud,
                'ma_longitude': self.longitud,
                'ma_datemark': today.replace(hour=8, minute=30).strftime("%Y-%m-%d %H:%M:%S"),
            }

            serializer_1 = MarkAttendanceSerializer(data=mark_data_1)
            if not serializer_1.is_valid():
                print(f"Errores en serializer_1: {serializer_1.errors}")

            self.assertTrue(serializer_1.is_valid())
            serializer_1.save()


            mark_data_2 = {
                'user': self.user.id,
                'ma_typeattendance': 1,
                'ma_latitude': self.latitud,
                'ma_longitude': self.longitud,
                'ma_datemark': today.replace(hour=17, minute=30).strftime("%Y-%m-%d %H:%M:%S"),
            }

            serializer_1 = MarkAttendanceSerializer(data=mark_data_2)
            if not serializer_1.is_valid():
                print(f"Errores en mark_data_2: {serializer_1.errors}")

            self.assertTrue(serializer_1.is_valid())
            serializer_1.save()

            today += timedelta(days=1)
            
        # Verificar que las marcas de asistencia se hayan guardado correctamente
        self.assertEqual(MarkAttendance.objects.filter(user=self.user).count(), 60)  # 30 días * 2 marcas por día