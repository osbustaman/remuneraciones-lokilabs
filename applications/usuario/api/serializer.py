from rest_framework import serializers
from applications.base.utils import validarRut

from applications.empresa.models import Afp
from applications.usuario.models import Colaborador

# Afp serializer
class AfpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Afp
        fields = ('__all__')


# 
class PersonalDataSerializer(serializers.ModelSerializer):

    col_rut = serializers.CharField(max_length=10)

    def validate_col_rut(self, value):
        if not validarRut(value):
            raise serializers.ValidationError("El RUT no es válido")
        return value
    
    class Meta:
        model = Colaborador
        fields = (
            'col_rut'
            , 'col_extranjero'
            , 'col_nacionalidad'
            , 'col_sexo'
            , 'col_fechanacimiento'
            , 'col_estadocivil'
            , 'col_direccion'
            , 'pais'
            , 'region'
            , 'comuna'
            , 'col_estudios'
            , 'col_estadoestudios'
            , 'col_titulo'
            , 'col_licenciaconducir'
            , 'col_tipolicencia'
            , 'col_tipousuario'
            )