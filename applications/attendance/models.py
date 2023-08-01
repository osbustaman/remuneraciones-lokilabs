from django.db import models
from model_utils.models import TimeStampedModel

from django.contrib.auth.models import User

# Create your models here.


class MarkAttendance(TimeStampedModel):

    TYPE_ATTENDANCE = (
        (1, 'ENTRADA'),
        (2, 'SALIDA'),
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
    ma_location = models.TextField("Localización")
    ma_datemark = models.DateTimeField("Fecha y hora de marca")
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