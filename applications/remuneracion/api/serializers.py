
from rest_framework import serializers
from applications.usuario.models import ConceptUser

class AsociateConceptUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConceptUser
        fields = ('user', 'concept')