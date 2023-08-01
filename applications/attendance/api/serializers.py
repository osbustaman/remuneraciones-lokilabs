
from rest_framework import serializers

from applications.attendance.models import MarkAttendance

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    pass

# User serializer
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

class MarkAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarkAttendance
        fields = '__all__'