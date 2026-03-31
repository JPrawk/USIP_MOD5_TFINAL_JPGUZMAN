from django.db import models
from .validators import (
    validar_recomendacion,
    validar_extension_pdf,
    validar_anio,
)


class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    padre = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='subcategorias'
    )
    recomendacion = models.IntegerField(default=5, validators=[validar_recomendacion])
    paginas = models.IntegerField(default=0, help_text='Número de hojas')

    def __str__(self):
        if self.padre:
            return f'{self.padre.nombre} > {self.nombre}'
        return self.nombre

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'


class OrganismoNorma(models.Model):
    class Organismos(models.TextChoices):
        IEC = 'IEC', 'IEC - International Electrotechnical Commission'
        IEEE = 'IEEE', 'IEEE - Institute of Electrical and Electronics Engineers'
        NBR = 'NBR', 'NBR - Norma Brasileira'
        CIGRE = 'CIGRE', 'CIGRE - Conseil International des Grands Réseaux Électriques'
        ASTM = 'ASTM', 'ASTM - American Society for Testing and Materials'
        ASCE = 'ASCE', 'ASCE - American Society of Civil Engineers'
        NB = 'NB', 'NB - Norma Boliviana'

    norma = models.CharField(
        max_length=10,
        choices=Organismos.choices,
        unique=True,
        verbose_name='Norma'
    )
    denominacion = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Denominación'
    )
    codigo = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Código',
        help_text='Ej: IEC-60076'
    )
    anio = models.IntegerField(
        null=True,
        blank=True,
        validators=[validar_anio],
        verbose_name='Año'
    )
    texto = models.TextField(
        blank=True,
        verbose_name='Texto/Resumen'
    )
    descripcion = models.TextField(blank=True)
    recomendacion = models.IntegerField(default=5, validators=[validar_recomendacion])
    paginas = models.IntegerField(default=0, help_text='Número de hojas')

    def __str__(self):
        if self.denominacion:
            return f'{self.norma} - {self.denominacion}'
        return self.norma

    class Meta:
        verbose_name = 'Norma'
        verbose_name_plural = 'Normas'


class DocumentoTecnico(models.Model):
    titulo = models.CharField(max_length=300)
    codigo = models.CharField(max_length=100, unique=True)
    organismo = models.ForeignKey(
        OrganismoNorma,
        on_delete=models.CASCADE,
        related_name='documentos'
    )
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='documentos'
    )
    anio = models.IntegerField(validators=[validar_anio])
    descripcion = models.TextField(blank=True)
    archivo = models.FileField(
        upload_to='doc_tecnicos/',
        validators=[validar_extension_pdf]
    )
    recomendacion = models.IntegerField(default=5, validators=[validar_recomendacion])
    paginas = models.IntegerField(default=0, help_text='Número de hojas')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.organismo.norma} - {self.codigo}: {self.titulo}'

    class Meta:
        verbose_name = 'Artículo técnico'
        verbose_name_plural = 'Artículos técnicos'
        permissions = [
            ('ver_reporte_documentos', 'Ver reporte de documentos'),
            ('descargar_documento', 'Descargar documento técnico'),
        ]


class LibroIngElectrica(models.Model):
    titulo = models.CharField(max_length=300)
    autor = models.CharField(max_length=200)
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='libros_ing'
    )
    anio = models.IntegerField(validators=[validar_anio])
    descripcion = models.TextField(blank=True)
    archivo = models.FileField(
        upload_to='libros_ing/',
        validators=[validar_extension_pdf]
    )
    recomendacion = models.IntegerField(default=5, validators=[validar_recomendacion])
    paginas = models.IntegerField(default=0, help_text='Número de hojas')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = 'Libro Ing. Eléctrica'
        verbose_name_plural = 'Libros Ing. Eléctrica'