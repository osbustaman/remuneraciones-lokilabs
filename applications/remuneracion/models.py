from django.db import models
from model_utils.models import TimeStampedModel

# Create your models here.

class MonthlyPreviredData(TimeStampedModel):

    OPTIONS = (
        ('S', 'SI'),
        ('N', 'NO'),
    )

    dpm_id = models.AutoField("Key", primary_key=True)
    dpm_name = models.CharField("Nombre", max_length=255)
    dpm_shot_name = models.CharField("Nombre Corto", max_length=50, null=True, blank=True)
    dpm_month = models.IntegerField("mes")
    dpm_year = models.IntegerField("año")
    dpm_day = models.IntegerField("dia")
    dpm_dict = models.TextField("Diccionario de remuneraciones mensuales", null=True, blank=True)
    dpm_active = models.CharField(
        "activo", choices=OPTIONS, max_length=1, default="S")
    
    def __int__(self):
        return self.dpm_id

    def __str__(self):
        return f"{self.dpm_id} - {self.dpm_name}"

    def save(self, *args, **kwargs):
        super(MonthlyPreviredData, self).save(*args, **kwargs)

    class Meta:
        db_table = 'remu_monthly_previred_data'
        ordering = ['dpm_id']


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

    REMUNERATION_TYPE = (
        (0, ' --------- '),
        (1, 'Sueldo'),
        (2, 'Sobresueldo'),
        (3, 'Variable'),
        (4, 'Eventuales'),
        (5, 'Gratificación'),
        (6, 'Descuento')
    )

    conc_id = models.AutoField("Key", primary_key=True)
    conc_name = models.CharField("Nombre", max_length=255)
    conc_clasificationconcept = models.IntegerField("Clasificación concepto", choices=CLASSIFICATION)
    conc_typeconcept = models.IntegerField("Tipo concepto", choices=TYPE_CLASSIFICATION)
    conc_remuneration_type = models.IntegerField("Tipo de remuneración", choices=REMUNERATION_TYPE)
    conc_search_field = models.CharField("Campo de busqueda", null=True, blank=True, default='0', max_length=50, choices=SEARCH_FIELDS)
    conc_default = models.CharField(
        "Concepto por defecto", choices=OPTIONS, max_length=1, default="N")
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


class ConfigVariableRemunerations(TimeStampedModel):
    
    OPTIONS = (
        ('S', 'SI'),
        ('N', 'NO'),
    )

    TITLES = (
        (0, ' --------- '),
        (1, 'RENTAS TOPES IMPONIBLES'),
        (2, 'RENTAS MÍNIMAS IMPONIBLES'),
        (3, 'AHORRO PREVISIONAL VOLUNTARIO (APV)'),
        (4, 'DEPÓSITO CONVENIDO'),
    )

    TYPE_VARIABLE = (
        (0, ' --------- '),
        (1, 'PREVIRED'),
        (2, 'REMUNERACIONES'),
    )

    cvr_id = models.AutoField("Key", primary_key=True)
    cvr_name = models.CharField("Nombre variable", max_length=255)
    cvr_valueone = models.CharField("Valor uno", max_length=255, null=True, blank=True)
    cvr_valuetwo = models.CharField("Valor dos", max_length=255, null=True, blank=True)

    cvr_vartype = models.IntegerField(
        "Tipo de variable", choices=TYPE_VARIABLE, default=0)

    cvr_active = models.CharField(
        "Variable activa", choices=OPTIONS, max_length=1, default="S")

    def __int__(self):
        return self.cvr_id

    def __str__(self):
        return f"{self.cvr_id} - {self.cvr_name}"

    def save(self, *args, **kwargs):
        super(ConfigVariableRemunerations, self).save(*args, **kwargs)

    class Meta:
        db_table = 'remu_config_variable_remunerations'
        ordering = ['cvr_id']