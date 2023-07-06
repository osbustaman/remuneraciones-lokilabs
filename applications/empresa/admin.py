from django.contrib import admin

from applications.empresa.models import Empresa, Sucursal, Cargo, GrupoCentroCosto, CentroCosto

# Register your models here.

admin.site.register(Empresa)
admin.site.register(Sucursal)
admin.site.register(Cargo)
admin.site.register(GrupoCentroCosto)
admin.site.register(CentroCosto)