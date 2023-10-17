
from django.db.models import F, Value, CharField
from django.db.models.functions import Concat

from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny

from applications.empresa.models import Afp
from applications.usuario.api.serializer import AfpSerializer

from django.contrib.auth.models import User

from applications.usuario.models import Colaborador, Contact

@permission_classes([AllowAny])
class AfpDetailApiView(generics.RetrieveAPIView):
    queryset = Afp.objects.all()
    serializer_class = AfpSerializer

    def get(self, request, *args, **kwargs):
        try:
            object = self.queryset.filter(afp_id=self.kwargs['pk'])
            if object.exists():
                data = list(object.values())
                return Response(data, status=status.HTTP_201_CREATED)
            else:
                raise IndexError("La AFP no existe")
        except IndexError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        

@permission_classes([AllowAny])
class ApiGetDataUserPage(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = AfpSerializer

    def get(self, request, *args, **kwargs):
        try:
            object = self.queryset.filter(id=self.kwargs['pk'])
            if object.exists():
                object = object.first()

                last_name = (object.last_name).split(" ")

                object_colaborator = Colaborador.objects.get(user = object)


                object_contact = Contact.objects.filter(user = object)

                data = {
                    "username": object.username,
                    "first_name": object.first_name,
                    "first_last_name": last_name[0] if len(last_name) > 0 else '',
                    "second_last_name": last_name[1] if len(last_name) > 1 else '',

                    "col_fechanacimiento": object_colaborator.col_fechanacimiento,
                    "col_sexo": object_colaborator.get_col_sexo_display().title(),
                    "col_estadocivil": object_colaborator.get_col_estadocivil_display(),


                }
                return Response(data, status=status.HTTP_201_CREATED)
            else:
                raise IndexError("La AFP no existe")
        except IndexError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)