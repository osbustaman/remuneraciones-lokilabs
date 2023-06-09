from rest_framework import serializers

from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from rest_framework import serializers

from applications.base.utils import validarRut
from applications.empresa.models import Cargo, CentroCosto, Empresa, GrupoCentroCosto, Sucursal   

class EmpresaSerializers(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = ('__all__')

        def validate(self, data):

            if self.instance:
                raise serializers.ValidationError(f'La empresa ya existe')

            if not validarRut(data['emp_rut']):
                raise serializers.ValidationError(f'El rut de la empresa no es valido')

            if not validarRut(data['emp_rutrepresentante']):
                raise serializers.ValidationError(f'El rut del representante de la empresa no es valido')

            try:
                validate_email(data['emp_mailuno'])
            except ValidationError:
                raise serializers.ValidationError("El el formato de correo 1 no es válido")

            try:
                validate_email(data['emp_maildos'])
            except ValidationError:
                raise serializers.ValidationError("El el formato de correo 2 no es válido")

            return data

class EmpresaActivaSerializer(serializers.Serializer):
    empresa_activa = serializers.CharField(max_length=50)

class SucursalSerializers(serializers.ModelSerializer):
    class Meta:
        model = Sucursal
        fields = ('__all__')

class SucursalActivaSerializer(serializers.Serializer):
    sucursal_activa = serializers.CharField(max_length=50)

class CargoSerializers(serializers.ModelSerializer):
    class Meta:
        model = Cargo
        fields = ('__all__')

class CargoActivaSerializer(serializers.Serializer):
    car_activa = serializers.CharField(max_length=50)

class GrupoCentroCostoSerializers(serializers.ModelSerializer):
    class Meta:
        model = GrupoCentroCosto
        fields = ('__all__')

class GrupoCentroCostoActivaSerializer(serializers.Serializer):
    gcencost_activo = serializers.CharField(max_length=50)

class CentroCostoSerializers(serializers.ModelSerializer):
    class Meta:
        model = CentroCosto
        fields = ('__all__')

class CentroCostoActivaSerializer(serializers.Serializer):
    cencost_activo = serializers.CharField(max_length=50)

class CargaMasivaConfiguracionEmpresaSerializer(serializers.Serializer):
    excel_carga_masiva = serializers.CharField(max_length=None)

class CargaLogoEmpresaSerializer(serializers.Serializer):
    logo_empresa = serializers.CharField(max_length=None)