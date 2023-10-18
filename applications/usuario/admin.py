from django.contrib import admin

from applications.usuario.models import Colaborador, UsuarioEmpresa, FamilyResponsibilities, ConceptUser, Contact

# Register your models here.

admin.site.register(Colaborador)
admin.site.register(UsuarioEmpresa)
admin.site.register(FamilyResponsibilities)
admin.site.register(ConceptUser)
admin.site.register(Contact)