import json

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User


from django.contrib import messages

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