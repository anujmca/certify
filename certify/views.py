from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from services.models import *

def login(request):
    next_url = request.GET.get('next')
    context = None if next_url is None else {'next' : next_url}
    return render(request, 'login.html', context)


# Create your views here.
def index(request):
    if request.user.is_anonymous:
        return render(request, 'login.html')
    else:
        context = {'content_title': 'Dashboard'}
        return render(request, 'index.html', context)


@login_required
def templates(request):
    context = {'content_title': 'Templates',
               'templates': Template.objects.all()}
    return render(request, 'templates.html', context)


@login_required
def employees(request):
    context = {'content_title': 'Employees'}
    return render(request, 'employees.html', context)


@login_required
def certificates(request):
    context = {'content_title': 'Certificates',
               'certificates': Certificate.objects.all()}
    return render(request, 'certificates.html', context)


# class CertificateTableView(tables.SingleTableView):
#     table_class = CertificateTable
#     queryset = Certificate.objects.all()
#     template_name = "certificates.html"
