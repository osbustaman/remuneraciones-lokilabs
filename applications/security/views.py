from django.contrib.auth.decorators import login_required
from django.shortcuts import render


# Create your views here.


@login_required
def error404(request):
    data = {
        'message': 'la petición es correcta pero el servidor se niega a ofrecerle el recurso o página web. Ya que debe existir a lo menos una empresa ingresada'
    }
    return render(request, 'errors/404.html', data)