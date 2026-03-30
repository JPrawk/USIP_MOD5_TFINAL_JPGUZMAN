from rest_framework import serializers
from .models import Genero, Autor, Libro, ArchivoLibro

class GeneroSerializer(serializers.ModelSerializer):
    subgeneros = serializers.SerializerMethodField()

    class Meta:
        model = Genero
        fields = '__all__'

    def get_subgeneros(self, obj):
        return GeneroSerializer(obj.subgeneros.all(), many=True).data

class AutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Autor
        fields = '__all__'

class ArchivoLibroSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArchivoLibro
        fields = '__all__'

class LibroSerializer(serializers.ModelSerializer):
    archivos = ArchivoLibroSerializer(many=True, read_only=True)
    autor_nombre = serializers.CharField(source='autor.nombre', read_only=True)
    genero_nombre = serializers.CharField(source='genero.nombre', read_only=True)

    class Meta:
        model = Libro
        fields = '__all__'