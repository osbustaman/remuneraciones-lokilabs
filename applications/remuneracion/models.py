from django.db import models
from model_utils.models import TimeStampedModel

# Create your models here.


class Concept(TimeStampedModel):
    CLASSIFICATION = (
        (1, 'Haberes'),
        (2, 'Descuentos'),
    )

    TYPE_CLASSIFICATION = (
        (1, 'Imponible'),
        (2, 'No Imponible'),
        (3, 'Previsional'),
        (4, 'Judicial'),
        (5, 'Tributario'),
        (6, 'Acordado')
    )

    OPTIONS = (
        ('S', 'SI'),
        ('N', 'NO'),
    )

    SEARCH_FIELDS = (
        ('0', ' --------- '),
        ('ISAPRE', 'isapre'),
        ('FONASA', 'fonasa'),
        ('AFP', 'afp'),
    )

    conc_id = models.AutoField("Key", primary_key=True)
    conc_name = models.CharField("Nombre", max_length=255)
    conc_clasificationconcept = models.IntegerField("Clasificación concepto", choices=CLASSIFICATION)
    conc_typeconcept = models.IntegerField("Tipo concepto", choices=TYPE_CLASSIFICATION)
    conc_search_field = models.CharField("Campo de busqueda", null=True, blank=True, default='0', max_length=50, choices=SEARCH_FIELDS)

    conc_active = models.CharField(
        "Concepto activo", choices=OPTIONS, max_length=1, default="S")

    def __int__(self):
        return self.conc_id

    def __str__(self):
        return f"{self.conc_id} - {self.conc_name}"

    def save(self, *args, **kwargs):
        super(Concept, self).save(*args, **kwargs)

    class Meta:
        db_table = 'remu_concept'
        ordering = ['conc_id']
