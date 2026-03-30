from django.contrib import admin
from .models import Genero, Autor, Libro, ArchivoLibro

@admin.register(Genero)
class GeneroAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'tipo', 'padre']
    search_fields = ['nombre']
    list_filter = ['tipo']

@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'nacionalidad']
    search_fields = ['nombre']

@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'autor', 'genero', 'anio_publicacion']
    search_fields = ['titulo', 'autor__nombre']
    list_filter = ['genero']

@admin.register(ArchivoLibro)
class ArchivoLibroAdmin(admin.ModelAdmin):
    list_display = ['libro', 'tipo']
    list_filter = ['tipo']