from rest_framework import serializers
from .models import Categoria, Genero, Autor, Libro, ArchivoLibro
import datetime


class CategoriaSerializer(serializers.ModelSerializer):
    subcategorias = serializers.SerializerMethodField()

    class Meta:
        model = Categoria
        ref_name = 'CategoriaLibros'
        fields = [
            'id', 'nombre', 'descripcion',
            'padre', 'recomendacion', 'paginas',
            'subcategorias'
        ]

    def get_subcategorias(self, obj):
        subcat = obj.subcategorias.all()
        return [{'id': c.id, 'nombre': c.nombre} for c in subcat]


class GeneroSerializer(serializers.ModelSerializer):
    subgeneros = serializers.SerializerMethodField()

    class Meta:
        model = Genero
        fields = [
            'id', 'nombre', 'tipo',
            'padre', 'descripcion',
            'recomendacion', 'paginas',
            'subgeneros'
        ]

    def get_subgeneros(self, obj):
        subgeneros = obj.subgeneros.all()
        return [{'id': g.id, 'nombre': g.nombre, 'tipo': g.tipo} for g in subgeneros]


class AutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Autor
        fields = [
            'id', 'nombre', 'nacionalidad',
            'biografia', 'recomendacion'
        ]


class ArchivoLibroSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArchivoLibro
        fields = [
            'id', 'libro', 'tipo', 'archivo',
            'descripcion', 'recomendacion', 'paginas',
            'created_at', 'updated_at'
        ]


class LibroReadSerializer(serializers.ModelSerializer):
    archivos = ArchivoLibroSerializer(many=True, read_only=True)
    autor_nombre = serializers.CharField(source='autor.nombre', read_only=True)
    genero_nombre = serializers.CharField(source='genero.nombre', read_only=True)
    categoria_nombre = serializers.CharField(source='categoria.nombre', read_only=True)

    class Meta:
        model = Libro
        fields = [
            'id', 'titulo',
            'autor', 'autor_nombre',
            'genero', 'genero_nombre',
            'categoria', 'categoria_nombre',
            'anio_publicacion', 'descripcion',
            'portada', 'recomendacion', 'paginas',
            'created_at', 'updated_at',
            'archivos'
        ]


class LibroWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Libro
        fields = [
            'id', 'titulo', 'autor', 'genero',
            'categoria', 'anio_publicacion', 'descripcion',
            'portada', 'recomendacion', 'paginas'
        ]

    def validate_anio_publicacion(self, value):
        anio_actual = datetime.date.today().year
        if value > anio_actual:
            raise serializers.ValidationError(
                f'El año no puede ser mayor a {anio_actual}.'
            )
        if value < 1000:
            raise serializers.ValidationError('El año no es válido.')
        return value


class ReporteLibrosSerializer(serializers.Serializer):
    total_libros = serializers.IntegerField()
    total_autores = serializers.IntegerField()
    libros = LibroReadSerializer(many=True)