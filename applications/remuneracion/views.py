import json

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User


from django.contrib import messages

from applications.remuneracion.forms import SalaryCalculatorForm

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