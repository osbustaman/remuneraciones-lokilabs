# -*- encoding: utf-8 -*-

class menu_middleware_items(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):

        try:

            if '/client/edit/' in request.path:
                request.session['item'] = 'clientes'
                request.session['sub_item'] = 'cliente'

            if '/add-client/' in request.path:
                request.session['item'] = 'clientes'
                request.session['sub_item'] = 'cliente'


            # ----
            if '/mi-perfil' in request.path:
                request.session['item'] = 'inicio'
                request.session['sub_item'] = 'inicio'  
                request.session['sub_sub_item'] = 'inicio' 

            if '/company/list/' in request.path:
                request.session['item'] = 'configuracion'
                request.session['sub_item'] = 'empresa'  
                request.session['sub_sub_item'] = 'empresa' 

            if '/company/add/' in request.path:
                request.session['item'] = 'configuracion'
                request.session['sub_item'] = 'empresa'  
                request.session['sub_sub_item'] = 'empresa' 
            
            if '/company/countries/' in request.path:
                request.session['item'] = 'configuracion'
                request.session['sub_item'] = 'tablas' 
                request.session['sub_sub_item'] = 'countries' 

            if '/company/regions/' in request.path:
                request.session['item'] = 'configuracion'
                request.session['sub_item'] = 'tablas' 
                request.session['sub_sub_item'] = 'regions'  

            if '/company/communes/' in request.path:
                request.session['item'] = 'configuracion'
                request.session['sub_item'] = 'tablas' 
                request.session['sub_sub_item'] = 'communes'  
            
            if '/company/afp/' in request.path:
                request.session['item'] = 'configuracion'
                request.session['sub_item'] = 'tablas' 
                request.session['sub_sub_item'] = 'afp' 

            if '/company/health/' in request.path:
                request.session['item'] = 'configuracion'
                request.session['sub_item'] = 'tablas' 
                request.session['sub_sub_item'] = 'salud' 

            if '/company/compensation/box/' in request.path:
                request.session['item'] = 'configuracion'
                request.session['sub_item'] = 'tablas' 
                request.session['sub_sub_item'] = 'compensation_box' 

            if '/company/banks/' in request.path:
                request.session['item'] = 'configuracion'
                request.session['sub_item'] = 'tablas' 
                request.session['sub_sub_item'] = 'banks' 

            if '/company/banks/add/' in request.path:
                request.session['item'] = 'configuracion'
                request.session['sub_item'] = 'tablas' 
                request.session['sub_sub_item'] = 'banks' 
            
            if '/company/apv/' in request.path:
                request.session['item'] = 'configuracion'
                request.session['sub_item'] = 'tablas' 
                request.session['sub_sub_item'] = 'apv' 
            
            if '/company/mutual/security/' in request.path:
                request.session['item'] = 'configuracion'
                request.session['sub_item'] = 'tablas' 
                request.session['sub_sub_item'] = 'mutual'

            if '/company/concepts/' in request.path:
                request.session['item'] = 'configuracion'
                request.session['sub_item'] = 'tablas' 
                request.session['sub_sub_item'] = 'concepts' 

            if '/collaborator/file/' in request.path:
                request.session['item'] = 'configuracion'
                request.session['sub_item'] = 'colaboradores' 
                request.session['sub_sub_item'] = 'search-user'

            if '/marcar-jornada-laboral' in request.path:
                request.session['item'] = 'eventos'
                request.session['sub_item'] = 'evento' 
                request.session['sub_sub_item'] = 'evento'

            if '/calculate-salaries/' in request.path:
                request.session['item'] = 'remuneraciones'
                request.session['sub_item'] = 'calculator' 
                request.session['sub_sub_item'] = 'calculator'
            
            if '/indicadores-previsionales' in request.path:
                request.session['item'] = 'remuneraciones'
                request.session['sub_item'] = 'previred_forecast_indicators' 
                request.session['sub_sub_item'] = 'previred_forecast_indicators'
            
            if '/variables-remuneraciones' in request.path:
                request.session['item'] = 'remuneraciones'
                request.session['sub_item'] = 'remuneration_variables' 
                request.session['sub_sub_item'] = 'remuneration_variables'

            if '/jornada-colaboradores' in request.path:
                request.session['item'] = 'eventos'
                request.session['sub_item'] = 'collaborators_working_day' 
                request.session['sub_sub_item'] = 'collaborators_working_day'

            if '/reportes-asistencia' in request.path:
                request.session['item'] = 'eventos'
                request.session['sub_item'] = 'collaborators_working_day' 
                request.session['sub_sub_item'] = 'collaborators_working_day'

        except:
            pass