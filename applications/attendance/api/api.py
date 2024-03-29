import pytz

from applications.attendance.api.serializers import MarkAttendanceSerializer, UsuarioEmpresaSerializer
from applications.attendance.models import MarkAttendance
from applications.base.models import TablaGeneral
from applications.usuario.models import Colaborador, UsuarioEmpresa

from datetime import datetime, timedelta
from decouple import config

from django.contrib.auth.models import User
from django.db.models import F, Count, Q, Value, CharField,  Min, Max
from django.db.models.functions import Concat, TruncDate
from django.utils import timezone
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
from itertools import chain

from requests import Response
from rest_framework import generics, status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

# Define el objeto Parameter para el encabezado Authorization
header_param = openapi.Parameter(
    name="Authorization",
    in_=openapi.IN_HEADER,
    type=openapi.TYPE_STRING,
    description="Token Bearer",
) 

error_401_response = openapi.Response(
    description='Error: Unauthorized - 401',
    schema=openapi.Schema(
        type='object',
        properties={
            'detail': openapi.Schema(type='string', description="Las credenciales de autenticación no se proveyeron."),
        }
    ),
)

@permission_classes([AllowAny])
class MarkInAndOutUserAPIView(generics.ListAPIView):
    serializer_class = MarkAttendanceSerializer
    queryset = MarkAttendance.objects.all()

    def get(self, request, *args, **kwargs):

        objectMarkInAndOutUser = self.queryset.filter(mm_id=self.kwargs['pk'])

        if objectMarkInAndOutUser:
            data = list(objectMarkInAndOutUser.values())
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Not Found - 404"}, status=status.HTTP_404_NOT_FOUND)


@permission_classes([AllowAny])
class GetUsersWorkDay(generics.ListAPIView):
    serializer_class = UsuarioEmpresaSerializer
    queryset = UsuarioEmpresa.objects.all()

    def get(self, request, *args, **kwargs):
        objectListEmpresas = self.queryset.filter(empresa__emp_id=self.kwargs['pk'])
        if objectListEmpresas:
            
            list_empresas = []
            for value in objectListEmpresas:

                list_empresas.append({
                    "user_id": value.user.id,
                    "first_name": value.user.first_name.title(),
                    "last_name": value.user.last_name.title(),
                    "cargo": value.cargo.car_nombre.title()
                })

            return Response(list_empresas, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Not Found - 404"}, status=status.HTTP_404_NOT_FOUND)


@permission_classes([AllowAny])
class ListUsersWorkDay(generics.ListAPIView):
    serializer_class = UsuarioEmpresaSerializer
    queryset = UsuarioEmpresa.objects.all()

    location_timezone = pytz.timezone('America/Santiago')

    def get(self, request, *args, **kwargs):
        objectListEmpresas = self.queryset.filter(empresa__emp_id=self.kwargs['pk'])
        if objectListEmpresas:
            list_empresas = []
            for value in objectListEmpresas:
                
                
                list_empresas.append({
                    "user_id": value.user.id,
                    "first_name": value.user.first_name.title(),
                    "last_name": value.user.last_name.title(),
                    "cargo": value.cargo.car_nombre.title(),
                })

            return Response(list_empresas, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Not Found - 404"}, status=status.HTTP_404_NOT_FOUND)

# @permission_classes([AllowAny])
class MarkInAndOutAPIView(generics.CreateAPIView):
    serializer_class = MarkAttendanceSerializer

    @swagger_auto_schema(
        manual_parameters=[header_param],
        operation_id="Crear Marca",
        operation_description='En esta operación se crea la marca para la entrada y salida',
        request_body=openapi.Schema(
            type='object',
            properties={
                'user': openapi.Schema(type='integer', description='ID del usuario.'),
                'ma_typeattendance': openapi.Schema(type='integer', description='Tipo de marca.'),
                'ma_latitude': openapi.Schema(type='string', description='Latitud ejemplo: -33.419500'),
                'ma_longitude': openapi.Schema(type='string', description='Latitud ejemplo: -70.604875'),

                'ma_modeldevice': openapi.Schema(type='string', description='Iphone 12'),
                'ma_photo': openapi.Schema(type='string', description='String en base64'),
                'ma_typemark': openapi.Schema(type='integer', description='MOVIL|HUELLEREO|WEB'),
                'ma_platformmark': openapi.Schema(type='string', description='navegador de internet en el caso que la marca sea desde la web'),

                'ma_datemark': openapi.Schema(type='string', format='date', description='Fecha formato YYYY-mm-dd'),
            },
            required=['user', 'ma_typeattendance', 'ma_latitude', 'ma_longitude', 'ma_datemark'],
        ),
        responses={
                status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response(
                    description="Error: Internal Server Error",
                    schema=openapi.Schema(
                        type='object',
                        properties={
                            "message": openapi.Schema(type="string", description="Error: Internal Server Error")
                        }
                    )
                ),
                status.HTTP_204_NO_CONTENT: openapi.Response(
                    description="Error: No Content",
                    schema=openapi.Schema(
                        type='object',
                        properties={
                            "error": openapi.Schema(type="string", description="tipo de error"),
                            "message": openapi.Schema(type="string", description="ya existe una marca de ENTRADA|SALIDA"),
                        }
                    )
                ),
                status.HTTP_400_BAD_REQUEST: openapi.Response(
                    description="Error: Error: Bad Request",
                    schema=openapi.Schema(
                        type='object',
                        properties={
                            "campo": openapi.Schema(
                                type="array",
                                items=openapi.Schema(
                                    type="string"
                                ),
                                description="Array de mensajes de error para cada campo.",
                            )
                        }
                    )
                ),
                status.HTTP_401_UNAUTHORIZED: error_401_response,
                status.HTTP_201_CREATED: openapi.Response(
                description="success: marca creada con exito",
                schema=openapi.Schema(
                    type='object',
                    properties={
                        "data_serializer": openapi.Schema(
                            type="object",
                            properties={
                                "ma_id": openapi.Schema(type='integer'),
                                "created": openapi.Schema(type='string', format='date-time'),
                                "modified": openapi.Schema(type='string', format='date-time'),
                                "ma_typeattendance": openapi.Schema(type='integer'),
                                "ma_location": openapi.Schema(type='string'),
                                "ma_datemark": openapi.Schema(type='string', format='date-time'),

                                
                                "ma_active": openapi.Schema(type='integer'),
                                "user": openapi.Schema(type='integer'),
                            }
                        )
                    }
                )
            ),
        },
        security=[{"Bearer": []}]
    )
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data = request.data)

        locationData = []
        if serializer.is_valid():
            objectUser = User.objects.filter(id = request.data['user'])

            if objectUser.exists():
                # Obtener la fecha y hora actual en el formato de la base de datos
                actualDate = datetime.strptime(request.data['ma_datemark'], "%Y-%m-%d").date()
                objectMarkAttendance = MarkAttendance.objects.filter(user=objectUser.first(), ma_datemark=actualDate)
                
                if objectMarkAttendance:

                    colaborador_data = Colaborador.objects.filter(user=objectUser.first()).values('col_latitude', 'col_longitude', 'col_direccion', 'comuna__com_nombre', 'region__re_nombre', 'pais__pa_nombre')
                    usuario_empresa_data = UsuarioEmpresa.objects.filter(user=objectUser.first()).values('sucursal__suc_latitude', 'sucursal__suc_longitude', 'sucursal__suc_direccion', 'sucursal__comuna__com_nombre', 'sucursal__region__re_nombre', 'sucursal__pais__pa_nombre')

                    result_list = list(chain(
                        [{'latitud': item['col_latitude'], 'longitud': item['col_longitude'], 'direccion': f"{item['col_direccion']}, {item['comuna__com_nombre']}, {item['region__re_nombre']}, {item['pais__pa_nombre']}"} for item in colaborador_data],
                        [{'latitud': item['sucursal__suc_latitude'], 'longitud': item['sucursal__suc_longitude'], 'direccion': f"{item['sucursal__suc_direccion']}, {item['sucursal__comuna__com_nombre']}, {item['sucursal__region__re_nombre']}, {item['sucursal__pais__pa_nombre']}"} for item in usuario_empresa_data]
                    ))
                    
                    itsRadio = False
                    locationData = []
                    for val in result_list:
                        itsRadio = self.isWithinTheDiameter(
                            float(val['latitud'])
                            , float(val['longitud'])
                            , float(request.data['ma_latitude'])
                            , float(request.data['ma_longitude']))
                        if not itsRadio:
                            break
                        elif itsRadio:
                            locationData.append(
                                {
                                    "lugar": "sucursal",
                                    "latitud": float(val['latitud']),
                                    "longitud": float(val['longitud']),
                                    "direccion": val['direccion']
                                }
                            )
                            break
                        
                    if not itsRadio:
                        return Response({"message": "No se encuantra en el rango del lugar de trabajo"}, status=status.HTTP_404_NOT_FOUND)
                    
                    locationData.append(
                        {
                            "lugar": "posicion",
                            "latitud": float(request.data['ma_latitude']),
                            "longitud": float(request.data['ma_longitude'])
                        }
                    )

                    if len(objectMarkAttendance) >= 2:
                        return Response({"message": f"ya existen marcas de ENTRADA y SALIDA para el dia { request.data['ma_datemark'] }"}, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        for mark in objectMarkAttendance:
                            if mark.ma_typeattendance == int(request.data['ma_typeattendance']):
                                return Response({"message": f"ya existe una marca de { mark.get_ma_typeattendance_display() }"}, status=status.HTTP_400_BAD_REQUEST)
                            else:
                                serializer.save()
                                response_to_page = {
                                    "data_serializer": serializer.data,
                                    "locationData": locationData
                                }
                                return Response(response_to_page, status=status.HTTP_201_CREATED)
                else:
                    if not objectMarkAttendance and int(request.data['ma_typeattendance']) == 2:
                        return Response({"message": f"para marcar la SALIDA debe existir una ENTRADA"}, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        serializer.save()
                        response_to_page = {
                            "data_serializer": serializer.data,
                            "locationData": locationData
                        }
                        return Response(response_to_page, status=status.HTTP_201_CREATED)
            else:
                return Response({"error": "Not Found - 404", "message": "Usuario no existe"}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def getLatitudeLongitude(self, address):
        # Crear un objeto geolocator utilizando el proveedor Nominatim
        geolocator = Nominatim(user_agent="Nominatim")

        # Obtener la ubicación (latitud, longitud) a partir de la dirección
        location = geolocator.geocode(address)

        if location:
            latitude = location.latitude
            longitude = location.longitude
            return latitude, longitude
        else:
            return None, None
        
    def isWithinTheDiameter(self, lat_a, lon_a, lat_b, lon_b, radio_km = 0.1):
        # Crear objetos de ubicación para A y B
        location_a = (lat_a, lon_a)
        location_b = (lat_b, lon_b)

        # Calcular la distancia entre las ubicaciones A y B en kilómetros
        distance_km = geodesic(location_a, location_b).kilometers

        # Verificar si la distancia es menor o igual al radio deseado
        return distance_km <= radio_km
