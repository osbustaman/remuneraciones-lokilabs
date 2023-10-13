
from rest_framework import serializers
from applications.usuario.models import ConceptUser

class AsociateConceptUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConceptUser
        fields = ('user', 'concept')

class ConceptUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConceptUser
        fields = '__all__'