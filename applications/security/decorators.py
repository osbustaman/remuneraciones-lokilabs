# -*- encoding: utf-8 -*-
from functools import wraps
from django.shortcuts import redirect
from applications.empresa.models import Empresa
from jwt import encode, decode, ExpiredSignatureError, InvalidSignatureError

from decouple import config

def existsCompany(func):
    def valida(request, *args, **kwargs):
        cantidadEmpresas = Empresa.objects.all().count()
        if cantidadEmpresas < 1:
            valor = redirect('security_app:error404')
        else:
            valor = func(request, *args, **kwargs)
        return valor

    return valida


def verify_token(func):
    @wraps(func)
    def decorador(*args, **kwargs):
        secret = config('SECRET_KEY')
        print(kwargs)
    return decorador