from django.db import models
from applications.security.models import Rol
from model_utils.models import TimeStampedModel
from django.contrib.auth.models import User
from applications.base.models import Comuna, Pais, Region, TablaGeneral

from applications.empresa.models import (
    Afp,
    Apv, Banco,
    CajasCompensacion, Cargo, CentroCosto, Empresa, Salud, Sucursal, TipoContrato
)
from applications.remuneracion.models import Concept

# Create your models here.


class UsuarioTipoContrato(TimeStampedModel):
    OPCIONES = (
        (1, 'SI'),
        (0, 'NO'),
    )

    utc_id = models.AutoField("Key", primary_key=True)
    user = models.ForeignKey(User, verbose_name="Usuario",
                             db_column="utc_usuario_id", on_delete=models.PROTECT)
    tipoContrato = models.ForeignKey(
        TipoContrato, verbose_name="Usuario", db_column="utc_tipo_contrato_id", on_delete=models.PROTECT)
    utc_contratoprincipal = models.IntegerField(
        "Contrato principal", choices=OPCIONES, null=True, blank=True, default=0)

    def __int__(self):
        return self.cc_id

    def save(self, *args, **kwargs):
        super(UsuarioTipoContrato, self).save(*args, **kwargs)

    class Meta:
        db_table = "usu_tipo_contrato"
        ordering = ['utc_id']


class Colaborador(TimeStampedModel):

    OPCIONES = (
        (1, 'SI'),
        (0, 'NO'),
    )

    SEXO = (
        ('M', 'MASCULINO'),
        ('F', 'FEMENINO'),
    )

    ESTADO_CIVIL = (
        (1, 'Solter@'),
        (2, 'Casad@'),
        (3, 'Divorsiad@'),
        (4, 'Viud@'),
    )

    TIPO_USUARIO = (
        (1, 'Super-Admin'),
        (2, 'Recursos Humanos'),
        (3, 'Recursos Humanos Administrador'),
        (4, 'Jefatura'),
        (5, 'Colaborador'),
    )

    FORMA_PAGO = (
        ('', '---------'),
        (1, 'Efectivo'),
        (2, 'Cheque'),
        (3, 'Vale vista'),
        (4, 'Depósito directo'),
    )

    TIPO_CUENTA_BANCARIA = (
        (0, '---------'),
        (1, 'CUENTA VISTA'),
        (2, 'CUENTA DE AHORRO'),
        (3, 'CUENTA BANCARIA PARA ESTUDIANTE'),
        (4, 'CUENTA CHEQUERA ELECTRÓNICA'),
        (5, 'CUENTA RUT'),
        (6, 'CUENTA BANCARIA PARA EXTRANJEROS'),
        (7, 'CUENTA CORRIENTE')
    )

    TIPO_ESTUDIOS = (
        (1, 'ENSEÑANZA MEDIA'),
        (2, 'ESTUDIOS SUPERIORES (CFT)'),
        (3, 'ESTUDIOS UNIVERSITARIOS'),
    )

    ESTADO_ESTUDIOS = (
        (1, 'COMPLETO'),
        (2, 'INCOMPLETO'),
    )

    col_id = models.AutoField("Key", primary_key=True)
    user = models.ForeignKey(User, verbose_name="Colaborador",
                             db_column="ue_usuario", null=True, blank=True, on_delete=models.PROTECT)
    col_extranjero = models.IntegerField(
        "Extranjero", choices=OPCIONES, default=0)
    col_nacionalidad = models.CharField(
        "Nacionalidad", max_length=100, blank=True, null=True, default='chilen@')
    col_rut = models.CharField("Rut", max_length=100)
    col_sexo = models.CharField("Sexo", max_length=1, choices=SEXO)
    col_fechanacimiento = models.DateField("Fecha de nacimiento")
    col_estadocivil = models.IntegerField("Estado civil", choices=ESTADO_CIVIL)
    col_direccion = models.TextField("Dirección")
    pais = models.ForeignKey(Pais, verbose_name="País",
                             db_column="usu_pais", on_delete=models.PROTECT)
    region = models.ForeignKey(
        Region, verbose_name="Región", db_column="usu_region", on_delete=models.PROTECT)
    comuna = models.ForeignKey(
        Comuna, verbose_name="Comuna", db_column="usu_comuna", on_delete=models.PROTECT)
    col_latitude = models.CharField("Latitud", max_length=255, null=True, blank=True)
    col_longitude = models.CharField("Longitud", max_length=255, null=True, blank=True)


    #col_tipousuario = models.IntegerField(
    #    "Tipo usuario", choices=TIPO_USUARIO, null=True, blank=True)
    
    col_tipousuario = models.ForeignKey(Rol, verbose_name="Rol", db_column="col_tipousuario",
                              null=True, blank=True, on_delete=models.PROTECT)

    col_estudios = models.IntegerField(
        "Tipo estudios", choices=TIPO_ESTUDIOS, default=1)
    col_estadoestudios = models.IntegerField(
        "Estado estudios", choices=ESTADO_ESTUDIOS, default=1)
    col_titulo = models.CharField(
        "Titulo", max_length=100, null=True, blank=True)
    col_formapago = models.IntegerField(
        "Forma de pago", choices=FORMA_PAGO, null=True, blank=True)
    banco = models.ForeignKey(Banco, verbose_name="Banco", db_column="ue_banco",
                              null=True, blank=True, on_delete=models.PROTECT)
    col_tipocuenta = models.IntegerField(
        "tipo de cuenta", choices=TIPO_CUENTA_BANCARIA, null=True, blank=True)
    col_cuentabancaria = models.CharField(
        "Cuenta bancaria", max_length=50, null=True, blank=True)
    col_usuarioactivo = models.IntegerField(
        "Usuario activo", choices=OPCIONES, default=1)
    col_licenciaconducir = models.IntegerField(
        "Licencia de conducir", choices=OPCIONES, null=True, blank=True)
    col_tipolicencia = models.CharField(
        "Tipo de licencia", max_length=2, null=True, blank=True)
    col_fotousuario = models.TextField("Foto usuario", null=True, blank=True)
    col_activo = models.IntegerField(
        "Colaborador Activo", choices=OPCIONES, default=1)

    def __int__(self):
        return self.col_id
    
    def __str__(self):
        return f"{self.col_id} - {self.col_rut}"

    def save(self, *args, **kwargs):
        super(Colaborador, self).save(*args, **kwargs)

    class Meta:
        db_table = "usu_colaborador"
        ordering = ['col_id']


class UsuarioEmpresa(TimeStampedModel):
    TIPO_TRABAJADOR = (
        (0, '[seleccione]'),
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
        ('', '[seleccione]'),
        ('PI', 'Plazo Indefinido'),
        ('PF', 'Plazo Fijo'),
        ('PI11', 'Plazo Indefinido 11 años o más'),
        ('TCP', 'Trabajador de Casa Particular'),
    )

    FAMILY_ALLOWANCE_SECTION = (
        (0, '---------'),
        (1, 'A'),
        (2, 'B'),
        (3, 'C'),
        (4, 'D'),
    )

    ESTATE_JOB = (
        (0, '[seleccione]'),
        (1, 'Vigente'),
        (2, 'Desvinculado')
    )

    CONTRIBUTION_TYPE = (
        (0, '---------'),
        (1, 'PESOS ($)'),
        (2, 'PORCENTAJE (%)'),
        (3, 'UNIDAD DE FOMENTO (UF)'),
    )

    TAX_REGIME = (
        (0, '---------'),
        (1, 'APV Regimen A'),
        (2, 'APV Regimen B'),
        (3, 'Depósitos Convenidos(**)'),
    )

    SHAPE = (
        (0, '---------'),
        (1, 'DIRECTA'),
        (2, 'INDIRECTA'),
    )

    WORKER_SECTOR = (
        (0, '[seleccione]'),
        (1, 'Público'),
        (2, 'Privado'),
    )

    ALL_DAYS = (
        ('Lunes', 'Lunes'),
        ('Martes', 'Martes'),
        ('Miércoles', 'Miércoles'),
        ('Jueves', 'Jueves'),
        ('Viernes', 'Viernes'),
        ('Sábado', 'Sábado'),
        ('Domingo', 'Domingo'),
    )

    ue_id = models.AutoField("Key", primary_key=True)
    user = models.ForeignKey(User, verbose_name="Usuario",
                            db_column="ue_usuario", on_delete=models.PROTECT)
    empresa = models.ForeignKey(
        Empresa, verbose_name="Empresa", db_column="ue_empresa", on_delete=models.PROTECT)
    cargo = models.ForeignKey(
        Cargo, verbose_name="Cargo", db_column="ue_cargo", on_delete=models.PROTECT, null=True, blank=True, related_name="usuarios_empresa_cargo")
    centrocosto = models.ForeignKey(
        CentroCosto, verbose_name="CentroDecosto ", db_column="ue_contro_costo", on_delete=models.PROTECT, null=True, blank=True)
    sucursal = models.ForeignKey(
        Sucursal, verbose_name="Sucursal", db_column="ue_sucursal", on_delete=models.PROTECT, null=True, blank=True)
    working_day = models.ForeignKey(
        TablaGeneral, verbose_name="TablaGeneral", db_column="ue_working_day", on_delete=models.PROTECT, null=True, blank=True, related_name="usuarios_empresa_working_day")

    # DATOS LABORALES
    ue_estate = models.IntegerField(
        "Estado de trabajador", choices=ESTATE_JOB, null=True, blank=True)
    ue_tipotrabajdor = models.IntegerField(
        "Tipo de trabajador", choices=TIPO_TRABAJADOR, null=True, blank=True)
    ue_tipocontrato = models.CharField(
        "Tipo de contrato", choices=TIPO_CONTRATO, max_length=5, null=True, blank=True, default=None)
    ue_fechacontratacion = models.DateField(
        "Fecha de contratacion del usuario", null=True, blank=True)
    ue_fecharenovacioncontrato = models.DateField(
        "Fecha primer contrato", null=True, blank=True)
    ue_horassemanales = models.IntegerField(
        "Horas trabajadas", null=True, blank=True, default=45)
    ue_agreedworkdays = models.CharField(
        "Dias de trabajo pactados", null=True, blank=True, max_length=255)
    ue_asignacionfamiliar = models.CharField(
        "Asignación familiar", choices=OPCIONES, max_length=1, null=True, blank=True, default="N")
    
    ue_family_allowance_section = models.IntegerField(
        "Asignación familiar", choices=FAMILY_ALLOWANCE_SECTION, null=True, blank=True)
    ue_cargasfamiliares = models.IntegerField(
        "Cargas familiares", null=True, blank=True, default=0)
    ue_montoasignacionfamiliar = models.DecimalField(
        "Monto asignación familiar", max_digits=15, decimal_places=2, null=True, blank=True, default=0)
    ue_sueldobase = models.DecimalField(
        "Sueldo base", max_digits=15, decimal_places=6, null=True, blank=True, default=0)
    ue_gratificacion = models.CharField(
        "Tiene gratificación", choices=OPCIONES, max_length=1, null=True, blank=True)
    ue_tipogratificacion = models.CharField(
        "Tipo de gratificación", choices=TIPO_GRATIFICACION, max_length=1, null=True, blank=True)
    ue_comiciones = models.CharField(
        "Tiene comociones", choices=OPCIONES, max_length=1, null=True, blank=True)
    ue_porcentajecomicion = models.DecimalField(
        "Porcentaje comociones", max_digits=15, decimal_places=2, null=True, blank=True)
    ue_semanacorrida = models.CharField(
        "Tiene semana corrida", choices=OPCIONES, max_length=1, null=True, blank=True)
    
    ue_workersector = models.IntegerField(
        "Sector del trabajador", choices=WORKER_SECTOR, null=True, blank=True)
    
    # AFP
    afp = models.ForeignKey(Afp, verbose_name="AFP", db_column="ue_afp",
                            on_delete=models.PROTECT, null=True, blank=True)

    # Caja Compensacion
    caja_compensacion = models.ForeignKey(CajasCompensacion, verbose_name="CajasCompensacion",
                                          db_column="ue_caja_compensacion", on_delete=models.PROTECT, null=True, blank=True)

    # APV
    ue_tieneapv = models.CharField(
        "Tiene APV", choices=OPCIONES, max_length=1, default="N", null=True, blank=True)
    apv = models.ForeignKey(Apv, verbose_name="APV", db_column="us_apv",
                            on_delete=models.PROTECT, null=True, blank=True)
    ue_contributiontype = models.IntegerField(
        "Tipo de contribución", choices=CONTRIBUTION_TYPE, null=True, blank=True)
    ue_taxregime = models.IntegerField(
        "Régimen tributario", choices=TAX_REGIME, null=True, blank=True)
    ue_shape = models.IntegerField(
        "Forma del aporte", choices=SHAPE, null=True, blank=True)
    ue_apvamount = models.DecimalField(
        "Monto", max_digits=15, decimal_places=2, null=True, blank=True)
    ue_paymentperioddate = models.DateField(
        "Fecha periodo de pago", null=True, blank=True)

    # COTIZACIONES VOLUNTARIAS
    ue_tieneahorrovoluntario = models.CharField(
        "Tiene ahorro voluntario", choices=OPCIONES, max_length=1, default="N", null=True, blank=True)
    ue_cotizacionvoluntaria = models.DecimalField(
        "Cotización voluntaria", max_digits=15, decimal_places=2, null=True, blank=True)
    ue_ahorrovoluntario = models.DecimalField(
        "Ahorro Voluntario", max_digits=15, decimal_places=2, null=True, blank=True)

    # SALUD
    salud = models.ForeignKey(Salud, verbose_name="Salud", db_column="ue_salud",
                              on_delete=models.PROTECT, null=True, blank=True)
    ue_ufisapre = models.FloatField(
        "Valor en UF isapre", null=True, blank=True, default=0)
    ue_funisapre = models.CharField(
        "Fun isapre", max_length=100, null=True, blank=True)
    ue_cotizacion = models.FloatField(
        "Cotizacion fonasa/isapre", null=True, blank=True, default=0)

    # SEGURO DE DESEMPLEO
    ue_segurodesempleo = models.CharField(
        "Seguro de desmpleo", max_length=1, choices=OPCIONES, null=True, blank=True)
    ue_porempleado = models.FloatField(
        "porcentaje por empleado", null=True, blank=True, default=0)
    ue_porempleador = models.FloatField(
        "porcentaje por empleador", null=True, blank=True, default=0)
    ue_trabajopesado = models.CharField(
        "Trabajo pesado", choices=OPCIONES, max_length=1, default="N", null=True, blank=True)

    # ENTREGA DE EQUIPOS SEGURIDAD Y OTROS
    ue_entregaequiposeguridad = models.CharField(
        "Entrega equipos de seguridad y otros", max_length=1, choices=OPCIONES, null=True, blank=True)
    ue_descripcionentrega = models.TextField(
        "Descpricion de la entrega de equipos y seguridad", default="N", null=True, blank=True)

    # TERMINO RELACION LABORAL
    ue_fechanotificacioncartaaviso = models.DateField(
        "Fecha de notificacion carta aviso", null=True, blank=True)
    ue_fechatermino = models.DateField(
        "Fecha de termino relacion laboral", null=True, blank=True, default=None)
    ue_cuasal = models.ForeignKey(TablaGeneral, verbose_name="TablaGeneral",
                                db_column="ue_causal", on_delete=models.PROTECT, null=True, blank=True)
    ue_fundamento = models.TextField("Fundamento", null=True, blank=True)
    ue_tiponoticacion = models.CharField(
        "Tipo de notificacion", choices=NOTIFICACION, max_length=1, null=True, blank=True)

    def __int__(self):
        return self.ue_id

    def __str__(self):
        return f"{self.ue_id} - {self.user.first_name} {self.user.last_name}"

    def save(self, *args, **kwargs):
        # print "save cto"
        super(UsuarioEmpresa, self).save(*args, **kwargs)

    class Meta:
        db_table = 'usu_usuario_empresa'
        ordering = ['ue_id']


class Contact(TimeStampedModel):
    TYPE = (
        (1, 'Email Personal'),
        (2, 'Email Corporativo'),
        (3, 'Teléfono Movil'),
        (4, 'Teléfono Fijo'),
        (5, 'Teléfono Familiar'),
        (6, 'Email Familiar'),
    )

    OPCIONES = (
        ('S', 'SI'),
        ('N', 'NO'),
    )

    con_id = models.AutoField("Key", primary_key=True)
    con_contact_type = models.IntegerField(
        "Tipo de contacto", choices=TYPE, default=2)
    con_mail_contact = models.CharField(
        "Correo de contacto", max_length=120, null=True, blank=True)
    con_phone_contact = models.CharField(
        "Teléfono de contacto", max_length=120, null=True, blank=True)
    cont_name_contact = models.CharField("Nombre del contacto", max_length=150)
    user = models.ForeignKey(User, verbose_name="Usuario",
                             db_column="con_user", on_delete=models.PROTECT)
    con_actiove = models.CharField(
        "Contacto activo", choices=OPCIONES, max_length=1, default="S")

    def __int__(self):
        return self.con_id

    def save(self, *args, **kwargs):
        super(Contact, self).save(*args, **kwargs)

    class Meta:
        db_table = 'usu_contact'
        ordering = ['con_id']


class ConceptUser(TimeStampedModel):

    REMUNERATION_TYPE = (
        (1, 'Orinarias'),
        (2, 'Extraordinarias'),
        (3, 'Especiales'),
    )

    cu_id = models.AutoField("Key", primary_key=True)
    user = models.ForeignKey(User, verbose_name="Usuario",
                             db_column="cu_usuario_id", on_delete=models.PROTECT)
    concept = models.ForeignKey(
        Concept, verbose_name="Concept", db_column="cu_concept_id", on_delete=models.PROTECT)
    cu_typeremuneration = models.IntegerField("Fórmula", choices=REMUNERATION_TYPE, null=True, blank=True)
    cu_formula = models.FloatField("Fórmula", null=True, blank=True)
    cu_value = models.FloatField("Valor", null=True, blank=True, default=0)
    cu_search_field = models.CharField("Campo de busqueda", null=True, blank=True, default=0, max_length=50)
    cu_description = models.CharField(
        "Descripción", max_length=150, null=True, blank=True)

    def __int__(self):
        return self.cu_id

    def __str__(self):
        return f"{self.cu_id} - {self.user.username} - {self.concept.conc_id}"

    def save(self, *args, **kwargs):
        super(ConceptUser, self).save(*args, **kwargs)

    class Meta:
        db_table = 'usu_concept_user'
        ordering = ['cu_id']


class FamilyResponsibilities(TimeStampedModel):

    SEXO = (
        ('M', 'MASCULINO'),
        ('F', 'FEMENINO'),
    )

    RELATIONSSHIP = (
        (0, '---------'),
        (1, 'Padre/Madre'),
        (2, 'Hij@'),
        (3, 'Herman@'),
        (4, 'Cónyuge'),
    )

    OPCIONES = (
        (1, 'SI'),
        (0, 'NO'),
    )
    
    fr_id = models.AutoField("Key", primary_key=True)
    user = models.ForeignKey(User, verbose_name="Colaborador",
                             db_column="fr_user", null=True, blank=True, on_delete=models.PROTECT)
    fr_rut = models.CharField("Rut", max_length=100)
    fr_sexo = models.CharField("Sexo", max_length=1, choices=SEXO)
    fr_relationship = models.IntegerField("Parentezco", choices=RELATIONSSHIP)
    fr_firstname = models.CharField("Nombres", max_length=150)
    fr_lastname = models.CharField("Apellidos", max_length=150)
    fr_fechanacimiento = models.DateField("Fecha de nacimiento")
    fr_activo = models.IntegerField(
        "Activo", choices=OPCIONES, default=1)

    def __int__(self):
        return self.col_id
    
    def __str__(self):
        return f"{self.fr_id} - {self.user.first_name} {self.user.last_name} - {self.fr_firstname} {self.fr_lastname}"

    def save(self, *args, **kwargs):
        super(FamilyResponsibilities, self).save(*args, **kwargs)

    class Meta:
        db_table = "usu_family_responsibilities"
        ordering = ['fr_id']