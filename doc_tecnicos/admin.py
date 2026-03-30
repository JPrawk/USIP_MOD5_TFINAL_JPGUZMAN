from django.contrib import admin
from .models import OrganismoNorma, DocumentoTecnico

@admin.register(OrganismoNorma)
class OrganismoNormaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion']
    search_fields = ['nombre']

@admin.register(DocumentoTecnico)
class DocumentoTecnicoAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'titulo', 'organismo', 'anio']
    search_fields = ['codigo', 'titulo']
    list_filter = ['organismo', 'anio']