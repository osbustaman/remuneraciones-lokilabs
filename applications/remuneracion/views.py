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
from applications.usuario.models import Colaborador, UsuarioEmpresa






# Create your views here.

@login_required
def control_panel(request):

    data = {

    }
    return render(request, 'client/page/company/dashboard.html', data)


def download_pdf(request, pdf_filename):
    pdf_file_path = os.path.join(settings.BASE_DIR, 'templates', 'pdf', pdf_filename)
    if os.path.exists(pdf_file_path):
        # Abre y lee el archivo PDF
        with open(pdf_file_path, 'rb') as pdf_file:
            response = HttpResponse(pdf_file.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(pdf_file_path)}"'
            return response
    else:
        # Maneja el caso en el que el archivo PDF no existe
        return HttpResponse("El archivo PDF no se encontró.", status=404)
    
def salary_liquidation_calculations(data, user_id = 3):

    data_colaborador = Colaborador.objects.filter(user__id=user_id).first()

    # forma de pago
    if data_colaborador.col_formapago == 4:
        way_to_pay = f"{ data_colaborador.get_col_formapago_display() }, banco: { data_colaborador.banco.ban_nombre.title() }, N° Cuenta { data_colaborador.col_cuentabancaria }"
    else:
        way_to_pay = data_colaborador.get_col_formapago_display()

    data_user = UsuarioEmpresa.objects.select_related('cargo', 'centrocosto').get(user__id=user_id)

    datos_usuario = {
        'collaborator_name': f"{ data_user.user.first_name.title() } { data_user.user.last_name.title() }",
        'position_company': data_user.cargo.car_nombre,
        'cost_center': data_user.centrocosto.cencost_nombre,
        'rut_dni': data_user.user.username,
        'entry_to_the_company': data_user.ue_fechacontratacion.strftime("%Y-%m-%d"),
        'number_days_worked': '30',
        'way_to_pay': way_to_pay,

        'uf': IndicatorEconomic.get_uf_value_last_day(),
        'utm': IndicatorEconomic.get_utm(),
    }
    
    return datos_usuario


def render_pdf(request):

    get_uf = IndicatorEconomic.get_uf_value_last_day()
    get_utm = IndicatorEconomic.get_utm()

    collaborator_name = 'xxxxx xxxxx xxxxx xxxxx'
    position_company = 'xxxxx'
    cost_center = 'xxxxx'
    rut_dni = 'xxxxxxxx-x'
    entry_to_the_company = 'yyyy-mm-dd'
    number_days_worked = '30'
    way_to_pay = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

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
    tax_base = int(salary_imponible_mount) - int(data_afp['discount_afp']) - int(health_discount) - int(sesantia_insurance['employee_contribution'])
    income_tax = Remunerations.monthly_income_tax_parameters(tax_base)
    
    mounts_dict = [
            {
                'concepto': 'Sueldo Base',
                'haberes': int(request.POST['base_salary']),
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
            },{
                'concepto': income_tax['concept'],
                'haberes': '',
                'descuentos': income_tax['amount_tax'],
            }
        ]
    
    total_assets = 0
    total_discounts = 0
    for value in mounts_dict:
        try:
            total_assets = total_assets + value['haberes']
        except:
            pass

        try:
            total_discounts = total_discounts + value['descuentos']
        except:
            pass

    liquid_salary = total_assets - total_discounts
    legal_discounts = data_afp['discount_afp'] + health_discount + sesantia_insurance['employee_contribution'] + income_tax['amount_tax']
    
    totales = {
        'tax_base': tax_base,
        'base_imponible': salary_imponible_mount,
        'total_discounts': total_discounts,
        'total_assets': total_assets,
        'liquid_salary': liquid_salary,
        'legal_discounts': legal_discounts,
    }

    # Renderiza el template con las variables
    context = {
        'emp_namecompany': company.emp_namecompany,
        'emp_rut': company.emp_rut,
        'emp_company_address': company.emp_company_address,
        'emp_fonouno': company.emp_fonouno,
        'month': month_translate.title(),
        'year': year,

        'collaborator_name': collaborator_name,
        'position_company': position_company,
        'cost_center': cost_center,
        'rut_dni': rut_dni,
        'entry_to_the_company': entry_to_the_company,
        'number_days_worked': number_days_worked,
        'way_to_pay': way_to_pay,

        'data_dict': mounts_dict,
        'totales': totales,
        'get_uf': get_uf
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


@login_required
def calculate_salaries(request):

    pdf_response = None
    if request.method == 'POST':
        form = SalaryCalculatorForm(request.POST)
        if form.is_valid():
            #pdf_response = render_pdf(request)
            pdf_response = salary_liquidation_calculations(request)
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