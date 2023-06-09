# Generated by Django 3.2 on 2023-06-09 16:09

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pais',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('pa_id', models.AutoField(primary_key=True, serialize=False, verbose_name='Key')),
                ('pa_nombre', models.CharField(max_length=255, verbose_name='Nombre país')),
                ('pa_codigo', models.IntegerField(unique=True, verbose_name='Código area país')),
            ],
            options={
                'db_table': 'conf_pais',
                'ordering': ['pa_id'],
            },
        ),
        migrations.CreateModel(
            name='ParametrosIndicadoresPrevisionales',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('pip_id', models.AutoField(primary_key=True, serialize=False, verbose_name='Key')),
                ('pip_codigo', models.CharField(max_length=10, verbose_name='Código del parámetro')),
                ('pip_descripcion', models.TextField(max_length=255, verbose_name='Descripción')),
                ('pip_valor', models.CharField(blank=True, default=0, max_length=50, null=True, verbose_name='Valor')),
                ('pip_rangoini', models.DecimalField(blank=True, decimal_places=6, default=0, max_digits=15, null=True, verbose_name='Desde $')),
                ('pip_rangofin', models.DecimalField(blank=True, decimal_places=6, default=0, max_digits=15, null=True, verbose_name='Hasta $')),
                ('pip_factor', models.CharField(max_length=50, verbose_name='Factor')),
                ('pip_activo', models.CharField(choices=[('S', 'SI'), ('N', 'NO')], default='S', max_length=1, verbose_name='Activo')),
            ],
            options={
                'db_table': 'conf_parametros_indicadores_previsionales',
                'ordering': ['pip_id'],
            },
        ),
        migrations.CreateModel(
            name='TablaGeneral',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('tg_id', models.AutoField(primary_key=True, serialize=False, verbose_name='Key')),
                ('tg_nombretabla', models.CharField(max_length=150, verbose_name='nombre_tabla')),
                ('tg_idelemento', models.CharField(blank=True, max_length=25, null=True, verbose_name='elemento_id')),
                ('tg_descripcion', models.TextField(blank=True, null=True, verbose_name='descripcion')),
                ('tg_activo', models.CharField(choices=[('S', 'SI'), ('N', 'NO')], default='S', max_length=1, verbose_name='Activo')),
            ],
            options={
                'db_table': 'conf_tabla_general',
                'ordering': ['tg_id'],
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('re_id', models.AutoField(primary_key=True, serialize=False, verbose_name='Key')),
                ('re_nombre', models.CharField(max_length=255, verbose_name='Nombre región')),
                ('re_numeroregion', models.CharField(blank=True, max_length=5, null=True, verbose_name='Sigla de región')),
                ('re_numero', models.IntegerField(db_index=True, verbose_name='Número de región')),
                ('pais', models.ForeignKey(blank=True, db_column='re_pais', null=True, on_delete=django.db.models.deletion.PROTECT, to='base.pais', verbose_name='País')),
            ],
            options={
                'db_table': 'conf_region',
                'ordering': ['re_id'],
            },
        ),
        migrations.CreateModel(
            name='Comuna',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('com_id', models.AutoField(primary_key=True, serialize=False, verbose_name='Key')),
                ('com_nombre', models.CharField(max_length=255, verbose_name='Nombre comuna')),
                ('com_numero', models.IntegerField(default=0, verbose_name='Numero comuna')),
                ('region', models.ForeignKey(blank=True, db_column='com_region', null=True, on_delete=django.db.models.deletion.PROTECT, to='base.region', verbose_name='Región')),
            ],
            options={
                'db_table': 'conf_comuna',
                'ordering': ['com_id'],
            },
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('nombre_cliente', models.CharField(max_length=120, verbose_name='Nombre del cliente')),
                ('rut_cliente', models.CharField(max_length=20, verbose_name='Rut del cliente')),
                ('nombre_bd', models.CharField(max_length=20, verbose_name='Nombre base de datos')),
                ('cli_link', models.CharField(default='', max_length=255, verbose_name='Link base')),
                ('imagen_cliente', models.ImageField(blank=True, null=True, upload_to=None, verbose_name='Logo Cliente')),
                ('favicon_cliente', models.ImageField(blank=True, null=True, upload_to=None, verbose_name='Favicon Cliente')),
                ('cliente_activo', models.CharField(choices=[('S', 'SI'), ('N', 'NO')], default='S', max_length=1, verbose_name='Cliente activo')),
                ('fecha_ingreso', models.DateField(verbose_name='Fecha creación de la base')),
                ('fecha_termino', models.DateField(verbose_name='Fecha termino de la base')),
                ('cantidad_usuarios', models.IntegerField(verbose_name='Cantidad usuarios')),
                ('nombre_representante', models.CharField(max_length=75, verbose_name='Nombre representante')),
                ('rut_representante', models.CharField(max_length=20, verbose_name='Rut representante')),
                ('correo_representante', models.CharField(max_length=100, verbose_name='Rut representante')),
                ('telefono_representante', models.CharField(max_length=100, verbose_name='Teléfono representante')),
                ('dirección_representante', models.CharField(max_length=100, verbose_name='Dirección representante')),
                ('emp_codpostal', models.CharField(blank=True, max_length=25, null=True, verbose_name='Código postal')),
                ('ruta_directorio', models.CharField(blank=True, max_length=255, null=True, verbose_name='Directorio cliente')),
                ('deleted', models.CharField(blank=True, choices=[('S', 'SI'), ('N', 'NO')], default='N', max_length=1, null=True, verbose_name='deleted')),
                ('comuna', models.ForeignKey(blank=True, db_column='comuna', null=True, on_delete=django.db.models.deletion.PROTECT, to='base.comuna', verbose_name='Comuna')),
                ('pais', models.ForeignKey(blank=True, db_column='pais', null=True, on_delete=django.db.models.deletion.PROTECT, to='base.pais', verbose_name='País')),
                ('region', models.ForeignKey(blank=True, db_column='region', null=True, on_delete=django.db.models.deletion.PROTECT, to='base.region', verbose_name='Región')),
            ],
            options={
                'db_table': 'conf_cliente',
                'ordering': ['id'],
                'unique_together': {('rut_cliente',)},
            },
        ),
    ]
