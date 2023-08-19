from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny

from applications.empresa.models import Afp
from applications.usuario.api.serializer import AfpSerializer

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