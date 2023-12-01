from applications.account_base.api.serializers import (
    CustomTokenObtainPairSerializer
    , CustomUserSerializer
)

from django.contrib.auth import authenticate

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework import status
from rest_framework import generics, status
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from django.contrib.auth.models import User

# Define el objeto Parameter para el encabezado Authorization
header_param = openapi.Parameter(
    name="Authorization",
    in_=openapi.IN_HEADER,
    type=openapi.TYPE_STRING,
    description="Token Bearer",
)

class Login(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    @swagger_auto_schema(
        operation_id="Login Usuario",
        operation_description='Login de usuario',
        request_body=openapi.Schema(
            type='object',
            properties={
                'username': openapi.Schema(type='string', description='Nombre de usuario.'),
                'password': openapi.Schema(type='string', description='Password de usuario.'),
            },
            required=['username', 'password'],
        ),
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="Inicio de sesion exitosa",
                schema=openapi.Schema(
                    type='object',
                    properties={
                        "token": openapi.Schema(type='string'),
                        "refresh-token": openapi.Schema(type='string'),
                        "user": openapi.Schema(
                            type='object',
                            properties={
                                "username": openapi.Schema(type='string'),
                                "email": openapi.Schema(type='string'),
                                "first_name": openapi.Schema(type='string'),
                                "last_name": openapi.Schema(type='string'),
                            }
                        ),
                        "message": openapi.Schema(type='string'),
                    }
                )
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                description="Datos enviados incorrectos",
                schema=openapi.Schema(
                    type='object',
                    properties={
                        "error": openapi.Schema(type="string", description="Contraseña o nombre de usuario incorrectos")
                    }
                )
            ),
        }
    )
    def post(self, request, *args, **kwargs):
        username = request.data.get('username', '')
        password = request.data.get('password', '')
        user = authenticate(
            username=username,
            password=password
        )

        if user:
            login_serializer = self.serializer_class(data=request.data)
            if login_serializer.is_valid():
                user_serializer = CustomUserSerializer(user)

                request.session['token'] = login_serializer.validated_data.get('access')
                request.session['refresh'] = login_serializer.validated_data.get('refresh')
                request.session['user'] = user_serializer.data

                return Response({
                    'token': request.session['token'],
                    'refresh-token': request.session['refresh'],
                    'user': request.session['user'],
                    'message': 'Inicio de sesion exitosa'
                }, status=status.HTTP_200_OK)
            return Response({
                'error': 'Contraseña o nombre de usuario incorrectos'
            }, status=status.HTTP_400_BAD_REQUEST)
        return Response({
                'error': 'Contraseña o nombre de usuario incorrectos'
            }, status=status.HTTP_400_BAD_REQUEST)
    

class Logout(generics.GenericAPIView):
    serializer_class = CustomTokenObtainPairSerializer

    @swagger_auto_schema(
        operation_id="Logout Usuario",
        operation_description='Logout de usuario',
        request_body=openapi.Schema(
            type='object',
            properties={
                'id': openapi.Schema(type='integer', description='ID del usuario que desea cerrar sesión.'),
            },
            required=['id'],
        ),
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="Cierre de sesion exitosa",
                schema=openapi.Schema(
                    type='object',
                    properties={
                        "message": openapi.Schema(type='string', description="Sesion cerrada con exito"),
                    }
                )
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                description="Datos enviados incorrectos",
                schema=openapi.Schema(
                    type='object',
                    properties={
                        "message": openapi.Schema(type="string", description="No existe este usuario")
                    }
                )
            ),
        }
    )

    def post(self, request, *args, **kwargs):
        id = request.data.get('id', '')
        user = User.objects.filter(id=id)
        if user.exists():
            RefreshToken.for_user(user.first())
            return Response({
                'message': 'Sesion cerrada con exito'
            }, status=status.HTTP_200_OK)
        return Response({
                'message': 'No existe este usuario'
            }, status=status.HTTP_400_BAD_REQUEST)