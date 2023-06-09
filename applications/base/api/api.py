import pandas as pd

from rest_framework.response import Response
from rest_framework import generics, status

from django.contrib.auth.models import User

from app01.functions import elige_choices
from applications.base.api.serializer import (
    ClienteSerializers
    , UserSerializer
)

from applications.base.models import Cliente, Comuna, Pais, Region
from applications.base.utils import (
    armarParametrosGeneralesDelSistema
    , crearMigrate
    , create_database
    , generate_pdf
)

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

# Define el objeto Parameter para el encabezado Authorization
header_param = openapi.Parameter(
    name="Authorization",
    in_=openapi.IN_HEADER,
    type=openapi.TYPE_STRING,
    description="Token Bearer",
)

class ClienteCreateAPIView(generics.CreateAPIView):
    serializer_class = ClienteSerializers

    @swagger_auto_schema(
        manual_parameters=[header_param],
        operation_id="My Operation ID",
        operation_description="My Operation Description",
        security=[{"Bearer": []}]
    )
    def post(self, request, format=None):
        serializer = ClienteSerializers(data=request.data)
        if serializer.is_valid():

            ## Guarda los datos del cliente
            serializer.save()

            # Crea la base de datos y su migración
            create_database(request.data)
            crearMigrate(request.data)
            armarParametrosGeneralesDelSistema(request.data)

            response_to_page = {
                "data_serializer": serializer.data
            }

            return Response(response_to_page, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ClientesListApiView(generics.ListAPIView):
    # Here you get the list of all registred tipo_producto
    serializer_class = ClienteSerializers

    @swagger_auto_schema(
        manual_parameters=[header_param],
        operation_id="Listar clientes",
        operation_description="Se obtiene un listado con toda la información de los clientes que se encuentran dentro de la plataforma",
        security=[{"Bearer": []}]
    )
    def list(self, request, *args, **kwargs):
        try:
            get_all_clientes = Cliente.objects.filter(deleted='N')
            data = {'data': list(get_all_clientes.values())}
            return Response(data, status=status.HTTP_201_CREATED)

        except Exception as inst:
            data = {
                "type_error": type(inst)
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

class ClientesDetailApiView(generics.RetrieveAPIView):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializers

    @swagger_auto_schema(
        manual_parameters=[header_param],
        operation_id="Obtener cliente por ID",
        operation_description="Se obtiene obtiene toda la información de un cliente en particular",
        security=[{"Bearer": []}]
    )
    def get(self, request, *args, **kwargs):
        object_cliente = Cliente.objects.filter(id=self.kwargs['pk'])
        data = {'data': list(object_cliente.values())}
        return Response(data, status=status.HTTP_201_CREATED)
    
class ClienteRetriveUpdateView(generics.UpdateAPIView):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializers

    @swagger_auto_schema(
        manual_parameters=[header_param],
        operation_id="Actualizar cliente",
        operation_description="Se actualiza toda la información de un cliente en particular",
        security=[{"Bearer": []}]
    )   
    
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        pk = int(kwargs['pk'])
        cliente = Cliente.objects.get(pk=pk)
        cliente_serializer = self.serializer_class(cliente, data=request.data)
        if cliente_serializer.is_valid():
            cliente_serializer.cli_link = request.data['cli_link']
            cliente_serializer.save()
            return Response(cliente_serializer.data, status=status.HTTP_200_OK)
        return Response(cliente_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

"""class ClienteDeleteView(generics.DestroyAPIView):
    # From here a tipo_producto is delete 
    serializer_class = ClienteSerializers
    queryset = Cliente.objects.all()"""

class ClienteDeleteView(generics.ListAPIView):
    # From here a tipo_producto is delete 
    serializer_class = ClienteSerializers
    def get_queryset(self):
        return None

    @swagger_auto_schema(
        manual_parameters=[header_param],
        operation_id="Borrado logico de un cliente",
        operation_description="Borrado logico de un cliente",
        security=[{"Bearer": []}]
    )
    def get(self, request, *args, **kwargs):

        try:
            object_cliente = Cliente.objects.get(id=self.kwargs['pk'])
            object_cliente.deleted = "S"
            object_cliente.save()
            
            data = {"data": True}
            
            # Devolver la respuesta HTTP
            return Response(data, status=status.HTTP_200_OK)
        
        except Exception as inst:
            data = {
                "type_error": type(inst)
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

class AdminUserCreateAPIView(generics.CreateAPIView):
    queryset = User.objects.none()
    serializer_class = UserSerializer

    @swagger_auto_schema(
        manual_parameters=[header_param],
        operation_id="Creación de usuario por cliente",
        operation_description="Desde aquí se crea un cliente para un cliente",
        security=[{"Bearer": []}]
    )
    def post(self, request, pk):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            client = Cliente.objects.get(id=pk)
            database_name = client.nombre_bd

            form = User()
            form.username = request.data['username']
            form.first_name = request.data['first_name']
            form.last_name = request.data['last_name']
            form.email = request.data['email']
            form.set_password(request.data['password'])
            form.is_staff = True
            form.is_superuser = True
            form.save(using=database_name)

            return Response({'success': True}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PdfDataClientApiView(generics.ListAPIView):
    # Here you get the list of all registred users
    serializer_class = ClienteSerializers

    def get_queryset(self):
        return None

    @swagger_auto_schema(
        manual_parameters=[header_param],
        operation_id="Pdf datos cliente",
        operation_description="Este endpoint entrega la información de uncliente en un formato de base64 el cual debe ser codificado en el Front",
        security=[{"Bearer": []}]
    )
    def get(self, request, *args, **kwargs):
        try:
            object_cliente = Cliente.objects.get(id=self.kwargs['pk'])
            object_pais = Pais.objects.get(pa_id=object_cliente.pais.pa_id)
            object_region = Region.objects.get(re_id=object_cliente.region.re_id)
            object_comuna = Comuna.objects.get(com_id=object_cliente.comuna.com_id)

            clientData = {
                "nombre_cliente": object_cliente.nombre_cliente,
                "rut_cliente": object_cliente.rut_cliente,
                "nombre_bd": object_cliente.nombre_bd,
                "cli_link": object_cliente.cli_link,
                "cliente_activo": elige_choices(object_cliente.OPCIONES, object_cliente.cliente_activo),
                "fecha_ingreso": object_cliente.fecha_ingreso,
                "fecha_termino": object_cliente.fecha_termino,
                "cantidad_usuarios": object_cliente.cantidad_usuarios,
                "nombre_representante": object_cliente.nombre_representante,
                "rut_representante": object_cliente.rut_representante,
                "correo_representante": object_cliente.correo_representante,
                "telefono_representante": object_cliente.telefono_representante,
                "dirección_representante": object_cliente.dirección_representante,
                "pais": object_pais.pa_nombre,
                "region": object_region.re_nombre,
                "comuna": object_comuna.com_nombre
            }
            
            # Generar el archivo PDF de manera asíncrona
            encoded_pdf = generate_pdf("", True, 'ficha_cliente.html', clientData)
                        
            # Crear la respuesta HTTP con el archivo PDF codificado en base64
            response = Response(encoded_pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'inline; filename="hello.pdf"'
            response = vars(response)

            data = {
                "pdf": response['data']
            }
            
            # Devolver la respuesta HTTP
            return Response(data, status=status.HTTP_200_OK)
        
        except Exception as inst:
            data = {
                "type_error": type(inst)
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

class PdfContratoClientApiView(generics.ListAPIView):
    # Here you get the list of all registred users
    serializer_class = ClienteSerializers

    def get_queryset(self):
        return None

    @swagger_auto_schema(
        manual_parameters=[header_param],
        operation_id="Pdf contrato cliente",
        operation_description="Este endpoint entrega contrato de un cliente en un formato de base64 el cual debe ser codificado en el Front",
        security=[{"Bearer": []}]
    )
    def get(self, request, *args, **kwargs):
        try:
            object_cliente = Cliente.objects.get(id=self.kwargs['pk'])
            object_pais = Pais.objects.get(pa_id=object_cliente.pais.pa_id)
            object_region = Region.objects.get(re_id=object_cliente.region.re_id)
            object_comuna = Comuna.objects.get(com_id=object_cliente.comuna.com_id)

            clientData = {
                "nombre_cliente": object_cliente.nombre_cliente,
                "rut_cliente": object_cliente.rut_cliente,
                "fecha_ingreso": object_cliente.fecha_ingreso,
                "fecha_termino": object_cliente.fecha_termino,
                "cantidad_usuarios": object_cliente.cantidad_usuarios,
                "nombre_representante": object_cliente.nombre_representante,
                "rut_representante": object_cliente.rut_representante,
                "correo_representante": object_cliente.correo_representante,
                "telefono_representante": object_cliente.telefono_representante,
                "dirección_representante": object_cliente.dirección_representante,
                "pais": object_pais.pa_nombre,
                "region": object_region.re_nombre,
                "comuna": object_comuna.com_nombre
            }
            
            # Generar el archivo PDF de manera asíncrona
            encoded_pdf = generate_pdf("", True, 'contrato_cliente.html', clientData)
                        
            # Crear la respuesta HTTP con el archivo PDF codificado en base64
            response = Response(encoded_pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'inline; filename="hello.pdf"'
            response = vars(response)

            data = {
                "pdf": response['data']
            }
            
            # Devolver la respuesta HTTP
            return Response(data, status=status.HTTP_200_OK)
        
        except Exception as inst:
            data = {
                "type_error": type(inst)
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)