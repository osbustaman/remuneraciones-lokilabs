import calendar
import json
import os
import pdfkit

from datetime import datetime

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse, FileResponse
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


def serve_pdf(request, pdf_filename):
    pdf_path = os.path.join(settings.BASE_DIR, 'templates', 'pdf', pdf_filename)
    if os.path.exists(pdf_path):
        with open(pdf_path, 'rb') as pdf_file:
            response = FileResponse(pdf_file, content_type='application/pdf')
            response['Content-Disposition'] = f'inline; filename="{pdf_filename}"'
            return response
    else:
        # Maneja el caso en el que el archivo PDF no existe
        return HttpResponse("El archivo PDF no se encontró.", status=404)


def render_pdf(request):

    get_uf = IndicatorEconomic.get_uf_value_last_day()

    bonus_cap = 0
    if int(request.POST['has_legal_gratification']) == 1:
        bonus_cap = Remunerations.obtain_legal_bonus_cap(request.POST['type_of_gratification'], request.POST['base_salary'], True)


    salary_imponible_mount = int(bonus_cap['legal_bonus_cap']) + int(request.POST['base_salary'])

    data_afp = Remunerations.calculate_afp_quote(request.POST['afp'], request.POST['type_of_work'], salary_imponible_mount)
    afp_nombre = f"AFP: {data_afp['afp_nombre']} - {data_afp['quote_rate']}%"
    
    
    
    
    uf_valor = request.POST.get('quantity_uf_health', '0')
    data_health = Remunerations.calculate_health_discount(salary_imponible_mount, request.POST['salud'], uf_valor)

    if data_health['quantity_uf_health']:
        salud_name = f"{data_health['sa_nombre']} - UF: {data_health['quantity_uf_health']} (7% {data_health['health_discount']}, diferencia {data_health['difference_of_amount']})"
        health_discount = data_health['health_discount_uf']
    else:
        salud_name = f"{data_health['sa_nombre']} - 7%"
        health_discount = data_health['health_discount']


    company = Empresa.objects.get(emp_id=int(request.session['la_empresa']))

    date_now = datetime.now()
    month = calendar.month_name[date_now.month]
    year = date_now.year

    month_translate = Remunerations.translate_month(month)

    sesantia_insurance = Remunerations.calculate_sesantia_insurance(salary_imponible_mount, request.POST['type_of_contract'])

    mounts_dict = [
            {
                'concepto': 'Sueldo Base',
                'haberes': request.POST['base_salary'],
                'descuentos': '',
            },{
                'concepto': 'Gratificación Legal',
                'haberes': bonus_cap['legal_bonus_cap'],
                'descuentos': '',
            },{
                'concepto': afp_nombre,
                'haberes': '',
                'descuentos': data_afp['discount_afp'],
            },{
                'concepto': salud_name,
                'haberes': '',
                'descuentos': health_discount,
            },{
                'concepto': sesantia_insurance['concept'],
                'haberes': '',
                'descuentos': sesantia_insurance['employee_contribution'],
            }

        ]
    
    totales = {
        'tributable': 0,
        'base_imponible': 0,
        'descuentos_legales': 0,
        'sueldo_liquido': 0,
    }

    # Renderiza el template con las variables
    context = {
        'emp_namecompany': company.emp_namecompany,
        'emp_rut': company.emp_rut,
        'emp_company_address': company.emp_company_address,
        'emp_fonouno': company.emp_fonouno,
        'month': month_translate.title(),
        'year': year,

        'data_dict': mounts_dict
    }
    rendered_html = render(request, 'pdf/salary_settlement.html', context).content.decode('utf-8')


    # Obtener la fecha y hora actual
    fecha_actual = datetime.now()

    # Formatear la fecha en el formato YYYYmmdd_hhmmss
    pdf_filename = fecha_actual.strftime('%Y%m%d_%H%M%S.pdf')

    # Ruta donde se guardará el PDF
    pdf_path = os.path.join(settings.BASE_DIR, 'templates', 'pdf', pdf_filename)

    # Convierte el HTML en PDF y guárdalo en la ruta especificada
    pdfkit.from_string(rendered_html, pdf_path)

    # Devuelve el nombre del archivo PDF, no la ruta completa
    return pdf_filename


def render_pdf2(request):

    get_uf = IndicatorEconomic.get_uf_value_last_day()
    data_afp = Remunerations.calculate_afp_quote(request.POST['afp'], request.POST['type_of_work'], request.POST['base_salary'])
    uf_valor = request.POST.get('quantity_uf_health', '0')
    data_health = Remunerations.calculate_health_discount(request.POST['base_salary'], request.POST['salud'], uf_valor)

    bonus_cap = 0
    if int(request.POST['has_legal_gratification']) == 1:
        bonus_cap = Remunerations.obtain_legal_bonus_cap(request.POST['type_of_gratification'], request.POST['base_salary'], True)

    taxable_salary = int(request.POST['base_salary']) + bonus_cap['legal_bonus_cap']

    company = Empresa.objects.get(emp_id = int(request.session['la_empresa']))

    date_now = datetime.now()
    month = calendar.month_name[date_now.month]
    year = date_now.year


    month_translate = Remunerations.translate_month(month)

    # Renderiza el template con las variables
    context = {

        'emp_namecompany': company.emp_namecompany,
        'emp_rut': company.emp_rut,
        'emp_company_address': company.emp_company_address,
        'emp_fonouno': company.emp_fonouno,
        'month': month_translate.title(),
        'year': year,

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

    pdf_response = None
    if request.method == 'POST':
        form = SalaryCalculatorForm(request.POST)
        if form.is_valid():
            pdf_response = render_pdf(request)
        for field in form:
            for error in field.errors:
                messages.error(request, f"{field.label}: {error}")
    else:
        form = SalaryCalculatorForm()

    data = {
        'form': form,
        'pdf_response': pdf_response,
    }
    return render(request, 'client/page/remunerations/page/calculate_salaries.html', data)