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
            
        except:
            pass