from django.db import models
from django.core.exceptions import ValidationError

def validar_extension_pdf(archivo):
    ext = archivo.name.split('.')[-1].lower()
    if ext != 'pdf':
        raise ValidationError('Solo se permiten archivos PDF.')

class OrganismoNorma(models.Model):
    ORGANISMOS = [
        ('IEC', 'IEC - International Electrotechnical Commission'),
        ('IEEE', 'IEEE - Institute of Electrical and Electronics Engineers'),
        ('NBR', 'NBR - Norma Brasileira'),
        ('CIGRE', 'CIGRE - Conseil International des Grands Réseaux Électriques'),
        ('ASTM', 'ASTM - American Society for Testing and Materials'),
        ('ASCE', 'ASCE - American Society of Civil Engineers'),
        ('NB', 'NB - Norma Boliviana'),
    ]
    nombre = models.CharField(max_length=10, choices=ORGANISMOS, unique=True)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Organismo de norma'
        verbose_name_plural = 'Organismos de normas'

class DocumentoTecnico(models.Model):
    titulo = models.CharField(max_length=300)
    codigo = models.CharField(max_length=100, unique=True)
    organismo = models.ForeignKey(OrganismoNorma, on_delete=models.CASCADE, related_name='documentos')
    anio = models.IntegerField()
    descripcion = models.TextField(blank=True)
    archivo = models.FileField(upload_to='doc_tecnicos/', validators=[validar_extension_pdf])

    def __str__(self):
        return f'{self.organismo.nombre} - {self.codigo}: {self.titulo}'

    class Meta:
        verbose_name = 'Documento técnico'
        verbose_name_plural = 'Documentos técnicos'