from rest_framework import viewsets
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
import logging

from .models import Categoria, Genero, Autor, Libro, ArchivoLibro
from .serializers import (
    CategoriaSerializer,
    GeneroSerializer,
    AutorSerializer,
    LibroReadSerializer,
    LibroWriteSerializer,
    ArchivoLibroSerializer,
    ReporteLibrosSerializer,
)
from .permissions import IsUserBibliotecario
from .utils import permission_required

logger = logging.getLogger(__name__)


# ==================== VISTAS HTML ====================

def inicio(request):
    from doc_tecnicos.models import DocumentoTecnico, OrganismoNorma
    context = {
        'total_libros': Libro.objects.count(),
        'total_autores': Autor.objects.count(),
        'total_documentos': DocumentoTecnico.objects.count(),
        'total_organismos': OrganismoNorma.objects.count(),
        'ultimos_libros': Libro.objects.select_related(
            'autor', 'genero'
        ).order_by('-created_at')[:4],
        'ultimos_documentos': DocumentoTecnico.objects.select_related(
            'organismo'
        ).order_by('-created_at')[:5],
    }
    return render(request, 'inicio.html', context)


def libros_lista(request):
    q = request.GET.get('q', '')
    genero_id = request.GET.get('genero', '')
    libros = Libro.objects.select_related('autor', 'genero', 'categoria').all()
    if q:
        libros = libros.filter(titulo__icontains=q) | \
                 libros.filter(autor__nombre__icontains=q)
    if genero_id:
        libros = libros.filter(genero__id=genero_id)
    context = {
        'libros': libros,
        'generos': Genero.objects.all(),
    }
    return render(request, 'libros/lista.html', context)


def libros_detalle(request, pk):
    libro = get_object_or_404(
        Libro.objects.select_related('autor', 'genero', 'categoria'),
        pk=pk
    )
    return render(request, 'libros/detalle.html', {'libro': libro})


def autores_lista(request):
    q = request.GET.get('q', '')
    autores = Autor.objects.all()
    if q:
        autores = autores.filter(nombre__icontains=q) | \
                  autores.filter(nacionalidad__icontains=q)
    return render(request, 'autores/lista.html', {'autores': autores})


# ==================== VISTAS API REST ====================

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer


class GeneroViewSet(viewsets.ModelViewSet):
    queryset = Genero.objects.all()
    serializer_class = GeneroSerializer


class AutorViewSet(viewsets.ModelViewSet):
    queryset = Autor.objects.all()
    serializer_class = AutorSerializer

    @action(detail=True, methods=['get'])
    def libros(self, request, pk=None):
        try:
            autor = self.get_object()
            libros = autor.libros.select_related('genero', 'categoria').all()
            serializer = LibroReadSerializer(libros, many=True)
            logger.info(f'Libros del autor {autor.nombre}: {libros.count()}')
            return Response(serializer.data)
        except Exception as e:
            logger.error(f'Error al obtener libros del autor: {str(e)}')
            return Response({'error': str(e)}, status=400)


class LibroViewSet(viewsets.ModelViewSet):
    queryset = Libro.objects.select_related(
        'autor', 'genero', 'categoria'
    ).all()
    permission_classes = [IsUserBibliotecario]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return LibroWriteSerializer
        return LibroReadSerializer

    @action(detail=False, methods=['get'],
            url_path='por-genero/(?P<genero_id>[^/.]+)')
    def por_genero(self, request, genero_id=None):
        try:
            genero = Genero.objects.get(id=genero_id)
            libros = Libro.objects.filter(
                genero=genero
            ).select_related('autor', 'categoria')
            serializer = LibroReadSerializer(libros, many=True)
            logger.info(f'Libros por genero {genero.nombre}: {libros.count()}')
            return Response(serializer.data)
        except Genero.DoesNotExist:
            logger.error(f'Genero {genero_id} no encontrado')
            return Response({'error': 'Genero no encontrado'}, status=404)
        except Exception as e:
            logger.error(f'Error en por_genero: {str(e)}')
            return Response({'error': str(e)}, status=400)

    @action(detail=False, methods=['get'],
            url_path='por-autor/(?P<autor_id>[^/.]+)')
    def por_autor(self, request, autor_id=None):
        try:
            autor = Autor.objects.get(id=autor_id)
            libros = Libro.objects.filter(
                autor=autor
            ).select_related('genero', 'categoria')
            serializer = LibroReadSerializer(libros, many=True)
            logger.info(f'Libros por autor {autor.nombre}: {libros.count()}')
            return Response(serializer.data)
        except Autor.DoesNotExist:
            logger.error(f'Autor {autor_id} no encontrado')
            return Response({'error': 'Autor no encontrado'}, status=404)
        except Exception as e:
            logger.error(f'Error en por_autor: {str(e)}')
            return Response({'error': str(e)}, status=400)


class ArchivoLibroViewSet(viewsets.ModelViewSet):
    queryset = ArchivoLibro.objects.select_related('libro').all()
    serializer_class = ArchivoLibroSerializer


@api_view(['GET'])
def reporte_libros(request):
    try:
        total_libros = Libro.objects.count()
        total_autores = Autor.objects.count()
        libros = Libro.objects.select_related(
            'autor', 'genero', 'categoria'
        ).all()
        serializer = ReporteLibrosSerializer({
            'total_libros': total_libros,
            'total_autores': total_autores,
            'libros': libros,
        })
        logger.info(f'Reporte libros: {total_libros} libros, {total_autores} autores')
        return Response(serializer.data)
    except Exception as e:
        logger.error(f'Error en reporte_libros: {str(e)}')
        return JsonResponse({'error': str(e)}, status=400)