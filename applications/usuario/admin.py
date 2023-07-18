from django.contrib import admin

from applications.usuario.models import Colaborador, UsuarioEmpresa

# Register your models here.

admin.site.register(Colaborador)
admin.site.register(UsuarioEmpresa)