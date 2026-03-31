from django.db import models
from .validators import (
    validar_recomendacion,
    validar_extension_archivo,
    validar_extension_portada,
    validar_anio_publicacion,
)


class TipoArchivo(models.TextChoices):
    PDF = 'pdf', 'PDF'
    EPUB = 'epub', 'EPUB'
    METADATOS = 'metadatos', 'Metadatos EPUB'


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
        permissions = [
            ('ver_reporte_libros', 'Ver reporte de libros'),
        ]


class Genero(models.Model):
    class TipoGenero(models.TextChoices):
        NOVELA = 'novela', 'Novela'
        MATEMATICAS = 'matematicas', 'Matemáticas'
        FISICA = 'fisica', 'Física'
        QUIMICA = 'quimica', 'Química'
        AJEDREZ = 'ajedrez', 'Ajedrez'
        ING_ELECTRICA = 'ing_electrica', 'Ingeniería Eléctrica'
        POLITICA = 'politica', 'Política'
        HISTORIA = 'historia', 'Historia'
        CIENCIA = 'ciencia', 'Ciencia'
        OTROS = 'otros', 'Otros'

    nombre = models.CharField(max_length=100)
    tipo = models.CharField(
        max_length=50,
        choices=TipoGenero.choices,
        default=TipoGenero.OTROS
    )
    padre = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='subgeneros'
    )
    descripcion = models.TextField(blank=True)
    recomendacion = models.IntegerField(default=5, validators=[validar_recomendacion])
    paginas = models.IntegerField(default=0, help_text='Número de hojas')

    def __str__(self):
        if self.padre:
            return f'{self.padre.nombre} > {self.nombre}'
        return self.nombre

    class Meta:
        verbose_name = 'Género'
        verbose_name_plural = 'Géneros'


class Autor(models.Model):
    nombre = models.CharField(max_length=200)
    nacionalidad = models.CharField(max_length=100, blank=True)
    biografia = models.TextField(blank=True)
    recomendacion = models.IntegerField(default=5, validators=[validar_recomendacion])

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Autor'
        verbose_name_plural = 'Autores'


class Libro(models.Model):
    titulo = models.CharField(max_length=300)
    autor = models.ForeignKey(
        Autor,
        on_delete=models.CASCADE,
        related_name='libros'
    )
    genero = models.ForeignKey(
        Genero,
        on_delete=models.SET_NULL,
        null=True,
        related_name='libros'
    )
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='libros'
    )
    anio_publicacion = models.IntegerField(validators=[validar_anio_publicacion])
    descripcion = models.TextField(blank=True)
    portada = models.ImageField(
        upload_to='portadas/',
        blank=True,
        null=True,
        validators=[validar_extension_portada]
    )
    recomendacion = models.IntegerField(default=5, validators=[validar_recomendacion])
    paginas = models.IntegerField(default=0, help_text='Número de hojas')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = 'Libro'
        verbose_name_plural = 'Libros'
        permissions = [
            ('descargar_libro', 'Descargar libro'),
        ]


class ArchivoLibro(models.Model):
    libro = models.ForeignKey(
        Libro,
        on_delete=models.CASCADE,
        related_name='archivos'
    )
    tipo = models.CharField(
        max_length=20,
        choices=TipoArchivo.choices,
        default=TipoArchivo.PDF
    )
    archivo = models.FileField(
        upload_to='archivos/',
        validators=[validar_extension_archivo]
    )
    descripcion = models.TextField(blank=True)
    recomendacion = models.IntegerField(default=5, validators=[validar_recomendacion])
    paginas = models.IntegerField(default=0, help_text='Número de hojas')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.libro.titulo} - {self.tipo.upper()}'

    class Meta:
        verbose_name = 'Tipo Formato'
        verbose_name_plural = 'Tipo Formato'