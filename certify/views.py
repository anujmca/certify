from django.contrib.auth.models import Group
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from public.models import PublicCertificate, PublicUser
from services.decorators import unauthenticated_user, allowed_users, public
from services.models import *
from django.conf import settings
import services.utilities as utl
from django_tenants.utils import schema_context, connection
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _


User = get_user_model()


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
            templates_total = Template.objects.count()
            templates_used = Event.objects.values('template').distinct().count()

            events_total = Event.objects.count()
            events_generated = Event.objects.filter(are_certificates_generated=True).count()

            certificates_total = Certificate.objects.count()
            certificates_published = Certificate.objects.filter(status=Certificate.STATUSES.PUBLISHED).count()

            awardee_total = len(get_awardees())
            awardee_downloaded = 0

            with schema_context(settings.PUBLIC_SCHEMA_NAME):
                awardee_downloaded = PublicCertificate.objects.filter(download_by_awardee_count__gt=0).values('awardee').distinct().count()

            context = {**context, **{
                'templates': {'used': templates_used, 'total': templates_total},
                'events': {'generated': events_generated, 'total': events_total},
                'certificates': {'published': certificates_published, 'total': certificates_total},
                'awardee': {'downloaded': awardee_downloaded, 'total': awardee_total}
                }
            }
            return render(request, 'index.html', context)
        else:
            return redirect('/public/dashboard')


@login_required
@allowed_users(allowed_roles=[utl.Groups.issuer])
def events(request):
    context = {'content_title': settings.CONTENT_TITLE.EVENTS,
               'events': Event.objects.all()}
    return render(request, 'events/event_list.html', context)


@login_required
@allowed_users(allowed_roles=[utl.Groups.issuer])
def templates(request):
    context = {'content_title': settings.CONTENT_TITLE.TEMPLATES,
               'templates': Template.objects.all()}
    return render(request, 'templates/templates_list.html', context)


@login_required
@allowed_users(allowed_roles=[utl.Groups.issuer])
def datasheets(request):
    context = {'content_title': settings.CONTENT_TITLE.DATASHEETS,
               'datasheets': DataSheet.objects.all()}
    return render(request, 'datasheets/datasheet_list.html', context)


@login_required
@allowed_users(allowed_roles=[utl.Groups.issuer])
def awardees(request):
    awardee_list = get_awardees()

    context = {'content_title': settings.CONTENT_TITLE.AWARDEES,
               'awardees': awardee_list}
    return render(request, 'awardees.html', context)


def get_awardees():
    tenant_schema_name = connection.schema_name
    # with schema_context(settings.PUBLIC_SCHEMA_NAME):
    awardee_group = Group.objects.get(name=utl.Groups.awardee)
    # awardee_list = list(
    #     PublicUser.objects.filter(tenant_schema_name=tenant_schema_name, groups__in=[awardee_group]).order_by(
    #         'first_name', 'last_name'))
    # awardee_list = set([c.awardee for c in PublicCertificate.objects.filter(tenant_schema_name=tenant_schema_name)])
    awardee_list = []
    with schema_context(settings.PUBLIC_SCHEMA_NAME):
        for pu in PublicUser.objects.all():
            if pu.get_tenant_specific_certificates(tenant_schema_name).exists():
                awardee_list.append(pu)
    return awardee_list

#
# def get_published_certificates():
#     tenant_schema_name = connection.schema_name
#     awardee_group = Group.objects.get(name=utl.Groups.awardee)
#     certificate_list = []
#     with schema_context(settings.PUBLIC_SCHEMA_NAME):
#         for pu in PublicCertificate.objects.all():
#             if pu.get_tenant_specific_certificates(tenant_schema_name).exists():
#                 awardee_list.append(pu)
#     return awardee_list

@login_required
@allowed_users(allowed_roles=[utl.Groups.issuer])
def certificates(request):
    context = {'content_title': settings.CONTENT_TITLE.CERTIFICATES,
               'certificates': Certificate.objects.all().order_by('-created_on')}
    return render(request, 'certificates.html', context)


@login_required
@allowed_users(allowed_roles=[utl.Groups.issuer])
def event_certificates(request, pk):
    event = Event.objects.get(pk=pk)
    context = {'content_title': settings.CONTENT_TITLE.CERTIFICATES,
               'certificates': event.certificates.all().order_by('-created_on')}
    return render(request, 'certificates.html', context)


@login_required
@allowed_users(allowed_roles=[utl.Groups.awardee])
def my_certificates(request):
    from public.models import PublicCertificate
    tenant_schema_name = connection.schema_name

    # with schema_context(settings.PUBLIC_SCHEMA_NAME):
    context = {'content_title': settings.CONTENT_TITLE.MY_CERTIFICATES,
               'certificates':
                   PublicCertificate.objects.filter(awardee=request.user).order_by('-created_on')
                   if tenant_schema_name == settings.PUBLIC_SCHEMA_NAME
                   else PublicCertificate.objects.filter(tenant_schema_name=tenant_schema_name,
                                                         awardee__id=request.user.public_user_id).order_by('-created_on')
               }

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
    return render(request, 'certificates/certificate_generate.html', context)


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
