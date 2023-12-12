from rest_framework import serializers
from applications.base.models import Comuna
from applications.base.utils import validarRut

from applications.empresa.models import Afp, Cargo, CentroCosto, Sucursal
from applications.usuario.models import Colaborador, UsuarioEmpresa


class CentroSucursalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sucursal
        fields = ('__all__')


class CentroCostosSerializer(serializers.ModelSerializer):
    class Meta:
        model = CentroCosto
        fields = ('__all__')


class CargosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cargo
        fields = ('__all__')


class ComunsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comuna
        fields = ('__all__')


# Afp serializer
class AfpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Afp
        fields = ('__all__')


class LaboralDataPersonalSerializer(serializers.ModelSerializer):

    ue_fechatermino = serializers.DateField(required=False, allow_null=True, input_formats=["%Y-%m-%d"])
    ue_fecharenovacioncontrato = serializers.DateField(required=False, allow_null=True, input_formats=["%Y-%m-%d"])

    def validate(self, value):
        return value.strftime('%Y-%m-%d') if value else value
    
    class Meta:
        model = UsuarioEmpresa
        fields = (
            'cargo',
            'centrocosto',
            'sucursal',
            'ue_fechacontratacion',
            'ue_fecharenovacioncontrato',
            'ue_fechatermino',
            'ue_tipocontrato',
            'ue_tipotrabajdor',
            'ue_estate',
            'ue_workersector',
            'ue_horassemanales',
            'ue_agreedworkdays'
            )


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