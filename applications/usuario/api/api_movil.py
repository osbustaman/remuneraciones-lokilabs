from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from applications.usuario.api.serializer import UserTokenSerializer

from django.contrib.auth import authenticate


from applications.usuario.models import UserToken

class LoginUserAppCreateView(CreateAPIView):
    serializer_class = UserTokenSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            username = request.data.get('username', '')
            password = request.data.get('password', '')
            user = authenticate(
                username=username,
                password=password
            )

            if user:
                login_serializer = self.serializer_class(data=request.data)
                if login_serializer.is_valid():

                    user_token = UserToken.objects.filter(user=user)
                    if user_token.exists():
                        user_token.first().ut_token = login_serializer._kwargs['data']['ut_token']
                        user_token.first().ut_device = login_serializer._kwargs['data']['ut_device']
                        user_token.first().save()
                    else:
                        UserToken.objects.create(
                            user=user,
                            ut_token=login_serializer._kwargs['data']['ut_token'],
                            ut_device=login_serializer._kwargs['data']['ut_device']
                        )

                    return Response({"mensaje": True}, status=status.HTTP_200_OK)
                return Response({
                    'error': 'Contraseña o nombre de usuario incorrectos'
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(str(e))
            return Response({
                    'error': 'Contraseña o nombre de usuario incorrectos'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        # Si los datos no son válidos, retornar mensajes de error
        return Response({'error': 'Los datos proporcionados no son válidos.'}, status=status.HTTP_400_BAD_REQUEST)
