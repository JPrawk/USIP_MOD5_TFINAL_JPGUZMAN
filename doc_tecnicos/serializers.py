from rest_framework import serializers
from .models import Categoria, OrganismoNorma, DocumentoTecnico, LibroIngElectrica
import datetime


class CategoriaSerializer(serializers.ModelSerializer):
    subcategorias = serializers.SerializerMethodField()

    class Meta:
        model = Categoria
        ref_name = 'CategoriaDocTecnicos'
        fields = [
            'id', 'nombre', 'descripcion',
            'padre', 'recomendacion', 'paginas',
            'subcategorias'
        ]

    def get_subcategorias(self, obj):
        subcat = obj.subcategorias.all()
        return [{'id': c.id, 'nombre': c.nombre} for c in subcat]


class OrganismoNormaSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganismoNorma
        fields = [
            'id', 'norma', 'denominacion',
            'codigo', 'anio', 'texto',
            'descripcion', 'recomendacion', 'paginas'
        ]


class DocumentoTecnicoSerializer(serializers.ModelSerializer):
    organismo_nombre = serializers.CharField(
        source='organismo.nombre',
        read_only=True
    )
    categoria_nombre = serializers.CharField(
        source='categoria.nombre',
        read_only=True
    )

    class Meta:
        model = DocumentoTecnico
        fields = [
            'id', 'titulo', 'codigo',
            'organismo', 'organismo_nombre',
            'categoria', 'categoria_nombre',
            'anio', 'descripcion', 'archivo',
            'recomendacion', 'paginas',
            'created_at', 'updated_at'
        ]

    def validate_anio(self, value):
        anio_actual = datetime.date.today().year
        if value > anio_actual:
            raise serializers.ValidationError(
                f'El año no puede ser mayor a {anio_actual}.'
            )
        if value < 1900:
            raise serializers.ValidationError('El año no es válido.')
        return value


class LibroIngElectricaSerializer(serializers.ModelSerializer):
    categoria_nombre = serializers.CharField(
        source='categoria.nombre',
        read_only=True
    )

    class Meta:
        model = LibroIngElectrica
        fields = [
            'id', 'titulo', 'autor',
            'categoria', 'categoria_nombre',
            'anio', 'descripcion', 'archivo',
            'recomendacion', 'paginas',
            'created_at', 'updated_at'
        ]

    def validate_anio(self, value):
        anio_actual = datetime.date.today().year
        if value > anio_actual:
            raise serializers.ValidationError(
                f'El año no puede ser mayor a {anio_actual}.'
            )
        if value < 1900:
            raise serializers.ValidationError('El año no es válido.')
        return value


class ReporteDocumentosSerializer(serializers.Serializer):
    total_documentos = serializers.IntegerField()
    total_organismos = serializers.IntegerField()
    documentos = DocumentoTecnicoSerializer(many=True)