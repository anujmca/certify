import mimetypes
from io import StringIO, BytesIO
# from wsgiref.util import FileWrapper

from django.contrib.auth import authenticate, logout as django_logout, login as django_login

from django.shortcuts import render, redirect
from django.utils.encoding import smart_str
from pandas import *
# import generators.pptx_generator
from generators import pptxGenerator as generator
from certify import settings
from django.http import HttpResponse

from django.contrib.auth.models import User

from typing import Optional
import os

from services.models import *


def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        # check if user has entered correct credentials
        user = authenticate(username=email, password=password)
        if user is not None and user.is_authenticated:
            django_login(request, user)
            next_url = request.GET.get('next')
            return redirect(next_url if next_url else '/')
        else:
            return redirect('/login')


def logout(request):
    if request.user is not None and request.user.is_authenticated:
        django_logout(request)
    return redirect('/')


def generate_certificate(request):
    templateId = request.POST.get('templateId')
    dataSheetId = request.POST.get('dataSheetId')
    template = Template.objects.get(pk=templateId)
    dataSheet = DataSheet.objects.get(pk=dataSheetId)
    if template is not None and dataSheet is not None:
        # templateFile =  template.file.read()
        data_sheet_excel = ExcelFile(dataSheet.data_sheet)
        df = data_sheet_excel.parse(data_sheet_excel.sheet_names[0])

        latest_batch_id = 0 if not Certificate.objects.exists() else Certificate.objects.order_by('-batch_id')[0].batch_id
        batch_id = 1 if latest_batch_id is None else latest_batch_id + 1
        for i, row in df.iterrows():
            data_sheet_dictionary = {}
            data_keys = []
            for key in df.columns:
                data_sheet_dictionary[key] = row[key]
                obj = DataKey(name=key, value=data_sheet_dictionary[key])
                obj.save()
                data_keys.append(obj)

            certificate_file = generator.generate(template_file_path=template.file,
                                                  data_sheet_dictionary=data_sheet_dictionary)
            # certificate_file.save(settings.MEDIA_ROOT + '')

            target_stream = BytesIO()
            certificate_file.save(target_stream)


            certificate = Certificate(batch_id=batch_id, template=template)
            certificate.save()
            certificate.data_keys.set(data_keys)
            certificate.file.save(data_sheet_dictionary['employee_name'] + '_' + str(batch_id) + '.pptx', target_stream)
            certificate.save()

        return redirect('/certificates')
