from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from applications.base.models import Comuna, Pais, Region
from applications.configurations.forms import AfpForm, ApvForm, BanksForm, CajasCompensacionForm, ConceptsForm, MutualSecurityForm, SaludForm

from applications.empresa.models import Afp, Apv, Banco, CajasCompensacion, MutualSecurity, Salud
from applications.remuneracion.models import Concept
from applications.security.decorators import existsCompany


# Create your views here.

@login_required
@existsCompany
def countries(request):

    objects = Pais.objects.all()
    data = {
        'objects': objects,
        'action': 'Listar'
    }
    return render(request, 'client/page/tables/countries.html', data)


@login_required
@existsCompany
def regions(request):

    objects = Region.objects.all()
    data = {
        'objects': objects,
        'action': 'Listar'
    }
    return render(request, 'client/page/tables/regions.html', data)


@login_required
@existsCompany
def communes(request):

    objects = Comuna.objects.all()
    data = {
        'objects': objects,
        'action': 'Listar'
    }
    return render(request, 'client/page/tables/communes.html', data)


@login_required
@existsCompany
def afp(request):

    objects = Afp.objects.filter(afp_activo="S")
    data = {
        'objects': objects,
        'action': 'Listar'
    }
    return render(request, 'client/page/tables/afp.html', data)


@login_required
def afp_add(request):

    if request.method == 'POST':
        form = AfpForm(request.POST)
        if form.is_valid():
            object = form.save()
            # Agregar mensaje de éxito
            messages.success(request, 'Elemento creado exitosamente.')
            return redirect('conf_app:afp_edit', afp_id=object.afp_id)

        for field in form:
            for error in field.errors:
                messages.error(request, f"{field.label}: {error}")
    else:
        form = AfpForm()
    data = {
        'form': form,
        'action': 'Guardar'
    }
    return render(request, 'client/page/tables/forms/form_afp.html', data)


@login_required
def afp_edit(request, afp_id):
    object = get_object_or_404(Afp, afp_id=afp_id)
    if request.method == 'POST':
        form = AfpForm(request.POST, instance=object)
        if form.is_valid():
            form.save()
            # Agregar mensaje de éxito
            messages.success(request, 'Elemento editado exitosamente.')
        else:
            for field in form:
                for error in field.errors:
                    messages.error(request, f"{field.label}: {error}")
    else:
        form = AfpForm(instance=object)

    data = {
        'form': form,
        'action': 'Editar',
        'afp_id': afp_id,
    }
    return render(request, 'client/page/tables/forms/form_afp.html', data)


@login_required
def afp_delete(request, afp_id):
    object = Afp.objects.get(afp_id=afp_id)
    object.afp_activo = 'N'
    object.save()
    return redirect('conf_app:afp_app')


@login_required
@existsCompany
def health(request):

    objects = Salud.objects.filter(sa_activo="S")
    data = {
        'objects': objects,
        'action': 'Listar'
    }
    return render(request, 'client/page/tables/health.html', data)


@login_required
def health_add(request):

    if request.method == 'POST':
        form = SaludForm(request.POST)
        if form.is_valid():
            object = form.save()
            # Agregar mensaje de éxito
            messages.success(request, 'Elemento creado exitosamente.')
            return redirect('conf_app:health_edit', sa_id=object.sa_id)

        lista_err = []
        for field in form:
            for error in field.errors:
                messages.error(request, f"{field.label}: {error}")
    else:
        form = SaludForm()
    data = {
        'form': form,
        'action': 'Guardar'
    }
    return render(request, 'client/page/tables/forms/form_health.html', data)


@login_required
def health_edit(request, sa_id):
    object = get_object_or_404(Salud, sa_id=sa_id)
    if request.method == 'POST':
        form = SaludForm(request.POST, instance=object)
        if form.is_valid():
            form.save()
            # Agregar mensaje de éxito
            messages.success(request, 'Elemento editado exitosamente.')
        else:
            for field in form:
                for error in field.errors:
                    messages.error(request, f"{field.label}: {error}")
    else:
        form = SaludForm(instance=object)

    data = {
        'form': form,
        'action': 'Editar',
        'sa_id': sa_id,
    }
    return render(request, 'client/page/tables/forms/form_health.html', data)


@login_required
def health_delete(request, sa_id):
    object = Salud.objects.get(sa_id=sa_id)
    object.sa_activo = 'N'
    object.save()
    return redirect('conf_app:health_app')


@login_required
@existsCompany
def compensation_box(request):

    objects = CajasCompensacion.objects.filter(cc_activo="S")
    data = {
        'objects': objects,
        'action': 'Listar'
    }
    return render(request, 'client/page/tables/compensation_box.html', data)


@login_required
def compensation_box_add(request):

    if request.method == 'POST':
        form = CajasCompensacionForm(request.POST)
        if form.is_valid():
            object = form.save()
            # Agregar mensaje de éxito
            messages.success(request, 'Elemento creado exitosamente.')
            return redirect('conf_app:compensation_box_edit', cc_id=object.cc_id)

        lista_err = []
        for field in form:
            for error in field.errors:
                lista_err.append(field.label + ': ' + error)
    else:
        form = CajasCompensacionForm()
    data = {
        'form': form,
        'action': 'Guardar'
    }
    return render(request, 'client/page/tables/forms/form_compensation_box.html', data)


@login_required
def compensation_box_edit(request, cc_id):
    object = get_object_or_404(CajasCompensacion, cc_id=cc_id)
    if request.method == 'POST':
        form = CajasCompensacionForm(request.POST, instance=object)
        if form.is_valid():
            form.save()
            # Agregar mensaje de éxito
            messages.success(request, 'Elemento editado exitosamente.')
        else:
            for field in form:
                for error in field.errors:
                    messages.error(request, f"{field.label}: {error}")
    else:
        form = CajasCompensacionForm(instance=object)

    data = {
        'form': form,
        'action': 'Editar',
        'cc_id': cc_id,
    }
    return render(request, 'client/page/tables/forms/form_compensation_box.html', data)


@login_required
def compensation_box_delete(request, cc_id):
    object = CajasCompensacion.objects.get(cc_id=cc_id)
    object.cc_activo = 'N'
    object.save()
    return redirect('conf_app:compensation_box_app')


@login_required
@existsCompany
def banks(request):

    list_banks = Banco.objects.filter(ban_activo="S")
    data = {
        'list_banks': list_banks,
        'action': 'Listar'
    }
    return render(request, 'client/page/tables/banks.html', data)


@login_required
def banks_add(request):

    if request.method == 'POST':
        form = BanksForm(request.POST)
        if form.is_valid():
            object = form.save()
            # Agregar mensaje de éxito
            messages.success(request, 'Elemento creado exitosamente.')
            return redirect('conf_app:banks_edit', ban_id=object.ban_id)

        lista_err = []
        for field in form:
            for error in field.errors:
                lista_err.append(field.label + ': ' + error)
    else:
        form = BanksForm()
    data = {
        'form': form,
        'action': 'Guardar'
    }
    return render(request, 'client/page/tables/forms/form_bank.html', data)


@login_required
def banks_edit(request, ban_id):
    object = get_object_or_404(Banco, ban_id=ban_id)
    if request.method == 'POST':
        form = BanksForm(request.POST, instance=object)
        if form.is_valid():
            form.save()
            # Agregar mensaje de éxito
            messages.success(request, 'Elemento editado exitosamente.')
    else:
        form = BanksForm(instance=object)

    data = {
        'form': form,
        'action': 'Editar',
        'ban_id': ban_id,
    }
    return render(request, 'client/page/tables/forms/form_bank.html', data)


@login_required
def delete_bank(request, ban_id):
    object = Banco.objects.get(ban_id=ban_id)
    object.ban_activo = 'N'
    object.save()
    return redirect('conf_app:banks_app')


@login_required
@existsCompany
def apv(request):

    objects = Apv.objects.filter(apv_activo="S")
    data = {
        'objects': objects,
        'action': 'Listar'
    }

    return render(request, 'client/page/tables/apv.html', data)


@login_required
def apv_add(request):

    if request.method == 'POST':
        form = ApvForm(request.POST)
        if form.is_valid():
            object = form.save()
            # Agregar mensaje de éxito
            messages.success(request, 'Elemento creado exitosamente.')
            return redirect('conf_app:apv_edit', apv_id=object.apv_id)

        for field in form:
            for error in field.errors:
                messages.error(request, f"{field.label}: {error}")
    else:
        form = ApvForm()
    data = {
        'form': form,
        'action': 'Guardar'
    }
    return render(request, 'client/page/tables/forms/form_apv.html', data)


@login_required
def apv_edit(request, apv_id):
    object = get_object_or_404(Apv, apv_id=apv_id)
    if request.method == 'POST':
        form = ApvForm(request.POST, instance=object)
        if form.is_valid():
            form.save()
            # Agregar mensaje de éxito
            messages.success(request, 'Elemento editado exitosamente.')
        else:
            for field in form:
                for error in field.errors:
                    messages.error(request, f"{field.label}: {error}")
    else:
        form = ApvForm(instance=object)

    data = {
        'form': form,
        'action': 'Editar',
        'apv_id': apv_id,
    }
    return render(request, 'client/page/tables/forms/form_apv.html', data)


@login_required
def apv_delete(request, apv_id):
    object = Apv.objects.get(apv_id=apv_id)
    object.apv_activo = 'N'
    object.save()
    return redirect('conf_app:apv_app')


@login_required
@existsCompany
def mutual_security(request):

    objects = MutualSecurity.objects.filter(ms_active="S")
    data = {
        'objects': objects,
        'action': 'Listar'
    }

    return render(request, 'client/page/tables/mutual_security.html', data)


@login_required
def mutual_security_add(request):

    if request.method == 'POST':
        form = MutualSecurityForm(request.POST)
        if form.is_valid():
            object = form.save()
            # Agregar mensaje de éxito
            messages.success(request, 'Elemento creado exitosamente.')
            return redirect('conf_app:mutual_security_edit', ms_id=object.ms_id)

        for field in form:
            for error in field.errors:
                messages.error(request, f"{field.label}: {error}")
    else:
        form = MutualSecurityForm()
    data = {
        'form': form,
        'action': 'Guardar'
    }
    return render(request, 'client/page/tables/forms/form_mutual_security.html', data)


@login_required
def mutual_security_edit(request, ms_id):

    object = get_object_or_404(MutualSecurity, ms_id=ms_id)
    if request.method == 'POST':
        form = MutualSecurityForm(request.POST, instance=object)
        if form.is_valid():
            form.save()
            # Agregar mensaje de éxito
            messages.success(request, 'Elemento editado exitosamente.')
        else:
            for field in form:
                for error in field.errors:
                    messages.error(request, f"{field.label}: {error}")
    else:
        form = MutualSecurityForm(instance=object)

    data = {
        'form': form,
        'action': 'Editar',
        'ms_id': ms_id,
    }
    return render(request, 'client/page/tables/forms/form_mutual_security.html', data)


@login_required
def mutual_security_delete(request, ms_id):
    object = MutualSecurity.objects.get(ms_id=ms_id)
    object.ms_active = 'N'
    object.save()
    return redirect('conf_app:mutual_security_app')


@login_required
@existsCompany
def concepts(request):

    objects = Concept.objects.filter(conc_active="S")
    data = {
        'objects': objects,
        'action': 'Listar'
    }

    return render(request, 'client/page/tables/concepts.html', data)


@login_required
def concepts_add(request):

    if request.method == 'POST':
        form = ConceptsForm(request.POST)
        if form.is_valid():
            object = form.save()
            # Agregar mensaje de éxito
            messages.success(request, 'Concepto creado exitosamente.')
            return redirect('conf_app:concepts_edit', conc_id=object.conc_id)

        for field in form:
            for error in field.errors:
                messages.error(request, f"{field.label}: {error}")
    else:
        form = ConceptsForm()
    data = {
        'form': form,
        'action': 'Guardar'
    }
    return render(request, 'client/page/tables/forms/form_concepts.html', data)


@login_required
def concepts_edit(request, conc_id):

    object = get_object_or_404(Concept, conc_id=conc_id)
    if request.method == 'POST':
        form = ConceptsForm(request.POST, instance=object)
        if form.is_valid():
            form.save()
            # Agregar mensaje de éxito
            messages.success(request, 'Concepto editado exitosamente.')
        else:
            for field in form:
                for error in field.errors:
                    messages.error(request, f"{field.label}: {error}")
    else:
        form = ConceptsForm(instance=object)

    data = {
        'form': form,
        'action': 'Editar',
        'conc_id': conc_id,
    }
    return render(request, 'client/page/tables/forms/form_concepts.html', data)


@login_required
def concepts_delete(request, conc_id):
    object = Concept.objects.get(conc_id=conc_id)
    object.conc_active = 'N'
    object.save()
    return redirect('conf_app:concepts_app')