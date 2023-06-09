from django.db import models
#from model_utils.models import TimeStampedModel
from django.contrib.auth.models import User
from applications.base.models import Comuna, Pais, Region, TablaGeneral

from applications.empresa.models import (
    Afp
    , Banco
    , Cargo
    , CentroCosto
    , Empresa
    , Salud
    , Sucursal
    , TipoContrato
)

# Create your models here.

class UsuarioTipoContrato(models.Model):
    OPCIONES = (
        (1, 'SI'),
        (0, 'NO'),
    )

    utc_id = models.AutoField("Key", primary_key=True)
    user = models.ForeignKey(User, verbose_name="Usuario", db_column="utc_usuario_id", on_delete=models.PROTECT)
    tipoContrato = models.ForeignKey(TipoContrato, verbose_name="Usuario", db_column="utc_tipo_contrato_id", on_delete=models.PROTECT)
    utc_contratoprincipal = models.IntegerField("Contrato principal", choices=OPCIONES, null=True, blank=True, default=0)

    def __int__(self):
        return self.cc_id

    def save(self, *args, **kwargs):
        super(UsuarioTipoContrato, self).save(*args, **kwargs)

    class Meta:
        db_table = "usu_tipo_contrato"
        ordering = ['utc_id']

class Colaborador(models.Model):

    OPCIONES = (
        (1, 'SI'),
        (0, 'NO'),
    )

    SEXO = (
        ('M', 'MASCULINO'),
        ('F', 'FEMENINO'),
    )

    ESTADO_CIVIL = (
        (1, 'Soltero(a)'),
        (2, 'Casado(a)'),
        (3, 'Divorsiado(a)'),
        (4, 'Viudo(a)'),
    )

    TIPO_USUARIO = (
        (1, 'Super-Admin'),
        (2, 'Recursos Humanos'),
        (3, 'Recursos Humanos Administrador'),
        (4, 'Jefatura'),
        (5, 'Colaborador'),
    )

    FORMA_PAGO = (
        (1, 'Efectivo'),
        (2, 'Cheque'),
        (3, 'Depósito directo'),
    )

    TIPO_CUENTA_BANCARIA = (
        (1, 'CUENTA VISTA'),
        (2, 'CUENTA DE AHORRO'),
        (3, 'CUENTA BANCARIA PARA ESTUDIANTE'),
        (4, 'CUENTA CHEQUERA ELECTRÓNICA'),
        (5, 'CUENTA RUT'),
        (6, 'CUENTA BANCARIA PARA EXTRANJEROS')
    )

    col_id = models.AutoField("Key", primary_key=True)
    user = models.ForeignKey(User, verbose_name="Colaborador", db_column="ue_usuario", null=True, blank=True, on_delete=models.PROTECT)
    col_extranjero = models.IntegerField("Extranjero", choices=OPCIONES, default=0)
    col_rut = models.CharField("Rut", max_length=100)
    col_sexo = models.CharField("Sexo", max_length=1, choices=SEXO)
    col_fechanacimiento = models.DateField("Fecha de nacimiento")
    col_estadocivil = models.IntegerField("Estado civil", choices=ESTADO_CIVIL)
    col_direccion = models.TextField("Dirección")
    pais = models.ForeignKey(Pais, verbose_name="País", db_column="usu_pais", on_delete=models.PROTECT)
    region = models.ForeignKey(Region, verbose_name="Región", db_column="usu_region", on_delete=models.PROTECT)
    comuna = models.ForeignKey(Comuna, verbose_name="Comuna", db_column="usu_comuna", on_delete=models.PROTECT)
    col_tipousuario = models.IntegerField("Tipo usuario", choices=TIPO_USUARIO)
    col_profesion = models.CharField("Profesión", max_length=255, null=True, blank=True)
    col_titulo = models.CharField("Titulo", max_length=100, null=True, blank=True)
    col_formapago = models.IntegerField("Forma de pago", choices=FORMA_PAGO, null=True, blank=True)
    banco = models.ForeignKey(Banco, verbose_name="Banco", db_column="ue_banco", null=True, blank=True, on_delete=models.PROTECT)
    col_tipocuenta = models.IntegerField("tipo de cuenta", choices=TIPO_CUENTA_BANCARIA, null=True, blank=True)
    col_cuentabancaria = models.CharField("Cuenta bancaria", max_length=50, null=True, blank=True)
    col_usuarioactivo = models.IntegerField("Usuario activo", choices=OPCIONES, default=1)
    col_licenciaconducir = models.IntegerField("Licencia de conducir", choices=OPCIONES, null=True, blank=True)
    col_tipolicencia = models.CharField("Tipo de licencia", max_length=2, null=True, blank=True)
    col_fotousuario = models.TextField("Foto usuario", null=True, blank=True)

    def __int__(self):
        return self.col_id

    def save(self, *args, **kwargs):
        super(Colaborador, self).save(*args, **kwargs)

    class Meta:
        db_table = "usu_colaborador"
        ordering = ['col_id']

class UsuarioEmpresa(models.Model):
    TIPO_TRABAJADOR = (
        (1, 'Activo (no pensionado)'),
        (2, 'Pensionado y cotiza AFP'),
        (3, 'Pensionado y no cotiza AFP'),
        (4, 'Activo mayor de 65 años (nunca pensionado)'),
    )

    OPCIONES = (
        ('S', 'SI'),
        ('N', 'NO'),
    )

    NOTIFICACION = (
        ('E', 'Email'),
        ('C', 'Carta'),
    )

    TIPO_MONTO = (
        ('P', 'Porcentaje'),
        ('M', 'Monto'),
    )

    TIPO_GRATIFICACION = (
        ('A', 'Anual'),
        ('M', 'Mensual'),
    )

    TIPO_CONTRATO = (
        ('PI', 'Plazo Indefinido'),
        ('PF', 'Plazo Fijo'),
        ('PI11', 'Plazo Indefinido 11 años o más'),
        ('TCP', 'Trabajador de Casa Particular'),
    )

    ue_id = models.AutoField("Key", primary_key=True)
    user = models.ForeignKey(User, verbose_name="Usuario", db_column="ue_usuario", on_delete=models.PROTECT)
    empresa = models.ForeignKey(Empresa, verbose_name="Empresa", db_column="ue_empresa", on_delete=models.PROTECT)
    cargo = models.ForeignKey(Cargo, verbose_name="Cargo", db_column="ue_cargo", on_delete=models.PROTECT)
    centrocosto = models.ForeignKey(CentroCosto, verbose_name="Centro de costo ", db_column="ue_contro_costo", on_delete=models.PROTECT)
    sucursal = models.ForeignKey(Sucursal, verbose_name="Sucursal", db_column="ue_sucursal", on_delete=models.PROTECT)
    
    # DATOS LABORALES
    ue_tipotrabajdor = models.IntegerField("Tipo de trabajador", choices=TIPO_TRABAJADOR, null=True, blank=True)
    ue_tipocontrato = models.CharField("Tipo de contrato", choices=TIPO_CONTRATO, max_length=5, null=True, blank=True, default=None)
    ue_fechacontratacion = models.DateField("Fecha de contratacion del usuario", null=True, blank=True)
    ue_fecharenovacioncontrato = models.DateField("Fecha termino de contrato", null=True, blank=True)
    ue_horassemanales = models.IntegerField("Horas trabajadas", null=True, blank=True, default=45)
    ue_asignacionfamiliar = models.CharField("Asignación familiar", choices=OPCIONES, max_length=1, null=True, blank=True, default="N")
    ue_cargasfamiliares = models.IntegerField("Cargas familiares", null=True, blank=True, default=0)
    ue_montoasignacionfamiliar = models.DecimalField("Monto asignación familiar", max_digits=15, decimal_places=2, null=True, blank=True, default=0)
    ue_sueldobase = models.DecimalField("Sueldo base", max_digits=15, decimal_places=6, null=True, blank=True, default=0)
    ue_gratificacion = models.CharField("Tiene gratificación", choices=OPCIONES, max_length=1, null=True, blank=True)
    ue_tipogratificacion = models.CharField("Tipo de gratificación", choices=TIPO_GRATIFICACION, max_length=1, null=True, blank=True)
    ue_comiciones = models.CharField("Tiene comociones", choices=OPCIONES, max_length=1, null=True, blank=True)
    ue_porcentajecomicion = models.DecimalField("Porcentaje comociones", max_digits=15, decimal_places=2, null=True, blank=True)
    ue_semanacorrida = models.CharField("Tiene semana corrida", choices=OPCIONES, max_length=1, null=True, blank=True)
    
    # AFP
    afp = models.ForeignKey(Afp, verbose_name="AFP", db_column="ue_afp", on_delete=models.PROTECT, null=True, blank=True)
    ue_tieneapv = models.CharField("Tiene APV", choices=OPCIONES, max_length=1, default="N", null=True, blank=True)
    ue_tipomontoapv = models.CharField("Tipo de monto", choices=TIPO_MONTO, null=True, blank=True, max_length=1, default="M")
    afp_apv = models.ForeignKey(Afp, verbose_name='AFP APV', db_column='ue_afp_apv', related_name="afp_apv", null=True, blank=True, on_delete=models.PROTECT)
    ue_entidad_apv = models.CharField("Entidad APV", max_length=150, default="", null=True, blank=True)
    ue_cotizacionvoluntaria = models.DecimalField("Cotización voluntaria", max_digits=15, decimal_places=2, null=True, blank=True)
    ue_tieneahorrovoluntario = models.CharField("Tiene ahorro voluntario", choices=OPCIONES, max_length=1, default="N", null=True, blank=True)
    ue_ahorrovoluntario = models.DecimalField("Ahorro Voluntario", max_digits=15, decimal_places=2, null=True, blank=True)
    
    # SALUD
    salud = models.ForeignKey(Salud, verbose_name="Salud", db_column="ue_salud", on_delete=models.PROTECT, null=True, blank=True)
    ue_ufisapre = models.FloatField("Valor en UF isapre", null=True, blank=True, default=0)
    ue_funisapre = models.IntegerField("Fun isapre", null=True, blank=True, default=0)
    ue_cotizacion = models.FloatField("Cotizacion fonasa/isapre", null=True, blank=True, default=0)
    
    # SEGURO DE DESEMPLEO
    ue_segurodesempleo = models.CharField("Seguro de desmpleo", max_length=1, choices=OPCIONES, null=True, blank=True)
    ue_porempleado = models.FloatField("porcentaje por empleado", null=True, blank=True, default=0)
    ue_porempleador = models.FloatField("porcentaje por empleador", null=True, blank=True, default=0)
    ue_trabajopesado = models.CharField("Trabajo pesado", choices=OPCIONES, max_length=1, default="N", null=True, blank=True)

    # ENTREGA DE EQUIPOS SEGURIDAD Y OTROS
    ue_entregaequiposeguridad = models.CharField("Entrega equipos de seguridad y otros", max_length=1, choices=OPCIONES, null=True, blank=True)
    ue_descripcionentrega = models.TextField("Descpricion de la entrega de equipos y seguridad", default="N", null=True, blank=True)
    
    # TERMINO RELACION LABORAL
    ue_fechanotificacioncartaaviso = models.DateField("Fecha de notificacion carta aviso", null=True, blank=True)
    ue_fechatermino = models.DateField("Fecha de termino relacion laboral", null=True, blank=True, default=None)
    ue_cuasal = models.ForeignKey(TablaGeneral, verbose_name="TablaGeneral", db_column="ue_causal", on_delete=models.PROTECT, null=True, blank=True)
    ue_fundamento = models.TextField("Fundamento", null=True, blank=True)
    ue_tiponoticacion = models.CharField("Tipo de notificacion", choices=NOTIFICACION, max_length=1, null=True, blank=True)

    def __int__(self):
        return self.ue_id

    def __str__(self):
        return "{n}".format(n=self.ue_id)

    def save(self, *args, **kwargs):
        # print "save cto"
        super(UsuarioEmpresa, self).save(*args, **kwargs)

    class Meta:
        db_table = 'usu_usuario_empresa'
        ordering = ['ue_id']


class Haberes(models.Model):
    TIPO = (
        ('', '--- Seleccione ---'),
        ('HI', 'Haberes imponible'),
        ('HNI', 'Haberes no imponibles'),
        ('F', 'Finiquito'),
        ('D', 'Descuento'),
    )

    OPCIONES = (
        ('S', 'SI'),
        ('N', 'NO'),
    )

    hab_id = models.AutoField("Key", primary_key=True)
    hab_nombre = models.CharField("Nombre", max_length=70)
    hab_monto = models.DecimalField("Monto", max_digits=15, decimal_places=6)
    hab_tipo = models.CharField("Tipo haber", choices=TIPO, max_length=3, null=True, blank=True, default=None)
    user = models.ForeignKey(User, verbose_name="Usuario", db_column="hab_usuario", on_delete=models.PROTECT)
    hab_activo = models.CharField("Haber activo", choices=OPCIONES, max_length=1, default="S")

    def __int__(self):
        return self.hab_id

    def save(self, *args, **kwargs):
        super(Haberes, self).save(*args, **kwargs)

    class Meta:
        db_table = 'usu_haberessa'
        ordering = ['hab_id']
