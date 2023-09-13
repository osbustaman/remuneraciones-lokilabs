from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from app01.functions import getLatitudeLongitude
from applications.base.models import TablaGeneral
from applications.empresa.models import Afp, Apv, Banco, CajasCompensacion, Cargo, CentroCosto, Empresa, Salud, Sucursal
from applications.security.decorators import existsCompany
from applications.usuario.forms import ColaboradorForm, ContactForm, DatosLaboralesForm, FamilyResponsibilitiesForm, FormsForecastData, FormsPayments, UserForm
from django.contrib.auth.models import User

from django.db.models import F, Value, CharField
from django.db.models.functions import Concat

from applications.usuario.models import Colaborador, Contact, FamilyResponsibilities, UsuarioEmpresa

# Create your views here.
@login_required
@existsCompany
def mark_in_out(request):


    data = {

    }
    return render(request, 'client/page/usuario/forms/from_mark_in_out.html', data)