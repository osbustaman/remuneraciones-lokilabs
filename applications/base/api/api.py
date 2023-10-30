from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import AllowAny

from applications.base.api.serializer import ClienteSerializers

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from applications.base.models import Cliente

# Define el objeto Parameter para el encabezado Authorization
header_param = openapi.Parameter(
    name="Authorization",
    in_=openapi.IN_HEADER,
    type=openapi.TYPE_STRING,
    description="Token Bearer",
)

@permission_classes([AllowAny])
class ClientesListApiView(generics.ListAPIView):
    # Here you get the list of all registred tipo_producto
    serializer_class = ClienteSerializers

    @swagger_auto_schema(
        manual_parameters=[header_param],
        operation_id="Listar clientes",
        operation_description="Se obtiene un listado con toda la información de los clientes que se encuentran dentro de la plataforma",
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
        

@permission_classes([AllowAny])
class NamesClientesListApiView(generics.ListAPIView):
    # Here you get the list of all registred tipo_producto
    queryset = Cliente.objects.all()

    @swagger_auto_schema(
        manual_parameters=[header_param],
        operation_id="Obtener el nombre de los clientes",
        operation_description="Se obtiene un listado con los nombres de los clientes que se encuentran dentro de la plataforma",
    )
    def list(self, request, *args, **kwargs):
        try:
            #get_all_clientes = Cliente.objects.filter(deleted='N')
            get_all_clientes = self.queryset.filter(deleted='N')
            
            
            list_data = []
            for value in get_all_clientes:
                list_data.append({
                    f"{value.nombre_cliente.lower()}": value.nombre_cliente.lower()
                })

            return Response(list_data, status=status.HTTP_200_OK)

        except Exception as inst:
            data = {
                "type_error": type(inst)
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)