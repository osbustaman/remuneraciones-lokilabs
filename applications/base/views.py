import json

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

from applications.base.clases.DataBase import DataBase
from applications.base.forms import AdminUserForm, ClientForm

from applications.base.models import Cliente

# Create your views here.

@login_required
def controlPanel(request):
    lst_bases = []

    data = {
        'lst_bases': lst_bases,
    }
    return render(request, 'base/base.html', data)

@login_required
def dashboard(request):

    data = {
    }
    return render(request, 'base/pages/dashboard.html', data)

@login_required
def list_clients(request):

    lst_clients = Cliente.objects.filter(deleted = "N")

    data = {
        'lst_clients': lst_clients,
    }
    return render(request, 'base/pages/list_clients.html', data)

@login_required
def add_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST, request.FILES)
        if form.is_valid():
            client = form.save()
            DataBase.create_database(client.nombre_cliente)
            DataBase.create_migrate(client.nombre_cliente)
            return redirect('base_app:edit_client', client_id=client.id)
        
        lista_err = []
        for field in form:
            for error in field.errors:
                lista_err.append(field.label + ': ' + error)
    else:
        form = ClientForm()
    data = {
        'form': form,
        'action': 'Agregar'
    }
    return render(request, 'base/pages/add_client.html', data)



@login_required
def edit_client(request, client_id):
    client = get_object_or_404(Cliente, id=client_id)
    if request.method == 'POST':
        form = ClientForm(request.POST, request.FILES, instance=client)
        if form.is_valid():
            form.save()
            DataBase.data_one(client.nombre_cliente)
    else:
        form = ClientForm(instance=client)

    list_users = User.objects.using(client.nombre_bd).all()

    data = {
        'form': form,
        'form_admin': AdminUserForm,
        'action': 'Editar',
        'client_id': client_id,
        'list_users': list_users,
        'url_client': client.cli_link
    }
    return render(request, 'base/pages/add_client.html', data)

@login_required
def delete_client(request, client_id):
    client = Cliente.objects.get(id=client_id)
    client.deleted = 'S'
    client.save()
    return redirect('base_app:list-clients')

@login_required
def add_admin(request, client_id):

    lista_err = []
    object_client = Cliente.objects.get(id=client_id)
    form = AdminUserForm(request.POST)
    if form.is_valid():
        admin_user = form.save(commit=False)
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.set_password(request.POST['password'])
        admin_user.save(using=object_client.nombre_cliente)
    else:
        for field in form:
            for error in field.errors:
                lista_err.append(field.label + ': ' + error)

    return redirect('base_app:edit_client', client_id=client_id)

def delete_admin(request, client_id, user_id):
    try:
        object_client = Cliente.objects.get(id=client_id)
        user = User.objects.using(object_client.nombre_bd).get(id=user_id)
        if user.is_superuser:
            user.delete(using=object_client.nombre_bd)
    except User.DoesNotExist:
        pass

    return redirect(request.META.get('HTTP_REFERER'))