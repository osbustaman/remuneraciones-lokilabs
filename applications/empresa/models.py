from django.db import models
#from model_utils.models import TimeStampedModel
from applications.base.models import Comuna, Pais, Region

# Create your models here.
class Banco(models.Model):
    OPCIONES = (
        ('S', 'SI'),
        ('N', 'NO'),
    )

    ban_id = models.AutoField("Key", primary_key=True)
    ban_nombre = models.CharField("Nombre del banco", max_length=150)
    ban_codigo = models.CharField("Código", max_length=10)
    ban_activo = models.CharField("Activo", max_length=1, choices=OPCIONES, default="S")

    def __int__(self):
        return self.ban_id

    def __str__(self):
        return "{n}-{cc}".format(n=self.ban_nombre, cc=self.ban_codigo)

    def save(self, *args, **kwargs):
        super(Banco, self).save(*args, **kwargs)

    class Meta:
        db_table = "usu_bancos"
        ordering = ['ban_id']

class Empresa(models.Model):
    OPCIONES = (
        ('S', 'SI'),
        ('N', 'NO'),
    )

    emp_id = models.AutoField("Key", primary_key=True)
    emp_codigo = models.CharField("Código de la empresa", max_length=150)
    emp_rut = models.CharField("Rut", max_length=25)
    emp_nombrerepresentante = models.CharField("Nombre representante", max_length=255, null=True, blank=True)
    emp_rutrepresentante = models.CharField("Rut representante", max_length=25)
    emp_isestatal = models.CharField("Es estatal", max_length=1, choices=OPCIONES, default="N")
    emp_razonsocial = models.CharField("Razón social", max_length=150)
    emp_giro = models.CharField("Giro", max_length=150)
    emp_direccion = models.TextField("Calle")
    emp_numero = models.IntegerField("N°")
    emp_piso = models.CharField("Piso", max_length=25, null=True, blank=True)
    emp_dptooficina = models.CharField("Departamento/oficina", max_length=25, null=True, blank=True)
    pais = models.ForeignKey(Pais, verbose_name="País", db_column="emp_pais", on_delete=models.PROTECT)
    region = models.ForeignKey(Region, verbose_name="Región", db_column="emp_region", on_delete=models.PROTECT)
    comuna = models.ForeignKey(Comuna, verbose_name="Comuna", db_column="emp_comuna", on_delete=models.PROTECT)
    emp_cospostal = models.CharField("Código postal", max_length=25, null=True, blank=True)
    emp_fonouno = models.CharField("Télefono 1", max_length=25)
    emp_mailuno = models.CharField("Email 1", max_length=150)
    emp_fonodos = models.CharField("Télefono 2", max_length=25, null=True, blank=True)
    emp_maildos = models.CharField("Email 2", max_length=150, null=True, blank=True)
    emp_fechaingreso = models.DateField(verbose_name='Fecha inicio de actividades', null=True, blank=True)
    emp_isholding = models.CharField("Es sub-empresa", max_length=1, choices=OPCIONES, default="S")
    emp_idempresamadre = models.ForeignKey('self', db_column="emp_idempresamadre", null=True, blank=True, default=None,
                                           on_delete=models.PROTECT)
    emp_activa = models.CharField("Empresa activa", max_length=1, choices=OPCIONES, default="S")
    emp_rutcontador = models.CharField("Rut contador", max_length=12, null=True, blank=True)
    emp_nombrecontador = models.CharField("Razón social", max_length=150, null=True, blank=True)
    emp_imagenempresa = models.TextField("Nombre imagen", null=True, blank=True, default='')
    emp_colorlogo = models.CharField("Color logo", max_length=10, null=True, blank=True, default='')


    def __int__(self):
        return self.emp_id

    def __str__(self):
        return self.emp_razonsocial


    def __generador_ruta_logo(self):
        rutaLogo = "{a}/{b}".format(a=self.emp_rutalogo, b=self.emp_nombreimagen)
        return rutaLogo

    emp_generadorrutalogo = property(__generador_ruta_logo)

    def save(self, *args, **kwargs):
        self.emp_razonsocial = self.emp_razonsocial.title()
        super(Empresa, self).save(*args, **kwargs)

    class Meta:
        db_table = 'emp_empresa'
        ordering = ['emp_id']

class Sucursal(models.Model):
    OPCIONES = (
        ('S', 'SI'),
        ('N', 'NO'),
    )

    suc_id = models.AutoField("Key", primary_key=True)
    suc_codigo = models.CharField("Código de la unidad", max_length=50, null=True, blank=True)
    suc_descripcion = models.CharField("Descripción de la unidad", max_length=255, null=True, blank=True)
    empresa = models.ForeignKey(Empresa, verbose_name='Empresa', db_column='suc_empresa', default=0,
                                on_delete=models.PROTECT)
    suc_direccion = models.CharField("Direccion de la unidad", max_length=255, default='')
    pais = models.ForeignKey(Pais, verbose_name="País", db_column="suc_pais", on_delete=models.PROTECT)
    region = models.ForeignKey(Region, verbose_name="Región", db_column="suc_region", on_delete=models.PROTECT)
    comuna = models.ForeignKey(Comuna, verbose_name="Comuna", db_column="suc_comuna", on_delete=models.PROTECT)
    suc_estado = models.CharField("Sucursal activa", max_length=1, choices=OPCIONES, default="S")

    def __int__(self):
        return self.suc_id

    def __str__(self):
        return self.suc_codigo

    def save(self, *args, **kwargs):
        # print "save cto"
        super(Sucursal, self).save(*args, **kwargs)

    class Meta:
        db_table = "emp_sucursal"

class Cargo(models.Model):

    OPCIONES = (
        ('S', 'SI'),
        ('N', 'NO'),
    )

    car_id = models.AutoField("Key", primary_key=True)
    car_nombre = models.CharField("Nombre cargo", max_length=255)
    car_activa = models.CharField("Cargo activa", max_length=1, choices=OPCIONES, default="S")
    empresa = models.ManyToManyField(Empresa)

    def __int__(self):
        return self.car_id

    def __str__(self):
        return "{n}".format(n=self.car_nombre.title())

    def save(self, *args, **kwargs):
        # print "save cto"
        super(Cargo, self).save(*args, **kwargs)

    class Meta:
        db_table = 'emp_cargo'
        ordering = ['car_id']

class GrupoCentroCosto(models.Model):
    OPCIONES = (
        ('S', 'SI'),
        ('N', 'NO'),
    )

    gcencost_id = models.AutoField("Key", primary_key=True)
    gcencost_nombre = models.CharField("Nombre", max_length=100)
    gcencost_codigo = models.CharField("Código", max_length=100)
    gcencost_activo = models.CharField("Activo", max_length=1, choices=OPCIONES, default="S")
    empresa = models.ForeignKey(Empresa, verbose_name="Empresa", db_column="gcencost_empresa", on_delete=models.PROTECT)

    def __int__(self):
        return self.gcencost_id

    def __str__(self):
        return "{n}".format(n=self.gcencost_nombre)

    def save(self, *args, **kwargs):
        super(GrupoCentroCosto, self).save(*args, **kwargs)

    class Meta:
        db_table = "emp_grupo_centro_costo"
        ordering = ['gcencost_id']

class CentroCosto(models.Model):
    OPCIONES = (
        ('S', 'SI'),
        ('N', 'NO'),
    )

    cencost_id = models.AutoField("Key", primary_key=True)
    grupocentrocosto = models.ForeignKey(GrupoCentroCosto, verbose_name="Grupo Centro costo",
                                         db_column="ec_grupocentrocosto", on_delete=models.PROTECT)
    cencost_nombre = models.CharField("Nombre", max_length=100)
    cencost_codigo = models.CharField("Código", max_length=100)
    cencost_activo = models.CharField("Activo", max_length=1, choices=OPCIONES, default="S")

    def __int__(self):
        return self.cencost_id

    def __str__(self):
        return "{n}".format(n=self.cencost_nombre)

    def save(self, *args, **kwargs):
        super(CentroCosto, self).save(*args, **kwargs)

    class Meta:
        db_table = "emp_centro_costo"
        ordering = ['cencost_id']

class CajasCompensacion(models.Model):
    cc_id = models.AutoField("Key", primary_key=True)
    cc_nombre = models.CharField("Nombre", max_length=100)
    cc_codigo = models.CharField("Código", max_length=100)

    def __int__(self):
        return self.cc_id

    def __str__(self):
        return "{n}".format(n=self.cc_nombre)

    def save(self, *args, **kwargs):
        super(CajasCompensacion, self).save(*args, **kwargs)

    class Meta:
        db_table = "emp_cajas_compensacion"
        ordering = ['cc_id']

class Salud(models.Model):
    TIPO = (
        ('F', 'FONASA'),
        ('I', 'ISAPRE'),
    )

    sa_id = models.AutoField("Key", primary_key=True)
    sa_nombre = models.CharField("Nombre", max_length=100)
    sa_codigo = models.CharField("Código", max_length=100)
    sa_tipo = models.CharField("Tipo", max_length=1, choices=TIPO, default='I')

    def __int__(self):
        return self.sa_id

    def __str__(self):
        return "{n}".format(n=self.sa_nombre)

    def __porcentaje_fonasa(self):
        if self.sa_tipo == 'F':
            return 7
        else:
            return 0

    porcentajeFonasa = property(__porcentaje_fonasa)

    def save(self, *args, **kwargs):
        super(Salud, self).save(*args, **kwargs)

    class Meta:
        db_table = "emp_salud"
        ordering = ['sa_id']

class Afp(models.Model):
    afp_id = models.AutoField("Key", primary_key=True)
    afp_codigoprevired = models.CharField("Código previred", max_length=100)
    afp_nombre = models.CharField("Nombre", max_length=100)
    afp_tasatrabajadordependiente = models.FloatField("Tasa traba. dependiente", default=0)
    afp_sis = models.FloatField("Seguro de Invalidez y Sobrevivencia (SIS)", default=0)
    afp_tasatrabajadorindependiente = models.FloatField("Tasa traba. independiente", default=0)

    def __int__(self):
        return self.afp_id

    def __str__(self):
        return "{n}".format(n=self.afp_nombre)

    def save(self, *args, **kwargs):
        super(Afp, self).save(*args, **kwargs)

    class Meta:
        db_table = "emp_afp"
        ordering = ['afp_id']

class TipoContrato(models.Model):
    tc_id = models.AutoField("Key", primary_key=True)
    tc_codcontrato = models.CharField("Codifo contrato", max_length=25)
    tc_nombrecontrato = models.CharField("Nombre contrato", max_length=100)
    cc_contrato = models.TextField("texto del contrato")

    def __int__(self):
        return self.tc_id

    def __str__(self):
        return "{n}".format(n=self.tc_nombrecontrato)

    def save(self, *args, **kwargs):
        super(TipoContrato, self).save(*args, **kwargs)

    class Meta:
        db_table = "emp_tipo_contrato"
        ordering = ['tc_id']
