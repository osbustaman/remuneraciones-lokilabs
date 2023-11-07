# -*- encoding: utf-8 -*-
import calendar
import json
import requests
import datetime

from app01.functions import load_data_base
from applications.base.models import Cliente, TablaGeneral
from applications.empresa.models import Afp
from applications.remuneracion.indicadores import IndicatorEconomic
