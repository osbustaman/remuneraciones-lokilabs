from django.contrib import messages

from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from applications.account_base.forms import LoginForm
from applications.usuario.models import Colaborador, UsuarioEmpresa

# Create your views here.

def login_client(request):

    data = {
        'form': LoginForm,
    }

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            request.session['username'] = user.username
            request.session['first_name'] = user.first_name
            request.session['last_name'] = user.last_name
            request.session['id'] = user.id

            try:
                objectColaborator = Colaborador.objects.get(user=user)
                request.session['user_nivel'] = objectColaborator.col_tipousuario.rol_nivel
            except:
                request.session['user_nivel'] = 8

            try:
                objectColaborator = UsuarioEmpresa.objects.get(user=user)
                request.session['la_empresa'] = objectColaborator.empresa.emp_id
                request.session['razon_social'] = objectColaborator.empresa.emp_namecompany
                request.session['emp_namecompany'] = objectColaborator.empresa.emp_namecompany
            except:
                pass

            #return HttpResponseRedirect(reverse('remun_app:panel'))
            return redirect('usuario_app:init_page')
        else:
            data['error'] = 'Usuario o contraseña incorrectos.'
            return render(request, 'client/login.html', data)
    else:
        return render(request, 'client/login.html', data)
    
def logout_client(request):
    logout(request)
    request.session.flush()
    response = redirect(reverse('account_base:login_client'))
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

def login_view(request):

    data = {
        'form': LoginForm,
    }

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            request.session['username'] = user.username
            request.session['first_name'] = user.first_name
            request.session['last_name'] = user.last_name
            request.session['id'] = user.id
            return HttpResponseRedirect(reverse('base_app:control-panel'))
        else:
            messages.error(request, f"Usuario o contraseña incorrectos.")
            return render(request, 'base/login.html', data)
    else:
        return render(request, 'base/login.html', data)
    
def logout_view(request):
    logout(request)
    request.session.flush()
    response = redirect(reverse('account_base:accounts-login'))
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response