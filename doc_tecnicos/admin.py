from django.contrib import admin
from .models import Categoria, OrganismoNorma, DocumentoTecnico, LibroIngElectrica


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'padre', 'paginas', 'recomendacion']
    search_fields = ['nombre']
    list_filter = ['padre']
    ordering = ['nombre']
    fields = ['nombre', 'descripcion', 'padre', 'paginas', 'recomendacion']


class DocumentoTecnicoInline(admin.TabularInline):
    model = DocumentoTecnico
    extra = 0
    fields = ['codigo', 'titulo', 'anio', 'paginas']


@admin.register(OrganismoNorma)
class OrganismoNormaAdmin(admin.ModelAdmin):
    list_display = ['norma', 'denominacion', 'codigo', 'anio', 'paginas', 'recomendacion']
    search_fields = ['norma', 'denominacion', 'codigo']
    ordering = ['norma']
    fields = ['norma', 'denominacion', 'codigo', 'anio', 'texto', 'descripcion', 'paginas', 'recomendacion']
    inlines = [DocumentoTecnicoInline]

@admin.register(DocumentoTecnico)
class DocumentoTecnicoAdmin(admin.ModelAdmin):
    list_display = [
        'codigo', 'titulo', 'organismo',
        'categoria', 'anio',
        'paginas', 'recomendacion'
    ]
    search_fields = ['codigo', 'titulo']
    list_filter = ['organismo', 'categoria', 'anio']
    ordering = ['-anio', 'titulo']
    fields = [
        'titulo', 'codigo', 'organismo', 'categoria',
        'anio', 'descripcion', 'archivo',
        'paginas', 'recomendacion'
    ]


@admin.register(LibroIngElectrica)
class LibroIngElectricaAdmin(admin.ModelAdmin):
    list_display = [
        'titulo', 'autor', 'categoria',
        'anio', 'paginas', 'recomendacion'
    ]
    search_fields = ['titulo', 'autor']
    list_filter = ['categoria', 'anio']
    ordering = ['-anio', 'titulo']
    fields = [
        'titulo', 'autor', 'categoria', 'anio',
        'descripcion', 'archivo',
        'paginas', 'recomendacion'
    ]