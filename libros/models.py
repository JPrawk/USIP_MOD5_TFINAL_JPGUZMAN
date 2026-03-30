from django.db import models
from django.core.exceptions import ValidationError
import datetime

def validar_extension_archivo(archivo):
    ext = archivo.name.split('.')[-1].lower()
    if ext not in ['pdf', 'epub']:
        raise ValidationError('Solo se permiten archivos PDF o EPUB.')

def validar_extension_portada(archivo):
    ext = archivo.name.split('.')[-1].lower()
    if ext not in ['jpg', 'jpeg', 'png']:
        raise ValidationError('Solo se permiten imágenes JPG o PNG.')

def validar_anio_publicacion(anio):
    anio_actual = datetime.date.today().year
    if anio > anio_actual:
        raise ValidationError(f'El año no puede ser mayor a {anio_actual}.')
    if anio < 1000:
        raise ValidationError('El año no es válido.')

class Genero(models.Model):
    GENEROS_PRINCIPALES = [
        ('novela', 'Novela'),
        ('matematicas', 'Matemáticas'),
        ('fisica', 'Física'),
        ('quimica', 'Química'),
        ('ajedrez', 'Ajedrez'),
        ('ing_electrica', 'Ingeniería Eléctrica'),
    ]
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50, choices=GENEROS_PRINCIPALES)
    padre = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subgeneros')
    descripcion = models.TextField(blank=True)

    def __str__(self):
        if self.padre:
            return f'{self.padre.nombre} > {self.nombre}'
        return self.nombre

    class Meta:
        verbose_name_plural = 'Géneros'

class Autor(models.Model):
    nombre = models.CharField(max_length=200)
    nacionalidad = models.CharField(max_length=100, blank=True)
    biografia = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

class Libro(models.Model):
    titulo = models.CharField(max_length=300)
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE, related_name='libros')
    genero = models.ForeignKey(Genero, on_delete=models.SET_NULL, null=True, related_name='libros')
    anio_publicacion = models.IntegerField(validators=[validar_anio_publicacion])
    descripcion = models.TextField(blank=True)
    portada = models.ImageField(upload_to='portadas/', blank=True, null=True, validators=[validar_extension_portada])

    def __str__(self):
        return self.titulo

class ArchivoLibro(models.Model):
    TIPO_CHOICES = [
        ('pdf', 'PDF'),
        ('epub', 'EPUB'),
        ('metadatos', 'Metadatos EPUB'),
    ]
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE, related_name='archivos')
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    archivo = models.FileField(upload_to='archivos/', validators=[validar_extension_archivo])

    def __str__(self):
        return f'{self.libro.titulo} - {self.tipo.upper()}'

    class Meta:
        verbose_name_plural = 'Archivos de libros'