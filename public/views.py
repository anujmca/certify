from django.http import HttpResponse, FileResponse
from django.shortcuts import render

from common.utilities import path_leaf
from public.models import PublicCertificate, PublicUser
from services.decorators import unauthenticated_user, allowed_users, public


# from django.contrib.auth import get_user_model
#
# User = get_user_model()

# Create your views here.

@public
def public_certificate_download(request, pk):
    certificate = PublicCertificate.objects.get(pk=pk)
    filename = path_leaf(certificate.file.name)
    response = HttpResponse(certificate.file,
                            content_type='application/vnd.ms-powerpoint|application/vnd.openxmlformats-officedocument.presentationml.presentation')
    response['Content-Disposition'] = 'inline; filename=%s' % filename
    return response

@public
def public_certificate_view_raw(request, pk):
    certificate = PublicCertificate.objects.get(pk=pk)
    response = FileResponse(open(certificate.file.name, 'rb'), content_type='application/pdf')

    return response

@public
def public_certificate_view(request, pk):
    certificate = PublicCertificate.objects.get(pk=pk)
    context = {'content_title': 'Authorised Certificate',
               'certificate': certificate}
    return render(request, 'unauthenticated/certificate_view.html', context=context)
