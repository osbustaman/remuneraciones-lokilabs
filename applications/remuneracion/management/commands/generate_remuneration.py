# -*- encoding: utf-8 -*-
import calendar
import json
import requests
import datetime

from django.contrib.auth.models import User

from app01.functions import load_data_base
from applications.base.models import Cliente, TablaGeneral
from applications.empresa.models import Afp
from applications.remuneracion.indicadores import IndicatorEconomic

from django.core.management.base import BaseCommand
from applications.remuneracion.remuneracion import Remunerations

from applications.usuario.models import ConceptUser, UsuarioEmpresa

class Command(BaseCommand):

    help = 'ingresa el nombre de la nueva base'
    
    page = requests.get('https://www.previred.com/indicadores-previsionales/')


    def generate_remunaration(self, user_id, nombre_bd):

        """
        generate_remunaration - Funcion que se encarga de generar la remuneracion del colaborador
        
        :param user_id: id del usuario
        
        :return: 
            un diccionario con toda la información de la remuneracion
        """

        object_concept_user = ConceptUser.objects.using(nombre_bd).filter(user_id = user_id)

        print(object_concept_user)


    def handle(self, *args, **kwargs):

        load_data_base()
        list_clients = Cliente.objects.all()

        for value in list_clients:
            nombre_bd = value.nombre_bd

            object_usuario_empresa = UsuarioEmpresa.objects.using(nombre_bd).select_related('user')
            for value in object_usuario_empresa:
                self.generate_remunaration(value.user.id, nombre_bd)

                