from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from app01.functions import getLatitudeLongitude
from applications.empresa.forms import AssociatedEntitiesForm, CargoForm, CentroCostoForm, EmpresaForm, GrupoCentroCostoForm, SucursalForm
from applications.empresa.models import CajasCompensacion, Cargo, CentroCosto, Empresa, GrupoCentroCosto, MutualSecurity, Sucursal

# Create your views here.


@login_required
def list_company(request):

    list_companys = Empresa.objects.filter(emp_activa='S')

    data = {
        'list_companys': list_companys
    }
    return render(request, 'client/page/company/list_company.html', data)


@login_required
def add_company(request):

    if request.method == 'POST':
        form = EmpresaForm(request.POST, request.FILES)
        if form.is_valid():
            company = form.save(commit=False)

            address = f"{ company.emp_direccion } { company.emp_numero }, { company.comuna.com_nombre }, { company.region.re_nombre }, { company.pais.pa_nombre }"
            lat, lng = getLatitudeLongitude(address)

            company.emp_latitude = str(lat)
            company.emp_longitude = str(lng)
            company.save()

            suc = Sucursal()
            suc.suc_descripcion = "Casa Matriz"
            suc.empresa = company
            suc.suc_direccion = address
            suc.pais = company.pais
            suc.region = company.region
            suc.comuna = company.comuna
            suc.suc_latitude = str(lat)
            suc.suc_longitude = str(lng)
            suc.suc_matrixhouse = "S"
            suc.save()

            messages.success(request, 'Empresa creada exitosamente.')
            return redirect('emp_app:edit_company', emp_id=company.emp_id)

        for field in form:
            for error in field.errors:
                messages.error(request, f"{field.label}: {error}")
    else:
        form = EmpresaForm()

    data = {
        'action': 'Crear',
        'form': form,
    }
    return render(request, 'client/page/company/add_company.html', data)


@login_required
def edit_company(request, emp_id):
    company = get_object_or_404(Empresa, emp_id=emp_id)
    if request.method == 'POST':
        form = EmpresaForm(request.POST, request.FILES, instance=company)
        if form.is_valid():
            com = form.save(commit=False)

            address = f"{ company.emp_direccion } { company.emp_numero }, { company.comuna.com_nombre }, { company.region.re_nombre }, { company.pais.pa_nombre }"
            lat, lng = getLatitudeLongitude(address)

            com.emp_latitude = str(lat)
            com.emp_longitude = str(lng)
            com.save()

            suc = Sucursal.objects.get(suc_matrixhouse = "S", empresa = company, suc_estado = "S")
            suc.suc_direccion = f"{ company.emp_direccion } { company.emp_numero }"
            suc.pais = company.pais
            suc.region = company.region
            suc.comuna = company.comuna
            suc.suc_latitude = str(lat)
            suc.suc_longitude = str(lng)
            suc.save()

    else:
        form = EmpresaForm(instance=company)

    list_branch_offices = Sucursal.objects.filter(suc_estado='S')
    list_positions = Cargo.objects.filter(
        car_activa='S', empresa__emp_id=emp_id)
    list_gcc = GrupoCentroCosto.objects.filter(
        gcencost_activo='S', empresa__emp_id=emp_id)
    
    list_associated_entities = []
    if company.mutualSecurity:
        list_associated_entities.append({
            "id": 1 ,
            "name": company.mutualSecurity.ms_name,
            "rut": company.mutualSecurity.ms_rut
        })

    if company.cajasCompensacion:
        list_associated_entities.append({
            "id": 2,
            "name": company.cajasCompensacion.cc_nombre,
            "rut": company.cajasCompensacion.cc_rut 
        })
    

    data = {
        'form': form,
        'form_position': CargoForm(),
        'form_gcc': GrupoCentroCostoForm(),
        'action': 'Editar',
        'emp_id': emp_id,
        'image': company.emp_imagenempresa,
        'list_branch_offices': list_branch_offices,
        'list_positions': list_positions,
        'list_gcc': list_gcc,
        'list_associated_entities': list_associated_entities,
        'length_list_associated_entities': len(list_associated_entities)
    }
    return render(request, 'client/page/company/add_company.html', data)


@login_required
def add_branch_office(request, emp_id):
    if request.method == 'POST':
        form = SucursalForm(request.POST)
        if form.is_valid():
            branch_office = form.save(commit=False)
            branch_office.empresa = Empresa.objects.get(emp_id=emp_id)

            address = f"{ branch_office.suc_direccion }, { branch_office.comuna.com_nombre }, { branch_office.region.re_nombre }, { branch_office.pais.pa_nombre }"
            lat, lng = getLatitudeLongitude(address)

            branch_office.suc_latitude = str(lat)
            branch_office.suc_longitude = str(lng)
            branch_office.save()

            # Agregar mensaje de éxito
            messages.success(request, 'Sucursal creada exitosamente.')
            return redirect('emp_app:edit_branch_office', emp_id=emp_id, suc_id=branch_office.suc_id)
        else:
            for field in form:
                for error in field.errors:
                    messages.error(request, f"{field.label}: {error}")
    else:
        form = SucursalForm()

    data = {
        'action': 'Crear',
        'form_branch': form,
        'emp_id': emp_id
    }
    return render(request, 'client/page/company/branchs_office.html', data)


@login_required
def edit_branch_office(request, emp_id, suc_id):
    branch = get_object_or_404(Sucursal, suc_id=suc_id)

    if request.method == 'POST':
        form = SucursalForm(request.POST, instance=branch)
        if form.is_valid():
            branch_office = form.save(commit=False)

            address = f"{ branch_office.suc_direccion }, { branch_office.comuna.com_nombre }, { branch_office.region.re_nombre }, { branch_office.pais.pa_nombre }"
            lat, lng = getLatitudeLongitude(address)

            branch_office.suc_latitude = str(lat)
            branch_office.suc_longitude = str(lng)
            branch_office.save()
            # Agregar mensaje de éxito
            messages.success(request, 'Sucursal editada exitosamente.')
        else:
            for field in form:
                for error in field.errors:
                    messages.error(request, f"{field.label}: {error}")
    else:
        form = SucursalForm(instance=branch)

    data = {
        'form_branch': form,
        'action': 'Editar',
        'emp_id': emp_id,
        'suc_id': suc_id,
    }
    return render(request, 'client/page/company/branchs_office.html', data)


@login_required
def delete_branch_office(request, emp_id, suc_id):
    branch_office = Sucursal.objects.get(suc_id=suc_id)
    branch_office.suc_estado = 'N'
    branch_office.save()
    return redirect('emp_app:edit_company', emp_id)


@login_required
def add_position(request, emp_id):
    if request.method == 'POST':
        form = CargoForm(request.POST)
        if form.is_valid():
            position = form.save(commit=False)
            empresa = Empresa.objects.get(emp_id=emp_id)

            position.save()
            # Utilizar el método set() para establecer la relación
            position.empresa.set([empresa])

            form.save_m2m()
            # Agregar mensaje de éxito
            messages.success(request, 'Cargo creado exitosamente.')
            return redirect('emp_app:edit_position', emp_id=emp_id, car_id=position.car_id)
        else:
            for field in form:
                for error in field.errors:
                    messages.error(request, f"{field.label}: {error}")
            # Aquí puedes agregar un mensaje de error si es necesario
    else:
        form = CargoForm()

    data = {
        'action': 'Crear',
        'form': form,
        'emp_id': emp_id
    }
    return render(request, 'client/page/company/position.html', data)


@login_required
def edit_position(request, emp_id, car_id):
    position = get_object_or_404(Cargo, car_id=car_id)

    if request.method == 'POST':
        form = CargoForm(request.POST, instance=position)
        if form.is_valid():
            form.save()
            # Agregar mensaje de éxito
            messages.success(request, 'Cargo editado exitosamente.')
        else:
            for field in form:
                for error in field.errors:
                    messages.error(request, f"{field.label}: {error}")
    else:
        form = CargoForm(instance=position)

    data = {
        'form': form,
        'action': 'Editar',
        'emp_id': emp_id,
        'car_id': car_id
    }
    return render(request, 'client/page/company/position.html', data)


@login_required
def delete_position(request, emp_id, car_id):
    position = Cargo.objects.get(car_id=car_id)
    position.car_activa = 'N'
    position.save()
    return redirect('emp_app:edit_company', emp_id)


@login_required
def add_gcc(request, emp_id):
    if request.method == 'POST':
        form = GrupoCentroCostoForm(request.POST)
        if form.is_valid():
            position = form.save(commit=False)
            position.empresa = Empresa.objects.get(emp_id=emp_id)

            position.save()

            # Agregar mensaje de éxito
            messages.success(
                request, 'Grupo Centro Costo creado exitosamente.')
            return redirect('emp_app:edit_gcc', emp_id=emp_id, gcencost_id=position.gcencost_id)
        else:
            for field in form:
                for error in field.errors:
                    messages.error(request, f"{field.label}: {error}")
    else:
        form = GrupoCentroCostoForm()

    data = {
        'action': 'Crear',
        'form': form,
        'emp_id': emp_id,
    }
    return render(request, 'client/page/company/gcc.html', data)


@login_required
def edit_gcc(request, emp_id, gcencost_id):
    position = get_object_or_404(GrupoCentroCosto, gcencost_id=gcencost_id)

    if request.method == 'POST':
        form = GrupoCentroCostoForm(request.POST, instance=position)
        if form.is_valid():
            form.save()
            # Agregar mensaje de éxito
            messages.success(
                request, 'Grupo Centro Costo editado exitosamente.')
        else:
            for field in form:
                for error in field.errors:
                    messages.error(request, f"{field.label}: {error}")
    else:
        form = GrupoCentroCostoForm(instance=position)

    list_cc = CentroCosto.objects.filter(
        grupocentrocosto__gcencost_id=gcencost_id, cencost_activo="S")

    data = {
        'form': form,
        'action': 'Editar',
        'emp_id': emp_id,
        'gcencost_id': gcencost_id,
        'list_cc': list_cc
    }
    return render(request, 'client/page/company/gcc.html', data)


@login_required
def delete_gcc(request, emp_id, gcencost_id):
    position = GrupoCentroCosto.objects.get(gcencost_id=gcencost_id)
    position.gcencost_activo = 'N'
    position.save()
    return redirect('emp_app:edit_company', emp_id)


@login_required
def add_cc(request, emp_id, gcencost_id):
    lista_err = []
    objects_GCC = GrupoCentroCosto.objects.get(gcencost_id=gcencost_id)
    if request.method == 'POST':
        form = CentroCostoForm(request.POST)
        if form.is_valid():
            position = form.save(commit=False)
            position.grupocentrocosto = objects_GCC

            position.save()

            # Agregar mensaje de éxito
            messages.success(
                request, 'Grupo Centro Costo creado exitosamente.')
            return redirect('emp_app:edit_cc', emp_id=emp_id, gcencost_id=gcencost_id, cencost_id=position.cencost_id)
        else:
            for field in form:
                for error in field.errors:
                    lista_err.append(field.label + ': ' + error)
            # Aquí puedes agregar un mensaje de error si es necesario
    else:
        form = CentroCostoForm()

    data = {
        'action': 'Crear',
        'form': form,
        'gcencost_id': gcencost_id,
        'emp_id': emp_id,
        'lista_err': lista_err,
        'name_gcc': objects_GCC.gcencost_nombre.upper()
    }
    return render(request, 'client/page/company/cc.html', data)


@login_required
def edit_cc(request, emp_id, gcencost_id, cencost_id):
    position = get_object_or_404(CentroCosto, cencost_id=cencost_id)

    if request.method == 'POST':
        form = CentroCostoForm(request.POST, instance=position)
        if form.is_valid():
            form.save()
            # Agregar mensaje de éxito
            messages.success(
                request, 'Grupo Centro Costo editado exitosamente.')
        else:
            # Aquí puedes agregar un mensaje de error si es necesario
            pass
    else:
        form = CentroCostoForm(instance=position)

    data = {
        'form': form,
        'action': 'Editar',
        'gcencost_id': gcencost_id,
        'cencost_id': cencost_id,
        'emp_id': emp_id,
        'name_gcc': position.grupocentrocosto.gcencost_nombre.upper()
    }
    return render(request, 'client/page/company/cc.html', data)


@login_required
def delete_cc(request, emp_id, gcencost_id, cencost_id):
    position = CentroCosto.objects.get(cencost_id=cencost_id)
    position.cencost_activo = 'N'
    position.save()
    return redirect('emp_app:edit_gcc', emp_id, gcencost_id)


@login_required
def add_associated_entities(request, emp_id):
    position = get_object_or_404(Empresa, emp_id=emp_id)

    if request.method == 'POST':
        
        form = AssociatedEntitiesForm(request.POST, instance=position)
        if form.is_valid():
            company = form.save(commit=False)
            company.mutualSecurity = MutualSecurity.objects.get(ms_id=request.POST['mutualSecurity'])
            company.cajasCompensacion = CajasCompensacion.objects.get(cc_id=request.POST['cajasCompensacion'])
            company.save()

            # Agregar mensaje de éxito
            messages.success(request, 'Creación exitosa.')
        else:
            for field in form:
                for error in field.errors:
                    messages.error(request, f"{field.label}: {error}")
    else:
        form = AssociatedEntitiesForm(instance=position)

    data = {
        'action': 'Crear',
        'form': form,
        'emp_id': emp_id
    }
    return render(request, 'client/includes/company/form_associated_entities.html', data)