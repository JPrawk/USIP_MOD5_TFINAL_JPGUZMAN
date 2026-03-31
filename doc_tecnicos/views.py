from rest_framework import viewsets
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
import logging

from .models import Categoria, OrganismoNorma, DocumentoTecnico, LibroIngElectrica
from .serializers import (
    CategoriaSerializer,
    OrganismoNormaSerializer,
    DocumentoTecnicoSerializer,
    LibroIngElectricaSerializer,
    ReporteDocumentosSerializer,
)
from .permissions import IsUserDocumentalista
from .utils import permission_required

logger = logging.getLogger(__name__)


# ==================== VISTAS HTML ====================

def documentos_lista(request):
    q = request.GET.get('q', '')
    organismo_id = request.GET.get('organismo', '')
    documentos = DocumentoTecnico.objects.select_related(
        'organismo', 'categoria'
    ).all()
    if q:
        documentos = documentos.filter(titulo__icontains=q) | \
                     documentos.filter(codigo__icontains=q)
    if organismo_id:
        documentos = documentos.filter(organismo__id=organismo_id)
    context = {
        'documentos': documentos,
        'organismos': OrganismoNorma.objects.all(),
    }
    return render(request, 'doc_tecnicos/lista.html', context)


def documentos_detalle(request, pk):
    documento = get_object_or_404(
        DocumentoTecnico.objects.select_related('organismo', 'categoria'),
        pk=pk
    )
    return render(request, 'doc_tecnicos/detalle.html', {'documento': documento})


def organismos_lista(request):
    organismos = OrganismoNorma.objects.all()
    return render(request, 'organismos/lista.html', {'organismos': organismos})


# ==================== VISTAS API REST ====================

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer


class OrganismoNormaViewSet(viewsets.ModelViewSet):
    queryset = OrganismoNorma.objects.all()
    serializer_class = OrganismoNormaSerializer


class DocumentoTecnicoViewSet(viewsets.ModelViewSet):
    queryset = DocumentoTecnico.objects.select_related(
        'organismo', 'categoria'
    ).all()
    serializer_class = DocumentoTecnicoSerializer
    permission_classes = [IsUserDocumentalista]

    @action(detail=False, methods=['get'],
            url_path='por-organismo/(?P<organismo_id>[^/.]+)')
    def por_organismo(self, request, organismo_id=None):
        try:
            organismo = OrganismoNorma.objects.get(id=organismo_id)
            documentos = DocumentoTecnico.objects.filter(
                organismo=organismo
            ).select_related('categoria')
            serializer = self.get_serializer(documentos, many=True)
            logger.info(
                f'Documentos por organismo {organismo.norma}: {documentos.count()}'
            )
            return Response(serializer.data)
        except OrganismoNorma.DoesNotExist:
            logger.error(f'Organismo {organismo_id} no encontrado')
            return Response({'error': 'Organismo no encontrado'}, status=404)
        except Exception as e:
            logger.error(f'Error en por_organismo: {str(e)}')
            return Response({'error': str(e)}, status=400)


class LibroIngElectricaViewSet(viewsets.ModelViewSet):
    queryset = LibroIngElectrica.objects.select_related('categoria').all()
    serializer_class = LibroIngElectricaSerializer
    permission_classes = [IsUserDocumentalista]


@api_view(['GET'])
def reporte_documentos(request):
    try:
        total_documentos = DocumentoTecnico.objects.count()
        total_organismos = OrganismoNorma.objects.count()
        documentos = DocumentoTecnico.objects.select_related(
            'organismo', 'categoria'
        ).all()
        serializer = ReporteDocumentosSerializer({
            'total_documentos': total_documentos,
            'total_organismos': total_organismos,
            'documentos': documentos,
        })
        logger.info(
            f'Reporte documentos: {total_documentos} docs, {total_organismos} organismos'
        )
        return Response(serializer.data)
    except Exception as e:
        logger.error(f'Error en reporte_documentos: {str(e)}')
        return JsonResponse({'error': str(e)}, status=400)