from django.core.exceptions import ValidationError
import datetime


def validar_recomendacion(valor):
    if valor < 1 or valor > 10:
        raise ValidationError('La recomendación debe ser entre 1 y 10.')


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