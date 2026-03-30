from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Genero, Autor, Libro, ArchivoLibro
from .serializers import GeneroSerializer, AutorSerializer, LibroSerializer, ArchivoLibroSerializer

class GeneroViewSet(viewsets.ModelViewSet):
    queryset = Genero.objects.all()
    serializer_class = GeneroSerializer

class AutorViewSet(viewsets.ModelViewSet):
    queryset = Autor.objects.all()
    serializer_class = AutorSerializer

class LibroViewSet(viewsets.ModelViewSet):
    queryset = Libro.objects.all()
    serializer_class = LibroSerializer

    @action(detail=False, methods=['get'], url_path='por-genero/(?P<genero_id>[^/.]+)')
    def por_genero(self, request, genero_id=None):
        libros = Libro.objects.filter(genero__id=genero_id)
        serializer = self.get_serializer(libros, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='por-autor/(?P<autor_id>[^/.]+)')
    def por_autor(self, request, autor_id=None):
        libros = Libro.objects.filter(autor__id=autor_id)
        serializer = self.get_serializer(libros, many=True)
        return Response(serializer.data)

class ArchivoLibroViewSet(viewsets.ModelViewSet):
    queryset = ArchivoLibro.objects.all()
    serializer_class = ArchivoLibroSerializer