from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from applications.usuario.forms import ColaboradorForm, ContactForm, UserForm
from django.contrib.auth.models import User

from applications.usuario.models import Colaborador, Contact

# Create your views here.

@login_required
def collaborator_file(request):

    list_objects = Colaborador.objects.filter(col_activo=1)

    data = {
        'list_objects': list_objects
    }
    return render(request, 'client/page/usuario/collaborator_file.html', data)


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
            colaborador.save()

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

    if request.method == 'POST':
        formUserForm = UserForm(request.POST, instance=user)
        formColaboradorForm = ColaboradorForm(request.POST, instance=colaborador)

        if formUserForm.is_valid() and formColaboradorForm.is_valid():
            user = formUserForm.save(commit=False)

            # Establecer la contraseña utilizando el valor de colaborador.col_rut
            password = colaborador.col_rut
            hashed_password = make_password(password)
            user.password = hashed_password
            user.save()

            colaborador = formColaboradorForm.save(commit=False)
            colaborador.user = user
            colaborador.save()

            messages.success(request, 'Datos personales editados exitosamente!.')

    else:
        formUserForm = UserForm(instance=user)
        formColaboradorForm = ColaboradorForm(instance=colaborador)

    list_contact = Contact.objects.filter(con_actiove="S")

    data = {
        'action': 'Editar',
        'formUserForm': formUserForm,
        'formColaboradorForm': formColaboradorForm,
        'id': id,
        'col_id': col_id,
        'list_contact': list_contact,
        'colaborador': colaborador
    }
    return render(request, 'client/page/usuario/add_collaborator_file.html', data)


"""@login_required
def mutual_security_delete(request, ms_id):
    object = MutualSecurity.objects.get(ms_id=ms_id)
    object.ms_active = 'N'
    object.save()
    return redirect('conf_app:mutual_security_app')"""



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