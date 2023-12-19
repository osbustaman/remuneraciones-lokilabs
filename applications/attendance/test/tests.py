from django.test import TestCase
from django.contrib.auth.models import User
from datetime import date

from applications.attendance.api.serializers import MarkAttendanceSerializer
from applications.attendance.models import MarkAttendance


class MarkAttendanceTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='19306862-6')
        self.today = date.today()

    def test_mark_attendance_creation(self):
        mark_data = {
            'user': self.user.id,
            'ma_typeattendance': 1,
            'ma_latitude': '37.7749',
            'ma_longitude': '-122.4194',
            'ma_datemark': str(self.today),
        }

        serializer = MarkAttendanceSerializer(data=mark_data)
        self.assertTrue(serializer.is_valid())

        serializer.save()

        mark_attendance = MarkAttendance.objects.get(user=self.user, ma_datemark=self.today)
        self.assertEqual(mark_attendance.ma_typeattendance, 1)
        self.assertEqual(mark_attendance.ma_latitude, '37.7749')