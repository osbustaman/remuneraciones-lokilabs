from django.db import models
from model_utils.models import TimeStampedModel

from django.contrib.auth.models import User

# Create your models here.


class MarkAttendance(TimeStampedModel):

    TYPE_ATTENDANCE = (
        (1, 'ENTRADA'),
        (2, 'SALIDA'),
    )

    TYPE_MARK = (
        (1, 'MOVIL'),
        (2, 'HUELLA'),
    )

    OPTIONS = (
        (1, 'SI'),
        (0, 'NO'),
    )

    ma_id = models.AutoField("Key", primary_key=True)
    user = models.ForeignKey(User, verbose_name="Colaborador",
                             db_column="ma_user", null=True, blank=True, on_delete=models.PROTECT)
    ma_typeattendance = models.IntegerField(
        "Tipo de marca", choices=TYPE_ATTENDANCE, null=True, blank=True)
    ma_latitude = models.TextField("Latitud")
    ma_longitude = models.TextField("Longitude")
    ma_place = models.TextField("Lugar de marca", null=True, blank=True)
    ma_modeldevice = models.CharField("Modelo celular", max_length=150, null=True, blank=True)
    ma_platformmark = models.CharField("Plataforma donde se marco", max_length=150, null=True, blank=True)
    ma_photo = models.TextField("Foto clolaborador", null=True, blank=True)
    ma_typemark = models.IntegerField(
        "Tipo marca", choices=TYPE_MARK, null=True, blank=True)
    ma_datemark = models.DateField("Fecha de marca")
    ma_active = models.IntegerField(
        "Marca activa", choices=OPTIONS, null=True, blank=True, default=1)

    def __int__(self):
        return self.ma_id

    def __str__(self):
        return f"{self.ma_id} - {self.user.username}"

    def save(self, *args, **kwargs):
        # print "save cto"
        super(MarkAttendance, self).save(*args, **kwargs)

    class Meta:
        db_table = 'mark_attendance'
        ordering = ['ma_id']