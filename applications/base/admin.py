from django.contrib import admin

from applications.base.models import Cliente, TablaGeneral

# Register your models here.

admin.site.register(Cliente)
admin.site.register(TablaGeneral)