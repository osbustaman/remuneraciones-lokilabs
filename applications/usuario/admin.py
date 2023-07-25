from django.contrib import admin

from applications.usuario.models import Colaborador, UsuarioEmpresa, FamilyResponsibilities

# Register your models here.

admin.site.register(Colaborador)
admin.site.register(UsuarioEmpresa)
admin.site.register(FamilyResponsibilities)