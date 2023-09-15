import json
import pdfkit

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
from applications.empresa.models import Empresa



from applications.remuneracion.forms import SalaryCalculatorForm
from applications.remuneracion.indicadores import IndicatorEconomic
from applications.remuneracion.remuneracion import Remunerations






# Create your views here.

@login_required
def control_panel(request):

    data = {

    }
    return render(request, 'client/page/company/dashboard.html', data)


@login_required
def render_pdf2(request):

    base_dir = f"{settings.BASE_DIR}/templates/"
    # Ruta al archivo HTML existente que deseas convertir en PDF
    html_file_path = f"{base_dir}pdf/salary_settlement.html"  # Reemplaza esto con la ruta real de tu archivo HTML

    # Lee el contenido del archivo HTML
    with open(html_file_path, 'r') as file:
        html_content = file.read()

    # Convierte el HTML en PDF
    pdf = pdfkit.from_string(html_content, False)

    # Devuelve el PDF como respuesta
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="archivo.pdf"'
    return response


def render_pdf(request):
    # Variables que deseas pasar al template
    titulo = "Título del PDF"
    contenido = "Este es el contenido del PDF con variables."


    company = Empresa.objects.get(emp_id = int(request.session['la_empresa']))


    # Renderiza el template con las variables
    context = {

        'emp_namecompany': company.emp_namecompany,
        'emp_rut': company.emp_rut,
        'emp_company_address': company.emp_company_address,
        'emp_fonouno': company.emp_fonouno,


        'titulo': titulo,
        'contenido': contenido,
    }
    rendered_html = render(request, 'pdf/salary_settlement.html', context).content.decode('utf-8')

    # Convierte el HTML en PDF
    pdf = pdfkit.from_string(rendered_html, False)

    # Devuelve el PDF como respuesta
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="archivo.pdf"'
    return response


@login_required
def calculate_salaries(request):


    if request.method == 'POST':
        form = SalaryCalculatorForm(request.POST)
        if form.is_valid():


            get_uf = IndicatorEconomic.get_uf_value_last_day()

            data_afp = Remunerations.calculate_afp_quote(request.POST['afp'], request.POST['type_of_work'], request.POST['base_salary'])

            uf_valor = request.POST.get('quantity_uf_health', '0')
            data_health = Remunerations.calculate_health_discount(request.POST['base_salary'], request.POST['salud'], uf_valor)

            
            bonus_cap = 0
            if int(request.POST['has_legal_gratification']) == 1:
                bonus_cap = Remunerations.obtain_legal_bonus_cap(request.POST['type_of_gratification'], request.POST['base_salary'], True)


            taxable_salary = int(request.POST['base_salary']) + bonus_cap['legal_bonus_cap']

            print(request.POST)

        for field in form:
            for error in field.errors:
                messages.error(request, f"{field.label}: {error}")
    else:
        form = SalaryCalculatorForm()



    data = {
        'form': form
    }
    return render(request, 'client/page/remunerations/page/calculate_salaries.html', data)