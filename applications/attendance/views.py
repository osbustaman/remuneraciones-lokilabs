from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from applications.security.decorators import existsCompany

# Create your views here.

@login_required
def work_day_report(request, user_id):

    data = {

    }
    return render(request, 'client/page/remunerations/page/work_day_report.html', data)


@login_required
def collaborators_working_day(request):

    data = {

    }
    return render(request, 'client/page/remunerations/page/collaborators_working_day.html', data)


# Create your views here.
@login_required
@existsCompany
def mark_in_out(request):


    data = {

    }
    return render(request, 'client/page/usuario/forms/from_mark_in_out.html', data)