import datetime

from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework import generics, status, serializers
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny

from applications.usuario.models import UserToken


class LoginUserAppCreateView(generics.CreateAPIView):
    """
    Login user app
    """
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data.get('user')
            token, created = UserToken.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name
                }
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)