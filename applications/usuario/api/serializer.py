from rest_framework import serializers

from applications.empresa.models import Afp

# Afp serializer
class AfpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Afp
        fields = ('__all__')
