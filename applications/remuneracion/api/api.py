from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework import serializers
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny

from applications.remuneracion.api.serializers import AsociateConceptUserSerializer, ConceptUserSerializer
from applications.remuneracion.remuneracion import Remunerations
from applications.security.decorators import verify_token
from applications.usuario.models import ConceptUser

@permission_classes([AllowAny])
class ApiAddMountConceptUser(generics.UpdateAPIView):

    serializer_class = ConceptUserSerializer

    def update(self, request, *args, **kwargs):
        response = self.get_object(request) 

        response_data = {
            "status": response.status_code,
            "message": response.data
        }
        return Response(response_data, status=status.HTTP_200_OK)
    
    def get_object(self, request):
        try:
            # Obtenemos los parámetros de la URL
            user_id = int(self.kwargs['user_id'])
            concept_id = int(self.kwargs['concept_id'])
            cu_value = int(request.data['cu_value'])

            # Filtramos el queryset por user y concept
            obj = ConceptUser.objects.get(user__id=user_id, concept__conc_id=concept_id)
            obj.cu_value = cu_value
            obj.save()
            return Response({'detail': 'actualizado con éxito'}, status=status.HTTP_201_CREATED)
        
        except serializers.ValidationError as e:
            # Capturar la excepción de validación del serializer y devolver la respuesta de error correspondiente
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            # Capturar cualquier otra excepción y devolver una respuesta de error genérica, además de registrar el error en el log
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@permission_classes([AllowAny])
class ApiAddConcept(generics.CreateAPIView):
    
    serializer_class = AsociateConceptUserSerializer
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


@permission_classes([AllowAny])
class ApiConceptUserDeleteView(generics.DestroyAPIView):
    queryset = ConceptUser.objects.all()
    serializer_class = ConceptUserSerializer

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.delete()

        response_data = {
            "success": True,
            "status": 200
        }
        return Response(response_data, status=status.HTTP_200_OK)

    def get_object(self):
        try:
            # Obtenemos los parámetros de la URL
            user_id = int(self.kwargs['user_id'])
            concept_id = int(self.kwargs['concept_id'])

            # Filtramos el queryset por user y concept
            obj = ConceptUser.objects.get(user__id=user_id, concept__conc_id=concept_id)
            return obj
        
        except serializers.ValidationError as e:
            # Capturar la excepción de validación del serializer y devolver la respuesta de error correspondiente
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            # Capturar cualquier otra excepción y devolver una respuesta de error genérica, además de registrar el error en el log
            return Response({'detail': 'Ha ocurrido un error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

@permission_classes([AllowAny])
class ApiGenerateLiquidationUserDeleteView(generics.GenericAPIView):
    queryset = ConceptUser.objects.all()
    serializer_class = ConceptUserSerializer

    def get(self, request, *args, **kwargs):
        try:
            user_id = kwargs['user_id']
            response_data = Remunerations.generate_remunaration(user_id)
            # response_data = Remunerations.get_detail_of_hours_worked(user_id)
            return Response(response_data, status=status.HTTP_200_OK)

        except serializers.ValidationError as e:
            # Capturar la excepción de validación del serializer y devolver la respuesta de error correspondiente
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            # Capturar cualquier otra excepción y devolver una respuesta de error genérica, además de registrar el error en el log
            return Response({'detail': 'Ha ocurrido un error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        









