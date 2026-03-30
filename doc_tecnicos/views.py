from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import OrganismoNorma, DocumentoTecnico
from .serializers import OrganismoNormaSerializer, DocumentoTecnicoSerializer

class OrganismoNormaViewSet(viewsets.ModelViewSet):
    queryset = OrganismoNorma.objects.all()
    serializer_class = OrganismoNormaSerializer

class DocumentoTecnicoViewSet(viewsets.ModelViewSet):
    queryset = DocumentoTecnico.objects.all()
    serializer_class = DocumentoTecnicoSerializer

    @action(detail=False, methods=['get'], url_path='por-organismo/(?P<organismo_id>[^/.]+)')
    def por_organismo(self, request, organismo_id=None):
        documentos = DocumentoTecnico.objects.filter(organismo__id=organismo_id)
        serializer = self.get_serializer(documentos, many=True)
        return Response(serializer.data)