import json

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from applications.account_base.forms import LoginForm
from applications.empresa.forms import EmpresaForm
from applications.empresa.models import Empresa

# Create your views here.

@login_required
def control_panel(request):

    data = {

    }
    return render(request, 'client/page/company/dashboard.html', data)