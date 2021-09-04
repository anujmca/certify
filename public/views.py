from django.db.models import Sum
from django.http import HttpResponse, FileResponse
from django.shortcuts import render

from common.utilities import path_leaf
from public.models import PublicCertificate, PublicUser
from services.decorators import unauthenticated_user, allowed_users, public


# from django.contrib.auth import get_user_model
#
# User = get_user_model()

# Create your views here.

def update_download_counter(certificate, request):
    try:
        if request.user == certificate.awardee:
            certificate.download_by_awardee_count += 1
        else:
            certificate.download_by_public_count += 1
        certificate.save()
    except Exception as ex:
        print(str(ex))


@public
def public_dashboard(request):
    my_certificates = PublicCertificate.objects.filter(awardee=request.user)
    certificate_count = my_certificates.count()
    issuer_count = my_certificates.values('tenant_schema_name').distinct().count()
    download_by_awardee_count = my_certificates.aggregate(Sum('download_by_awardee_count'))['download_by_awardee_count__sum']
    download_by_public_count = my_certificates.aggregate(Sum('download_by_public_count'))['download_by_public_count__sum']

    context = {'content_title': 'Dashboard',
               'certificate_count': certificate_count,
               'issuer_count': issuer_count,
               'download_by_awardee_count': download_by_awardee_count,
               'download_by_public_count': download_by_public_count}
    return render(request, 'public/public_dashboard.html', context=context)


@public
def public_certificate_download(request, pk):
    certificate = PublicCertificate.objects.get(pk=pk)
    filename = path_leaf(certificate.file.name)
    response = HttpResponse(certificate.file,
                            content_type='application/vnd.ms-powerpoint|application/vnd.openxmlformats-officedocument.presentationml.presentation')
    response['Content-Disposition'] = 'attachment; filename=%s' % filename

    update_download_counter(certificate, request)
    return response


@public
def public_certificate_view_raw(request, pk):
    certificate = PublicCertificate.objects.get(pk=pk)
    response = FileResponse(open(certificate.file.name, 'rb'), content_type='application/pdf')

    update_download_counter(certificate, request)
    return response


@public
def public_certificate_view(request, pk):
    certificate = PublicCertificate.objects.get(pk=pk)
    context = {'content_title': 'Authorised Certificate',
               'certificate': certificate}

    # update_download_counter(certificate, request)
    return render(request, 'unauthenticated/certificate_view.html', context=context)
