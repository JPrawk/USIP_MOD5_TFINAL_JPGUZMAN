from django.contrib import admin
from .models import Categoria, Genero, Autor, Libro, ArchivoLibro


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'padre', 'paginas', 'recomendacion']
    search_fields = ['nombre']
    list_filter = ['padre']
    ordering = ['nombre']
    fields = ['nombre', 'descripcion', 'padre', 'paginas', 'recomendacion']


@admin.register(Genero)
class GeneroAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'tipo', 'padre', 'paginas', 'recomendacion']
    search_fields = ['nombre']
    list_filter = ['tipo', 'padre']
    ordering = ['tipo', 'nombre']
    fields = ['nombre', 'tipo', 'padre', 'descripcion', 'paginas', 'recomendacion']


@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'nacionalidad', 'recomendacion']
    search_fields = ['nombre', 'nacionalidad']
    ordering = ['nombre']
    fields = ['nombre', 'nacionalidad', 'biografia', 'recomendacion']


class ArchivoLibroInline(admin.TabularInline):
    model = ArchivoLibro
    extra = 0
    fields = ['tipo', 'archivo', 'descripcion', 'paginas', 'recomendacion']


@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    list_display = [
        'titulo', 'autor', 'genero',
        'categoria', 'anio_publicacion',
        'paginas', 'recomendacion'
    ]
    search_fields = ['titulo', 'autor__nombre']
    list_filter = ['genero', 'categoria', 'anio_publicacion']
    ordering = ['-anio_publicacion', 'titulo']
    fields = [
        'titulo', 'autor', 'genero', 'categoria',
        'anio_publicacion', 'descripcion',
        'portada', 'paginas', 'recomendacion'
    ]
    inlines = [ArchivoLibroInline]


@admin.register(ArchivoLibro)
class ArchivoLibroAdmin(admin.ModelAdmin):
    list_display = ['libro', 'tipo', 'paginas', 'recomendacion']
    list_filter = ['tipo']
    ordering = ['libro', 'tipo']
    fields = ['libro', 'tipo', 'archivo', 'descripcion', 'paginas', 'recomendacion']