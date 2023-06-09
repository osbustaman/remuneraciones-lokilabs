from rest_framework import serializers
from django.contrib.auth.models import User
from applications.base.models import Cliente

from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password

from applications.base.utils import getCliente, validarRut   

class AddClienteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ('__all__')

class ClienteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ('__all__')
    
    def validate(self, data):

        if not validarRut(data['rut_cliente']):
            raise serializers.ValidationError(f'El rut del cliente es invalido')

        if not validarRut(data['rut_representante']):
            raise serializers.ValidationError(f'El rut del representante es invalido')

        if getCliente(data) and not self.instance:
            raise serializers.ValidationError(f'El cliente ya existe')

        try:
            validate_email(data['correo_representante'])
        except ValidationError:
            raise serializers.ValidationError("El correo electrónico no es válido")

        return data

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        try:
            validate_email(data['email'])
        except ValidationError:
            raise serializers.ValidationError("El correo electrónico no es válido")

        return data

    def create(self, validated_data):
        # Hashea la contraseña antes de crear el usuario
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)