from django.contrib.auth.models import Group
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from services.decorators import unauthenticated_user, allowed_users
from services.models import *
from django.conf import settings
import services.utilities as utl


@unauthenticated_user
def login(request):
    next_url = request.GET.get('next')
    context = None if next_url is None else {'next': next_url}
    if 'redirect-context' in request.session:
        if context is not None:
            context.update(request.session['redirect-context'])
        else:
            context = request.session['redirect-context']

        del request.session['redirect-context']

    return render(request, 'login.html', context)


# Create your views here.
@login_required
def index(request):
    if request.user.is_anonymous:
        return render(request, 'login.html')
    else:
        context = {'content_title': settings.CONTENT_TITLE.DASHBOARD}

        if utl.Groups.issuer in utl.get_user_group_names(request.user):
            return render(request, 'index.html', context)
        else:
            return render(request, 'index-for-awardee.html', context)


@login_required
@allowed_users(allowed_roles=[utl.Groups.issuer])
def templates(request):
    context = {'content_title': settings.CONTENT_TITLE.TEMPLATES,
               'templates': Template.objects.all()}
    return render(request, 'templates.html', context)


@login_required
@allowed_users(allowed_roles=[utl.Groups.issuer])
def awardees(request):
    awardee_group = Group.objects.get(name=utl.Groups.awardee)
    context = {'content_title': settings.CONTENT_TITLE.AWARDEES,
               'awardees': User.objects.filter(groups__in=[awardee_group]).order_by('first_name', 'last_name')}
    return render(request, 'awardees.html', context)


@login_required
@allowed_users(allowed_roles=[utl.Groups.issuer])
def certificates(request):
    context = {'content_title': settings.CONTENT_TITLE.CERTIFICATES,
               'certificates': Certificate.objects.all().order_by('-created_on')}
    return render(request, 'certificates.html', context)


@login_required
@allowed_users(allowed_roles=[utl.Groups.awardee])
def my_certificates(request):
    context = {'content_title': settings.CONTENT_TITLE.MY_CERTIFICATES,
               'certificates': Certificate.objects.filter(awardee=request.user).order_by('-created_on')}
    return render(request, 'certificates\my-certificates.html', context)


@login_required
@allowed_users(allowed_roles=[utl.Groups.issuer])
def certificates_setup(request, pk=None):
    event = Event.objects.get(pk=pk) if pk is not None else None
    context = {'content_title': settings.CONTENT_TITLE.CERTIFICATE_SETUP,
               'event': event,
               'templates': Template.objects.all(),
               'datasheets': DataSheet.objects.all(), }
    return render(request, r'certificates\certificate_setup.html', context)


@login_required
@allowed_users(allowed_roles=[utl.Groups.issuer])
def certificates_generate(request):
    context = {'content_title': settings.CONTENT_TITLE.CERTIFICATE_GENERATE,
               'events': Event.objects.all()}
    return render(request, 'certificates\certificate_generate.html', context)


@login_required
@allowed_users(allowed_roles=[utl.Groups.issuer])
def certificates_generated(request):
    context = {'content_title': settings.CONTENT_TITLE.CERTIFICATE_GENERATED,
               'events': Event.objects.filter(are_certificates_generated=True).all()}
    return render(request, 'certificates\past_certificates.html', context)

# class CertificateTableView(tables.SingleTableView):
#     table_class = CertificateTable
#     queryset = Certificate.objects.all()
#     template_name = "certificates.html"
