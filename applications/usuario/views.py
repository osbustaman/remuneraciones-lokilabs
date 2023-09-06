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
def collaborator_file(request):

    # Realizar el join entre Colaborador, UsuarioEmpresa y User
    try:
        list_objects = Colaborador.objects.filter(
            user__usuarioempresa__empresa_id=request.session['la_empresa']
        ).annotate(
            full_name=Concat('user__first_name', Value(' '), 'user__last_name'),
            cargo_nombre=F('user__usuarioempresa__cargo__car_nombre'),
            centro_costo_nombre=F('user__usuarioempresa__centrocosto__cencost_nombre')
        )
        
        data = {
            'list_objects': list_objects
        }
        return render(request, 'client/page/usuario/collaborator_file.html', data)
    except KeyError:
        return redirect('usuario_app:add_collaborator_file')
    except Exception as ex:
        return redirect('security_app:error404')


@login_required
def add_collaborator_file(request):

    if request.method == 'POST':
        formUserForm = UserForm(request.POST)
        formColaboradorForm = ColaboradorForm(request.POST)
        
        if formUserForm.is_valid() and formColaboradorForm.is_valid():
            # Guardar los datos del formulario UserForm
            user = formUserForm.save(commit=False)
            user.is_staff = True
            user.is_superuser = False
            user.set_password(request.POST['password'])
            user.save()

            # Guardar los datos del formulario ColaboradorForm con el ID del usuario
            colaborador = formColaboradorForm.save(commit=False)
            colaborador.user_id = user.id

            address = f"{ colaborador.col_direccion }, { colaborador.comuna.com_nombre }, { colaborador.region.re_nombre }, { colaborador.pais.pa_nombre }"
            lat, lng = getLatitudeLongitude(address)
            
            colaborador.col_latitude = lat
            colaborador.col_longitude = lng
            colaborador.save()

            usuarioEmpresa = UsuarioEmpresa()
            usuarioEmpresa.user = user
            usuarioEmpresa.empresa = Empresa.objects.get(emp_id = int(request.session['la_empresa']))
            usuarioEmpresa.save()


            messages.success(request, 'Datos personales creados exitosamente!.')

            return redirect('usuario_app:edit_collaborator_file', id=user.id, col_id=colaborador.col_id)
        
        else:
            for field in formUserForm:
                for error in field.errors:
                    messages.error(request, f"{field.label}: {error}")
    else:
        formUserForm = UserForm()
        formColaboradorForm = ColaboradorForm()


    data = {
        'action': 'Crear',
        'formUserForm': formUserForm,
        'formColaboradorForm': formColaboradorForm
    }
    return render(request, 'client/page/usuario/add_collaborator_file.html', data)


@login_required
def edit_collaborator_file(request, id, col_id):
    user = get_object_or_404(User, id=id)
    colaborador = get_object_or_404(Colaborador, user=user)

    try:
        usuario_empresa = get_object_or_404(UsuarioEmpresa, user=user)
    except:
        usuario_empresa = False

    if request.method == 'POST':
        formUserForm = UserForm(request.POST, instance=user)
        formColaboradorForm = ColaboradorForm(request.POST, instance=colaborador)

        if usuario_empresa:
            formDatosLaboralesForm = DatosLaboralesForm(instance=usuario_empresa)
            formFormsPayments = FormsPayments(instance=colaborador)
            formFormsForecastData = FormsForecastData(instance=usuario_empresa)
        else:
            formDatosLaboralesForm = DatosLaboralesForm()
            formFormsPayments = FormsPayments()
            formFormsForecastData = FormsForecastData()

        if formUserForm.is_valid() and formColaboradorForm.is_valid():
            user = formUserForm.save(commit=False)

            # Establecer la contraseña utilizando el valor de colaborador.col_rut
            password = colaborador.col_rut
            hashed_password = make_password(password)
            user.password = hashed_password
            user.save()

            colaborador = formColaboradorForm.save(commit=False)
            colaborador.user = user

            address = f"{ colaborador.col_direccion }, { colaborador.comuna.com_nombre }, { colaborador.region.re_nombre }, { colaborador.pais.pa_nombre }"
            lat, lng = getLatitudeLongitude(address)
            
            colaborador.col_latitude = lat
            colaborador.col_longitude = lng

            colaborador.save()

            messages.success(request, 'Datos personales editados exitosamente!.')

        else:
            for field in formUserForm:
                for error in field.errors:
                    messages.error(request, f"{field.label}: {error}")

    else:
        formUserForm = UserForm(instance=user)
        formColaboradorForm = ColaboradorForm(instance=colaborador)
        try:
            formDatosLaboralesForm = DatosLaboralesForm(instance=usuario_empresa)
            formFormsPayments = FormsPayments(instance=colaborador)
            formFormsForecastData = FormsForecastData(instance=usuario_empresa)
        except AttributeError:
            formDatosLaboralesForm = DatosLaboralesForm()
            formFormsPayments = FormsPayments()
            formFormsForecastData = FormsForecastData()

    list_contact = Contact.objects.filter(con_actiove="S")
    list_familyResponsibilities = FamilyResponsibilities.objects.filter(fr_activo=1)

    opciones_working_day = TablaGeneral.objects.filter(tg_nombretabla="tb_working_day").annotate(display_name=Concat(
                F('tg_id'), Value(' - '), F('tg_short_description'), output_field=CharField())).values_list('display_name', flat=True)  # flat=True para obtener una lista plana

    # Crear una instancia del formulario y establecer el valor inicial para working_day
    formularioWorkingDay = DatosLaboralesForm(initial={'working_day': opciones_working_day.first()})

    data = {
        'action': 'Editar',
        'formUserForm': formUserForm,
        'formColaboradorForm': formColaboradorForm,
        'formDatosLaboralesForm': formDatosLaboralesForm,
        'formFormsPayments': formFormsPayments,
        'formFormsForecastData': formFormsForecastData,
        'formularioWorkingDay': formularioWorkingDay,
        'id': id,
        'col_id': col_id,
        'list_contact': list_contact,
        'list_familyResponsibilities': list_familyResponsibilities,
        'colaborador': colaborador,
        'usuario_empresa': usuario_empresa,
    }
    return render(request, 'client/page/usuario/add_collaborator_file.html', data)


@login_required
def add_contact(request, user_id, col_id):

    if request.method == 'POST':
        formContactForm = ContactForm(request.POST)
        
        if formContactForm.is_valid():
            # Guardar los datos del formulario UserForm
            contact = formContactForm.save(commit=False)
            object_user = User.objects.get(id=user_id)
            contact.user = object_user
            contact.save()

            messages.success(request, 'Datos de contacto creados exitosamente!.')

            return redirect('usuario_app:edit_collaborator_file', id=user_id, col_id=col_id)
        
        else:
            for field in formContactForm:
                for error in field.errors:
                    messages.error(request, f"{field.label}: {error}")
    else:
        formContactForm = ContactForm()

    data = {
        'action': 'Crear',
        'form': formContactForm,
        'id': user_id, 
        'col_id': col_id
    }
    return render(request, 'client/page/usuario/forms/forms_add_contact.html', data)


@login_required
def contact_delete(request, con_id, user_id, col_id):
    object = Contact.objects.get(con_id=con_id)
    object.con_actiove = 'N'
    object.save()
    return redirect('usuario_app:edit_collaborator_file', user_id, col_id)


@login_required
def add_personal_information(request, user_id, col_id):

    object_user = User.objects.get(id=user_id)
    try:
        usuario_empresa = get_object_or_404(UsuarioEmpresa, user=object_user)
    except:
        usuario_empresa = False
    
    if request.method == 'POST':

        if usuario_empresa:
            form = DatosLaboralesForm(request.POST, instance=usuario_empresa)
        else:
            form = DatosLaboralesForm(request.POST)

        if form.is_valid():
            dp = form.save(commit=False)
            dp.user = User.objects.get(id=user_id)
            dp.empresa = Empresa.objects.all().first()
            dp.cargo = Cargo.objects.get(car_id=request.POST['cargo'])
            dp.centrocosto = CentroCosto.objects.get(cencost_id=request.POST['centrocosto'])
            dp.sucursal = Sucursal.objects.get(suc_id=request.POST['sucursal'])
            dp.save()

            # Agregar mensaje de éxito personal_information
            messages.success(request, 'Datos personales creados exitosamente.')
            
        else:
            for field in form:
                for error in field.errors:
                    messages.error(request, f"{field.label}: {error}")
            # Aquí puedes agregar un mensaje de error si es necesario

    return redirect('usuario_app:edit_collaborator_file', id=user_id, col_id=col_id)



@login_required
def add_form_payment(request, user_id, col_id):
    try:
        collaborator = get_object_or_404(Colaborador, col_id=col_id)
    except:
        collaborator = False
    
    if request.method == 'POST':

        if collaborator:
            form = FormsPayments(request.POST, instance=collaborator)
        else:
            form = FormsPayments(request.POST)

        if form.is_valid():
            dp = form.save(commit=False)
            if request.POST.get("banco", None):
                dp.banco = Banco.objects.get(ban_id=request.POST['banco'])
            dp.save()

            # Agregar mensaje de éxito personal_information
            messages.success(request, 'La forma de pago fue creada exitosamente.')
            
        else:
            for field in form:
                for error in field.errors:
                    messages.error(request, f"{field.label}: {error}")
            # Aquí puedes agregar un mensaje de error si es necesario

    return redirect('usuario_app:edit_collaborator_file', id=user_id, col_id=col_id)


@login_required
def add_forecast_data(request, user_id, col_id):

    object_user = User.objects.get(id=user_id)
    try:
        usuario_empresa = get_object_or_404(UsuarioEmpresa, user=object_user)
    except:
        usuario_empresa = False
    
    if request.method == 'POST':

        if usuario_empresa:
            form = FormsForecastData(request.POST, instance=usuario_empresa)
        else:
            form = FormsForecastData(request.POST)

        if form.is_valid():
            dp = form.save(commit=False)

            dp.afp = Afp.objects.get(afp_id=request.POST['afp'])
            dp.salud = Salud.objects.get(sa_id=request.POST['salud'])
            if request.POST['apv']:
                dp.apv = Apv.objects.get(apv_id=request.POST['apv'])
            dp.caja_compensacion = CajasCompensacion.objects.get(cc_id=request.POST['caja_compensacion'])
            dp.save()

            # Agregar mensaje de éxito personal_information
            messages.success(request, 'Datos previsionales creados exitosamente.')
            
        else:
            for field in form:
                for error in field.errors:
                    messages.error(request, f"{field.label}: {error}")
            # Aquí puedes agregar un mensaje de error si es necesario


    return redirect('usuario_app:edit_collaborator_file', id=user_id, col_id=col_id)


@login_required
def add_family_responsibilities(request, user_id, col_id):

    if request.method == 'POST':
        formFamilyResponsibilitiesForm = FamilyResponsibilitiesForm(request.POST)
        
        if formFamilyResponsibilitiesForm.is_valid():
            # Guardar los datos del formulario UserForm
            object = formFamilyResponsibilitiesForm.save(commit=False)
            object.user = User.objects.get(id=user_id)
            object.save()

            messages.success(request, 'Datos creados exitosamente!.')

            return redirect('usuario_app:edit_family_responsibilities', fr_id=object.fr_id, user_id=user_id, col_id=col_id)
        
        else:
            for field in formFamilyResponsibilitiesForm:
                for error in field.errors:
                    messages.error(request, f"{field.label}: {error}")
    else:
        formFamilyResponsibilitiesForm = FamilyResponsibilitiesForm()

    data = {
        'action': 'Crear',
        'form': formFamilyResponsibilitiesForm,
        'user_id': user_id,
        'col_id': col_id,
    }
    return render(request, 'client/page/usuario/forms/forms_family_responsibilities.html', data)


@login_required
def edit_family_responsibilities(request, fr_id, user_id, col_id):
    FamilyResponsibilitiesObject = get_object_or_404(FamilyResponsibilities, fr_id=fr_id)

    if request.method == 'POST':
        formFamilyResponsibilitiesForm = FamilyResponsibilitiesForm(request.POST, instance=FamilyResponsibilitiesObject)
        if formFamilyResponsibilitiesForm.is_valid():
            formFamilyResponsibilitiesForm.save()
            # Agregar mensaje de éxito
            messages.success(request, 'Datos editados exitosamente!.')
        else:
            for field in formFamilyResponsibilitiesForm:
                for error in field.errors:
                    messages.error(request, f"{field.label}: {error}")
    else:
        formFamilyResponsibilitiesForm = FamilyResponsibilitiesForm(instance=FamilyResponsibilitiesObject)

    data = {
        'form': formFamilyResponsibilitiesForm,
        'action': 'Editar',
        'user_id': user_id,
        'fr_id': fr_id,
        'col_id': col_id
    }
    return render(request, 'client/page/usuario/forms/forms_family_responsibilities.html', data)


@login_required
def family_responsibilities_delete(request, fr_id, user_id, col_id):
    object = FamilyResponsibilities.objects.get(fr_id=fr_id)
    object.fr_activo = 0
    object.save()
    return redirect('usuario_app:edit_collaborator_file', user_id, col_id)