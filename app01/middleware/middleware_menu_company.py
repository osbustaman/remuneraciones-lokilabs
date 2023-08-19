from applications.empresa.models import Empresa


class middleware_menu_company(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        try:
            lstEmpresas = []
            emp = Empresa.objects.all()

            for e in emp:
                lstEmpresas.append({
                    'key':e.emp_id,
                    'value':e.emp_namecompany
                })
            request.session['list_company'] = lstEmpresas
        except:
            pass