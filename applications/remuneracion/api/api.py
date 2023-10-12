from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework import serializers
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny

from applications.remuneracion.api.serializers import AsociateConceptUserSerializer
from applications.security.decorators import verify_token

@permission_classes([AllowAny])
class ApiAddConcept(generics.CreateAPIView):
    
    serializer_class = AsociateConceptUserSerializer

    #@verify_token
    def post(self, request, *args, **kwargs):

        try:
            serializer = self.serializer_class(data = request.data)

            # serializer es válido, en caso contrario lanza una excepción y devuelve una respuesta de error
            serializer.is_valid(raise_exception=True)
            serializer.save()
            response_data = {
                "data_serializer": serializer.data,
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        
        except serializers.ValidationError as e:
            # Capturar la excepción de validación del serializer y devolver la respuesta de error correspondiente
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            # Capturar cualquier otra excepción y devolver una respuesta de error genérica, además de registrar el error en el log
            return Response({'detail': 'Ha ocurrido un error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
