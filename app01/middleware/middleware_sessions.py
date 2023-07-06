# -*- encoding: utf-8 -*-

import json
from applications.empresa.models import Empresa


class middleware_sessions(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):

        try:

            object_company = Empresa.objects.filter(emp_activa = 'S').first()
            
            is_company = True if not object_company == None else False
            if is_company:           
                request.session['logo_company'] = f"/media/{str(object_company.emp_imagenempresa)}"
                request.session['is_company'] = True

        except:
            pass