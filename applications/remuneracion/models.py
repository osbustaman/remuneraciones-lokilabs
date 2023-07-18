from django.db import models
from model_utils.models import TimeStampedModel

# Create your models here.


class Concept(TimeStampedModel):
    TYPE = (
        (0, '---------'),
        (1, 'Haberes imponible'),
        (2, 'Haberes no imponibles'),
        (3, 'Descuento'),
    )

    OPTIONS = (
        ('S', 'SI'),
        ('N', 'NO'),
    )

    conc_id = models.AutoField("Key", primary_key=True)
    conc_name = models.CharField("Nombre", max_length=70)
    conc_typeconcept = models.IntegerField("Tipo concepto", choices=TYPE)
    conc_description = models.CharField("Descripción", max_length=150, null=True, blank=True)
    conc_active = models.CharField("Concepto activo", choices=OPTIONS, max_length=1, default="S")

    def __int__(self):
        return self.conc_id
    
    def __str__(self):
        return f"{self.conc_id} - {self.conc_name}"

    def save(self, *args, **kwargs):
        super(Concept, self).save(*args, **kwargs)

    class Meta:
        db_table = 'remu_concept'
        ordering = ['conc_id']