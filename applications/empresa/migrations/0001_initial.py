# Generated by Django 3.2 on 2023-06-09 16:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Afp',
            fields=[
                ('afp_id', models.AutoField(primary_key=True, serialize=False, verbose_name='Key')),
                ('afp_codigoprevired', models.CharField(max_length=100, verbose_name='Código previred')),
                ('afp_nombre', models.CharField(max_length=100, verbose_name='Nombre')),
                ('afp_tasatrabajadordependiente', models.FloatField(default=0, verbose_name='Tasa traba. dependiente')),
                ('afp_sis', models.FloatField(default=0, verbose_name='Seguro de Invalidez y Sobrevivencia (SIS)')),
                ('afp_tasatrabajadorindependiente', models.FloatField(default=0, verbose_name='Tasa traba. independiente')),
            ],
            options={
                'db_table': 'emp_afp',
                'ordering': ['afp_id'],
            },
        ),
        migrations.CreateModel(
            name='Banco',
            fields=[
                ('ban_id', models.AutoField(primary_key=True, serialize=False, verbose_name='Key')),
                ('ban_nombre', models.CharField(max_length=150, verbose_name='Nombre del banco')),
                ('ban_codigo', models.CharField(max_length=10, verbose_name='Código')),
                ('ban_activo', models.CharField(choices=[('S', 'SI'), ('N', 'NO')], default='S', max_length=1, verbose_name='Activo')),
            ],
            options={
                'db_table': 'usu_bancos',
                'ordering': ['ban_id'],
            },
        ),
        migrations.CreateModel(
            name='CajasCompensacion',
            fields=[
                ('cc_id', models.AutoField(primary_key=True, serialize=False, verbose_name='Key')),
                ('cc_nombre', models.CharField(max_length=100, verbose_name='Nombre')),
                ('cc_codigo', models.CharField(max_length=100, verbose_name='Código')),
            ],
            options={
                'db_table': 'emp_cajas_compensacion',
                'ordering': ['cc_id'],
            },
        ),
        migrations.CreateModel(
            name='Empresa',
            fields=[
                ('emp_id', models.AutoField(primary_key=True, serialize=False, verbose_name='Key')),
                ('emp_codigo', models.CharField(max_length=150, verbose_name='Código de la empresa')),
                ('emp_rut', models.CharField(max_length=25, verbose_name='Rut')),
                ('emp_nombrerepresentante', models.CharField(blank=True, max_length=255, null=True, verbose_name='Nombre representante')),
                ('emp_rutrepresentante', models.CharField(max_length=25, verbose_name='Rut representante')),
                ('emp_isestatal', models.CharField(choices=[('S', 'SI'), ('N', 'NO')], default='N', max_length=1, verbose_name='Es estatal')),
                ('emp_razonsocial', models.CharField(max_length=150, verbose_name='Razón social')),
                ('emp_giro', models.CharField(max_length=150, verbose_name='Giro')),
                ('emp_direccion', models.TextField(verbose_name='Calle')),
                ('emp_numero', models.IntegerField(verbose_name='N°')),
                ('emp_piso', models.CharField(blank=True, max_length=25, null=True, verbose_name='Piso')),
                ('emp_dptooficina', models.CharField(blank=True, max_length=25, null=True, verbose_name='Departamento/oficina')),
                ('emp_cospostal', models.CharField(blank=True, max_length=25, null=True, verbose_name='Código postal')),
                ('emp_fonouno', models.CharField(max_length=25, verbose_name='Télefono 1')),
                ('emp_mailuno', models.CharField(max_length=150, verbose_name='Email 1')),
                ('emp_fonodos', models.CharField(blank=True, max_length=25, null=True, verbose_name='Télefono 2')),
                ('emp_maildos', models.CharField(blank=True, max_length=150, null=True, verbose_name='Email 2')),
                ('emp_fechaingreso', models.DateField(blank=True, null=True, verbose_name='Fecha inicio de actividades')),
                ('emp_isholding', models.CharField(choices=[('S', 'SI'), ('N', 'NO')], default='S', max_length=1, verbose_name='Es sub-empresa')),
                ('emp_activa', models.CharField(choices=[('S', 'SI'), ('N', 'NO')], default='S', max_length=1, verbose_name='Empresa activa')),
                ('emp_rutcontador', models.CharField(blank=True, max_length=12, null=True, verbose_name='Rut contador')),
                ('emp_nombrecontador', models.CharField(blank=True, max_length=150, null=True, verbose_name='Razón social')),
                ('emp_imagenempresa', models.TextField(blank=True, default='', null=True, verbose_name='Nombre imagen')),
                ('emp_colorlogo', models.CharField(blank=True, default='', max_length=10, null=True, verbose_name='Color logo')),
                ('comuna', models.ForeignKey(db_column='emp_comuna', on_delete=django.db.models.deletion.PROTECT, to='base.comuna', verbose_name='Comuna')),
                ('emp_idempresamadre', models.ForeignKey(blank=True, db_column='emp_idempresamadre', default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='empresa.empresa')),
                ('pais', models.ForeignKey(db_column='emp_pais', on_delete=django.db.models.deletion.PROTECT, to='base.pais', verbose_name='País')),
                ('region', models.ForeignKey(db_column='emp_region', on_delete=django.db.models.deletion.PROTECT, to='base.region', verbose_name='Región')),
            ],
            options={
                'db_table': 'emp_empresa',
                'ordering': ['emp_id'],
            },
        ),
        migrations.CreateModel(
            name='Salud',
            fields=[
                ('sa_id', models.AutoField(primary_key=True, serialize=False, verbose_name='Key')),
                ('sa_nombre', models.CharField(max_length=100, verbose_name='Nombre')),
                ('sa_codigo', models.CharField(max_length=100, verbose_name='Código')),
                ('sa_tipo', models.CharField(choices=[('F', 'FONASA'), ('I', 'ISAPRE')], default='I', max_length=1, verbose_name='Tipo')),
            ],
            options={
                'db_table': 'emp_salud',
                'ordering': ['sa_id'],
            },
        ),
        migrations.CreateModel(
            name='TipoContrato',
            fields=[
                ('tc_id', models.AutoField(primary_key=True, serialize=False, verbose_name='Key')),
                ('tc_codcontrato', models.CharField(max_length=25, verbose_name='Codifo contrato')),
                ('tc_nombrecontrato', models.CharField(max_length=100, verbose_name='Nombre contrato')),
                ('cc_contrato', models.TextField(verbose_name='texto del contrato')),
            ],
            options={
                'db_table': 'emp_tipo_contrato',
                'ordering': ['tc_id'],
            },
        ),
        migrations.CreateModel(
            name='Sucursal',
            fields=[
                ('suc_id', models.AutoField(primary_key=True, serialize=False, verbose_name='Key')),
                ('suc_codigo', models.CharField(blank=True, max_length=50, null=True, verbose_name='Código de la unidad')),
                ('suc_descripcion', models.CharField(blank=True, max_length=255, null=True, verbose_name='Descripción de la unidad')),
                ('suc_direccion', models.CharField(default='', max_length=255, verbose_name='Direccion de la unidad')),
                ('suc_estado', models.CharField(choices=[('S', 'SI'), ('N', 'NO')], default='S', max_length=1, verbose_name='Sucursal activa')),
                ('comuna', models.ForeignKey(db_column='suc_comuna', on_delete=django.db.models.deletion.PROTECT, to='base.comuna', verbose_name='Comuna')),
                ('empresa', models.ForeignKey(db_column='suc_empresa', default=0, on_delete=django.db.models.deletion.PROTECT, to='empresa.empresa', verbose_name='Empresa')),
                ('pais', models.ForeignKey(db_column='suc_pais', on_delete=django.db.models.deletion.PROTECT, to='base.pais', verbose_name='País')),
                ('region', models.ForeignKey(db_column='suc_region', on_delete=django.db.models.deletion.PROTECT, to='base.region', verbose_name='Región')),
            ],
            options={
                'db_table': 'emp_sucursal',
            },
        ),
        migrations.CreateModel(
            name='GrupoCentroCosto',
            fields=[
                ('gcencost_id', models.AutoField(primary_key=True, serialize=False, verbose_name='Key')),
                ('gcencost_nombre', models.CharField(max_length=100, verbose_name='Nombre')),
                ('gcencost_codigo', models.CharField(max_length=100, verbose_name='Código')),
                ('gcencost_activo', models.CharField(choices=[('S', 'SI'), ('N', 'NO')], default='S', max_length=1, verbose_name='Activo')),
                ('empresa', models.ForeignKey(db_column='gcencost_empresa', on_delete=django.db.models.deletion.PROTECT, to='empresa.empresa', verbose_name='Empresa')),
            ],
            options={
                'db_table': 'emp_grupo_centro_costo',
                'ordering': ['gcencost_id'],
            },
        ),
        migrations.CreateModel(
            name='CentroCosto',
            fields=[
                ('cencost_id', models.AutoField(primary_key=True, serialize=False, verbose_name='Key')),
                ('cencost_nombre', models.CharField(max_length=100, verbose_name='Nombre')),
                ('cencost_codigo', models.CharField(max_length=100, verbose_name='Código')),
                ('cencost_activo', models.CharField(choices=[('S', 'SI'), ('N', 'NO')], default='S', max_length=1, verbose_name='Activo')),
                ('grupocentrocosto', models.ForeignKey(db_column='ec_grupocentrocosto', on_delete=django.db.models.deletion.PROTECT, to='empresa.grupocentrocosto', verbose_name='Grupo Centro costo')),
            ],
            options={
                'db_table': 'emp_centro_costo',
                'ordering': ['cencost_id'],
            },
        ),
        migrations.CreateModel(
            name='Cargo',
            fields=[
                ('car_id', models.AutoField(primary_key=True, serialize=False, verbose_name='Key')),
                ('car_nombre', models.CharField(max_length=255, verbose_name='Nombre cargo')),
                ('car_activa', models.CharField(choices=[('S', 'SI'), ('N', 'NO')], default='S', max_length=1, verbose_name='Cargo activa')),
                ('empresa', models.ManyToManyField(to='empresa.Empresa')),
            ],
            options={
                'db_table': 'emp_cargo',
                'ordering': ['car_id'],
            },
        ),
    ]