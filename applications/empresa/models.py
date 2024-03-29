import datetime
from django.db import models
# from model_utils.models import TimeStampedModel
from applications.base.models import Comuna, Pais, Region

# Create your models here.


class CajasCompensacion(models.Model):

    OPCIONES = (
        ('S', 'SI'),
        ('N', 'NO'),
    )

    cc_id = models.AutoField("Key", primary_key=True)
    cc_nombre = models.CharField("Nombre", max_length=100)
    cc_codigo = models.CharField("Código", max_length=100)
    cc_rut = models.CharField("Rut", max_length=10)
    cc_activo = models.CharField(
        "Activo", max_length=1, choices=OPCIONES, default="S")

    def __int__(self):
        return self.cc_id

    def __str__(self):
        return "{n}".format(n=self.cc_nombre)

    def save(self, *args, **kwargs):
        super(CajasCompensacion, self).save(*args, **kwargs)

    class Meta:
        db_table = "emp_cajas_compensacion"
        ordering = ['cc_id']


class MutualSecurity(models.Model):

    OPTIONS = (
        ('S', 'SI'),
        ('N', 'NO'),
    )

    ms_id = models.AutoField("Key", primary_key=True)
    ms_name = models.CharField("Nombre", max_length=150)
    ms_rut = models.CharField("Rut", max_length=150)
    ms_codeprevired = models.CharField("Código Previred", max_length=3)
    ms_active = models.CharField(
        "Activo", max_length=1, choices=OPTIONS, default="S")

    def __int__(self):
        return self.ms_id

    def __str__(self):
        return f"{self.ms_id} - {self.ms_name}"

    def save(self, *args, **kwargs):
        super(MutualSecurity, self).save(*args, **kwargs)

    class Meta:
        db_table = "emp_mutual_security"
        ordering = ['ms_id']


class Banco(models.Model):
    OPCIONES = (
        ('S', 'SI'),
        ('N', 'NO'),
    )

    ban_id = models.AutoField("Key", primary_key=True)
    ban_nombre = models.CharField("Nombre del banco", max_length=150)
    ban_codigo = models.CharField("Código", max_length=10)
    ban_bankbranch = models.CharField(
        "Nombre Sucursal", max_length=120, null=True, blank=True)
    ban_activo = models.CharField(
        "Activo", max_length=1, choices=OPCIONES, default="S")

    def __int__(self):
        return self.ban_id

    def __str__(self):
        return f"{self.ban_id} - {self.ban_nombre}"

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

    BUSSINESS_SOCIAL_REASON = (
        (0, '( Seleccione )'),
        (1, 'Empresa Individual de Responsabilidad Limitada (E.I.R.L.)'),
        (2, 'Sociedad de Responsabilidad Limitada (S.R.L.)'),
        (3, 'Sociedad por Acciones (SpA)'),
        (4, 'Sociedad Anónima (S.A.)'),
        (5, 'Sociedad Anónima de Garantía Recíproca (S.A.G.R.)'),
    )


    emp_id = models.AutoField("Key", primary_key=True)
    emp_rut = models.CharField("Rut", max_length=25)
    emp_nombrerepresentante = models.CharField(
        "Nombre representante", max_length=255, null=True, blank=True)
    emp_rutrepresentante = models.CharField("Rut representante", max_length=25)
    emp_isestatal = models.CharField(
        "Es estatal", max_length=1, choices=OPCIONES, default="N")
    emp_namecompany = models.CharField("Nombre empresa", max_length=150)
    emp_razonsocial = models.IntegerField("Razón social", choices=BUSSINESS_SOCIAL_REASON, null=True, blank=True)
    emp_giro = models.CharField("Giro", max_length=150)
    emp_direccion = models.TextField("Calle")
    emp_numero = models.IntegerField("N°")
    emp_piso = models.CharField("Piso", max_length=25, null=True, blank=True)
    emp_dptooficina = models.CharField(
        "Departamento/oficina", max_length=25, null=True, blank=True)
    pais = models.ForeignKey(Pais, verbose_name="País",
                             db_column="emp_pais", on_delete=models.PROTECT)
    region = models.ForeignKey(
        Region, verbose_name="Región", db_column="emp_region", on_delete=models.PROTECT)
    comuna = models.ForeignKey(
        Comuna, verbose_name="Comuna", db_column="emp_comuna", on_delete=models.PROTECT)
    emp_latitude = models.CharField("Latitud", max_length=255, null=True, blank=True)
    emp_longitude = models.CharField("Longitud", max_length=255, null=True, blank=True)
    emp_cospostal = models.CharField(
        "Código postal", max_length=25, null=True, blank=True)
    emp_fonouno = models.CharField("Télefono 1", max_length=25)
    emp_mailuno = models.CharField("Email 1", max_length=150)
    emp_fonodos = models.CharField(
        "Télefono 2", max_length=25, null=True, blank=True)
    emp_maildos = models.CharField(
        "Email 2", max_length=150, null=True, blank=True)
    emp_fechaingreso = models.DateField(
        verbose_name='Fecha inicio de actividades', null=True, blank=True)
    emp_isholding = models.CharField(
        "Es sub-empresa", max_length=1, choices=OPCIONES, default="S")
    emp_idempresamadre = models.ForeignKey('self', db_column="emp_idempresamadre", null=True, blank=True, default=None,
                                           on_delete=models.PROTECT)
    emp_activa = models.CharField(
        "Empresa activa", max_length=1, choices=OPCIONES, default="S")
    emp_rutcontador = models.CharField(
        "Rut contador", max_length=12, null=True, blank=True)
    emp_nombrecontador = models.CharField(
        "Razón social", max_length=150, null=True, blank=True)
    emp_imagenempresa = models.ImageField(
        "Logo Empresa", help_text=" Formatos .jpg|.png|.gif|.jpeg", upload_to='imagen/logos/', null=True, blank=True)
    emp_colorlogo = models.CharField(
        "Color logo", max_length=10, null=True, blank=True, default='')
    mutualSecurity = models.ForeignKey(MutualSecurity, verbose_name="MutualSecurity",
                                       db_column="emp_mutualsecurity", on_delete=models.PROTECT, null=True, blank=True)
    cajasCompensacion = models.ForeignKey(CajasCompensacion, verbose_name="CajasCompensacion",
                                          db_column="emp_cajas_compensacion", on_delete=models.PROTECT, null=True, blank=True)

    def __int__(self):
        return self.emp_id

    def __str__(self):
        return f"{ self.emp_id } - { self.emp_namecompany }"
    
    def __generador_ruta_logo(self):
        rutaLogo = "{a}/{b}".format(a=self.emp_rutalogo,
                                    b=self.emp_nombreimagen)
        return rutaLogo

    emp_generadorrutalogo = property(__generador_ruta_logo)

    def __company_address(self):
        floor = ''
        if len(self.emp_piso) > 0 and len(self.emp_dptooficina) > 0:
            floor = f" piso {self.emp_piso}, oficina {self.emp_dptooficina}"

        return f"{self.emp_direccion} {self.emp_numero}{floor}, {self.region.re_nombre}, {self.comuna.com_nombre}"
    emp_company_address = property(__company_address)

    def save(self, *args, **kwargs):
        super(Empresa, self).save(*args, **kwargs)

    class Meta:
        db_table = 'emp_empresa'
        ordering = ['emp_id']


class Sucursal(models.Model):
    OPCIONES = (
        ('S', 'SI'),
        ('N', 'NO'),
    )


    MATRIX_HOUSE = (
        ('S', 'SI'),
        ('N', 'NO'),
    )

    suc_id = models.AutoField("Key", primary_key=True)
    suc_codigo = models.CharField(
        "Código de la unidad", max_length=50, null=True, blank=True)
    suc_descripcion = models.CharField(
        "Descripción de la unidad", max_length=255, null=True, blank=True)
    empresa = models.ForeignKey(Empresa, verbose_name='Empresa', db_column='suc_empresa', default=0,
                                on_delete=models.PROTECT)
    suc_direccion = models.CharField(
        "Direccion de la unidad", max_length=255, default='')
    pais = models.ForeignKey(Pais, verbose_name="País",
                             db_column="suc_pais", on_delete=models.PROTECT)
    region = models.ForeignKey(
        Region, verbose_name="Región", db_column="suc_region", on_delete=models.PROTECT)
    comuna = models.ForeignKey(
        Comuna, verbose_name="Comuna", db_column="suc_comuna", on_delete=models.PROTECT)
    suc_latitude = models.CharField("Latitud", max_length=255, null=True, blank=True)
    suc_longitude = models.CharField("Longitud", max_length=255, null=True, blank=True)
    suc_matrixhouse = models.CharField(
        "Es casa matriz", max_length=1, choices=OPCIONES, null=True, blank=True, default="N")
    suc_estado = models.CharField(
        "Sucursal activa", max_length=1, choices=OPCIONES, default="S")

    def __int__(self):
        return self.suc_id

    def __str__(self):
        return f"{self.suc_id} - {self.suc_descripcion}"

    def __code_generator(self):
        return f"SUC-{self.suc_id}"
    code_generator = property(__code_generator)

    def save(self, *args, **kwargs):
        self.suc_codigo = self.code_generator
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
    car_activa = models.CharField(
        "Cargo activa", max_length=1, choices=OPCIONES, default="S")
    empresa = models.ManyToManyField(Empresa)

    def __int__(self):
        return self.car_id

    def __str__(self):
        return f"{self.car_id} - {self.car_nombre}"

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
    gcencost_codigo = models.CharField(
        "Código", max_length=100, null=True, blank=True)
    gcencost_activo = models.CharField(
        "Activo", max_length=1, choices=OPCIONES, default="S")
    empresa = models.ForeignKey(Empresa, verbose_name="Empresa",
                                db_column="gcencost_empresa", on_delete=models.PROTECT)

    def __int__(self):
        return self.gcencost_id

    def __str__(self):
        return "{n}".format(n=self.gcencost_nombre)

    def __code_generator(self):
        return f"GCC-{self.gcencost_id}"
    code_generator = property(__code_generator)

    def save(self, *args, **kwargs):
        self.gcencost_codigo = self.code_generator
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
    cencost_codigo = models.CharField(
        "Código", max_length=100, null=True, blank=True)
    cencost_activo = models.CharField(
        "Activo", max_length=1, choices=OPCIONES, default="S")

    def __int__(self):
        return self.cencost_id

    def __str__(self):
        return f"{self.cencost_id} - {self.cencost_nombre}"

    def __code_generator(self):
        return f"CC-{self.cencost_id}"
    code_generator = property(__code_generator)

    def save(self, *args, **kwargs):
        self.cencost_codigo = self.code_generator
        super(CentroCosto, self).save(*args, **kwargs)

    class Meta:
        db_table = "emp_centro_costo"
        ordering = ['cencost_id']


class Salud(models.Model):
    TIPO = (
        ('F', 'FONASA'),
        ('I', 'ISAPRE'),
    )

    OPCIONES = (
        ('S', 'SI'),
        ('N', 'NO'),
    )

    sa_id = models.AutoField("Key", primary_key=True)
    sa_nombre = models.CharField("Nombre", max_length=100)
    sa_codigo = models.CharField("Código", max_length=100)
    sa_tipo = models.CharField("Tipo", max_length=1, choices=TIPO, default='I')
    sa_activo = models.CharField(
        "Activo", max_length=1, choices=OPCIONES, default="S")

    def __int__(self):
        return self.sa_id

    def __str__(self):
        return f"{self.sa_id} - {self.sa_nombre}"

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

    OPCIONES = (
        ('S', 'SI'),
        ('N', 'NO'),
    )
    
    afp_id = models.AutoField("Key", primary_key=True)
    afp_codigoprevired = models.CharField("Código previred", max_length=100, null=False, blank=True)
    afp_nombre = models.CharField("Nombre", max_length=100)
    afp_tasatrabajadordependiente = models.FloatField(
        "Tasa traba. dependiente", default=0)
    afp_sis = models.FloatField(
        "Seguro de Invalidez y Sobrevivencia (SIS)", default=0)
    afp_tasatrabajadorindependiente = models.FloatField(
        "Tasa traba. independiente", default=0)
    afp_activo = models.CharField(
        "Activo", max_length=1, choices=OPCIONES, default="S")

    def __int__(self):
        return self.afp_id

    def __str__(self):
        return f"{self.afp_codigoprevired} - {self.afp_nombre}"

    def save(self, *args, **kwargs):
        super(Afp, self).save(*args, **kwargs)

    class Meta:
        db_table = "emp_afp"
        ordering = ['afp_id']


class Apv(models.Model):

    OPCIONES = (
        ('S', 'SI'),
        ('N', 'NO'),
    )

    apv_id = models.AutoField("Key", primary_key=True)
    apv_codigoprevired = models.CharField("Código previred", max_length=100, null=True, blank=True)
    apv_nombre = models.CharField("Nombre", max_length=100)
    apv_nombrerazonsocial = models.CharField(
        "Nombre razón social", max_length=150, null=True, blank=True)
    apv_activo = models.CharField(
        "Activo", max_length=1, choices=OPCIONES, default="S")

    def __int__(self):
        return self.apv_id

    def __str__(self):
        return f"{self.apv_id} - {self.apv_nombre}"

    def save(self, *args, **kwargs):
        super(Apv, self).save(*args, **kwargs)

    class Meta:
        db_table = "emp_apv"
        ordering = ['apv_id']


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
