from django.db import models

from model_utils.models import TimeStampedModel
from app01.settings.local import NAME_HOST, PORT_LOCALHOST


class Pais(TimeStampedModel):
    pa_id = models.AutoField("Key", primary_key=True)
    pa_nombre = models.CharField("Nombre país", max_length=255)
    pa_codigo = models.IntegerField("Código area país", unique=True)

    def __int__(self):
        return self.pa_id

    def __str__(self):
        return "{n}".format(n=self.pa_nombre.title())

    def save(self, *args, **kwargs):
        # print "save cto"
        super(Pais, self).save(*args, **kwargs)

    class Meta:
        db_table = 'conf_pais'
        ordering = ['pa_id']

class Region(TimeStampedModel):
    re_id = models.AutoField("Key", primary_key=True)
    re_nombre = models.CharField("Nombre región", max_length=255)
    pais = models.ForeignKey(Pais, verbose_name="País", blank=True, null=True, on_delete=models.PROTECT,
                             db_column="re_pais")
    re_numeroregion = models.CharField("Sigla de región", blank=True, null=True, max_length=5)
    re_numero = models.IntegerField("Número de región", db_index=True)

    def __int__(self):
        return self.re_id

    def save(self, *args, **kwargs):
        # print "save cto"
        super(Region, self).save(*args, **kwargs)

    class Meta:
        db_table = 'conf_region'
        ordering = ['re_id']

class Comuna(TimeStampedModel):
    com_id = models.AutoField("Key", primary_key=True)
    com_nombre = models.CharField("Nombre comuna", max_length=255)
    com_numero = models.IntegerField("Numero comuna", default=0)
    region = models.ForeignKey(Region, verbose_name="Región", blank=True, null=True, on_delete=models.PROTECT,
                               db_column="com_region")

    def __int__(self):
        return self.com_id

    def save(self, *args, **kwargs):
        # print "save cto"
        super(Comuna, self).save(*args, **kwargs)

    class Meta:
        db_table = 'conf_comuna'
        ordering = ['com_id']

class Cliente(TimeStampedModel):
    OPCIONES = (
        ('S', 'SI'),
        ('N', 'NO'),
    )

    nombre_cliente = models.CharField('Nombre del cliente', max_length=120)
    rut_cliente = models.CharField('Rut del cliente', max_length=20)
    nombre_bd = models.CharField('Nombre base de datos', max_length=20)
    # url_cliente = models.TextField('URL cliente', blank=True, null=True)
    cli_link = models.CharField("Link base", max_length=255, default='')
    imagen_cliente = models.ImageField('Logo Cliente', blank=True, null=True, upload_to=None, height_field=None, width_field=None, max_length=None)
    favicon_cliente = models.ImageField('Favicon Cliente', blank=True, null=True, upload_to=None, height_field=None, width_field=None, max_length=None)
    cliente_activo = models.CharField("Cliente activo", max_length=1, choices=OPCIONES, default="S")
    fecha_ingreso = models.DateField("Fecha creación de la base")
    fecha_termino = models.DateField(verbose_name='Fecha termino de la base')
    cantidad_usuarios = models.IntegerField("Cantidad usuarios")
    nombre_representante = models.CharField("Nombre representante", max_length=75)
    rut_representante = models.CharField("Rut representante", max_length=20)
    correo_representante = models.CharField("Rut representante", max_length=100)
    telefono_representante = models.CharField("Teléfono representante", max_length=100)
    dirección_representante = models.CharField("Dirección representante", max_length=100)
    pais = models.ForeignKey(Pais, verbose_name="País", db_column="pais", null=True, blank=True, on_delete=models.PROTECT)
    region = models.ForeignKey(Region, verbose_name="Región", db_column="region", null=True, blank=True, on_delete=models.PROTECT)
    comuna = models.ForeignKey(Comuna, verbose_name="Comuna", db_column="comuna", null=True, blank=True, on_delete=models.PROTECT)
    emp_codpostal = models.CharField("Código postal", max_length=25, null=True, blank=True)

    ruta_directorio = models.CharField("Directorio cliente", max_length=255, null=True, blank=True)

    deleted = models.CharField('deleted', max_length=1, choices=OPCIONES, default='N', null=True, blank=True)

    def __str__(self):
        return str(self.id) + ' - ' + self.nombre_cliente

    def __create_url_client(self):
        isCliente = Cliente.objects.filter(rut_cliente = self.rut_cliente).exists()
        if not isCliente:
            return f"http://{self.nombre_bd}.{NAME_HOST}:{PORT_LOCALHOST}"
        return self.cli_link

    create_url_client = property(__create_url_client)

    def save(self, *args, **kwargs):
        self.cli_link = self.create_url_client.lower()
        self.nombre_bd = self.nombre_bd.lower()
        super(Cliente, self).save(*args, **kwargs)

    class Meta:
        db_table = 'conf_cliente'
        ordering = ['id']
        unique_together = ('rut_cliente',)

class ParametrosIndicadoresPrevisionales(TimeStampedModel):
    OPCIONES = (
        ('S', 'SI'),
        ('N', 'NO'),
    )

    pip_id = models.AutoField("Key", primary_key=True)
    pip_codigo = models.CharField("Código del parámetro", max_length=10)
    pip_descripcion = models.TextField("Descripción", max_length=255)
    pip_valor = models.CharField("Valor", max_length=50, null=True, blank=True, default=0)
    pip_rangoini = models.DecimalField("Desde $", max_digits=15, decimal_places=6, null=True, blank=True, default=0)
    pip_rangofin = models.DecimalField("Hasta $", max_digits=15, decimal_places=6, null=True, blank=True, default=0)
    pip_factor = models.CharField("Factor", max_length=50)
    pip_activo = models.CharField("Activo", max_length=1, choices=OPCIONES, default="S")

    def __int__(self):
        return self.pip_id

    def save(self, *args, **kwargs):
        super(ParametrosIndicadoresPrevisionales, self).save(*args, **kwargs)

    class Meta:
        db_table = "conf_parametros_indicadores_previsionales"
        ordering = ['pip_id']

class TablaGeneral(TimeStampedModel):
    OPCIONES = (
        ('S', 'SI'),
        ('N', 'NO'),
    )

    tg_id = models.AutoField("Key", primary_key=True)
    tg_nombretabla = models.CharField("nombre_tabla", max_length=150)
    tg_idelemento = models.CharField("elemento_id", null=True, blank=True, max_length=25)
    tg_descripcion = models.TextField("descripcion", null=True, blank=True)
    tg_activo = models.CharField("Activo", max_length=1, choices=OPCIONES, default="S")

    def __int__(self):
        return self.tg_id

    def save(self, *args, **kwargs):
        super(TablaGeneral, self).save(*args, **kwargs)

    class Meta:
        db_table = "conf_tabla_general"
        ordering = ['tg_id']