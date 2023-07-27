from rest_framework import serializers

from django.core.validators import validate_email
from django.core.exceptions import ValidationError

class BulkLoadExcelSerializer(serializers.Serializer):
    excel_carga_masiva = serializers.CharField(max_length=None)