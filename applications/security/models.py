from django.db import models
from model_utils.models import TimeStampedModel

# Create your models here.
class Rol(TimeStampedModel):

    OPTIONS = (
        ('S', 'SI'),
        ('N', 'NO'),
    )

    NIVEL = (
        (0, 0),
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
        (6, 6),
        (7, 7),
        (8, 8),
    )

    rol_id = models.AutoField("Key", primary_key=True)
    rol_name = models.CharField("Nombre", max_length=70)
    rol_nivel = models.IntegerField("Nivel", choices=NIVEL)
    rol_client = models.CharField(
        "Vista para cliente", choices=OPTIONS, max_length=1, default="S")
    rol_active = models.CharField(
        "Rol activo", choices=OPTIONS, max_length=1, default="S")

    def __int__(self):
        return self.rol_id

    def __str__(self):
        return f"{self.rol_id} - {self.rol_name} - {self.rol_nivel}"

    def save(self, *args, **kwargs):
        super(Rol, self).save(*args, **kwargs)

    class Meta:
        db_table = 'sec_rol'
        ordering = ['rol_id']


class RoutesRol(TimeStampedModel):

    OPTIONS = (
        ('S', 'SI'),
        ('N', 'NO'),
    )

    rr_id = models.AutoField("Key", primary_key=True)
    rol = models.ForeignKey(Rol, verbose_name="Rol",
                             db_column="rr_rol", on_delete=models.PROTECT)
    rr_route = models.TextField("Ruta")
    rr_active = models.CharField(
        "Ruta activo", choices=OPTIONS, max_length=1, default="S")

    def __int__(self):
        return self.rr_id

    def __str__(self):
        return f"{self.rr_id} - {self.rr_route}"

    def save(self, *args, **kwargs):
        super(RoutesRol, self).save(*args, **kwargs)

    class Meta:
        db_table = 'sec_routes_rol'
        ordering = ['rr_id']