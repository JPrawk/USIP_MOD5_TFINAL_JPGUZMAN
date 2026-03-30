from rest_framework import serializers
from .models import OrganismoNorma, DocumentoTecnico

class OrganismoNormaSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganismoNorma
        fields = '__all__'

class DocumentoTecnicoSerializer(serializers.ModelSerializer):
    organismo_nombre = serializers.CharField(source='organismo.nombre', read_only=True)

    class Meta:
        model = DocumentoTecnico
        fields = '__all__'