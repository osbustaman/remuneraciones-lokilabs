from django.contrib import admin

from applications.security.models import Rol, RoutesRol

# Register your models here.

admin.site.register(Rol)
admin.site.register(RoutesRol)
