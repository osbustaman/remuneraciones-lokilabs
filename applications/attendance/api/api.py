

from applications.attendance.api.serializers import MarkAttendanceSerializer
from applications.attendance.models import MarkAttendance

from datetime import datetime
from django.db.models import F, Count
from django.utils import timezone

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework import status
from rest_framework import generics, status
from rest_framework.response import Response

from django.contrib.auth.models import User

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
                'ma_location': openapi.Schema(type='string', description='Localización (dirección, comuna, region, país)'),
                'ma_datemark': openapi.Schema(type='string', format='date', description='Fecha'),
            },
            required=['user', 'ma_typeattendance', 'ma_location', 'ma_datemark'],
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
        if serializer.is_valid():
            objectUser = User.objects.filter(id = request.data['user'])

            if objectUser.exists():
                # Obtener la fecha y hora actual en el formato de la base de datos
                actualDate = datetime.strptime(request.data['ma_datemark'], "%Y-%m-%d").date()
                objectMarkAttendance = MarkAttendance.objects.filter(user=objectUser.first(), ma_datemark=actualDate)
                
                if objectMarkAttendance:
                    if len(objectMarkAttendance) >= 2:
                        return Response({"error": "No Content - 204", "message": f"ya existen marcas de ENTRADA y SALIDA para el dia { request.data['ma_datemark'] }"}, status=status.HTTP_204_NO_CONTENT)
                    else:
                        for mark in objectMarkAttendance:
                            if mark.ma_typeattendance == int(request.data['ma_typeattendance']):
                                return Response({"error": "No Content - 204", "message": f"ya existe una marca de { mark.get_ma_typeattendance_display() }"}, status=status.HTTP_204_NO_CONTENT)
                            else:
                                serializer.save()
                                response_to_page = {
                                    "data_serializer": serializer.data
                                }
                                return Response(response_to_page, status=status.HTTP_201_CREATED)
                else:
                    if not objectMarkAttendance and int(request.data['ma_typeattendance']) == 2:
                        return Response({"error": "No Content - 204", "message": f"para marcar la SALIDA debe existir una ENTRADA"}, status=status.HTTP_204_NO_CONTENT)
                    else:
                        serializer.save()
                        response_to_page = {
                            "data_serializer": serializer.data
                        }
                        return Response(response_to_page, status=status.HTTP_201_CREATED)
            else:
                return Response({"error": "Not Found - 404", "message": "Usuario no existe"}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
