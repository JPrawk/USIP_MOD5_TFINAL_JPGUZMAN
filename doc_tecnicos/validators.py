from django.core.exceptions import ValidationError
import datetime


def validar_recomendacion(valor):
    if valor < 1 or valor > 10:
        raise ValidationError('La recomendación debe ser entre 1 y 10.')


def validar_extension_pdf(archivo):
    ext = archivo.name.split('.')[-1].lower()
    if ext != 'pdf':
        raise ValidationError('Solo se permiten archivos PDF.')


def validar_anio(anio):
    anio_actual = datetime.date.today().year
    if anio > anio_actual:
        raise ValidationError(f'El año no puede ser mayor a {anio_actual}.')
    if anio < 1900:
        raise ValidationError('El año no es válido.')