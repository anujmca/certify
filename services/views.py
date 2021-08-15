from io import StringIO, BytesIO
from django.contrib.auth import authenticate, logout as django_logout, login as django_login
from django.db.models import Q
from django.shortcuts import render, redirect
from pandas import *

from certify.middleware import CustomAuthenticationBackend
from generators import pptxGenerator as generator
from services.models import *
from random import randint
from twilio.rest import Client as TwilioClient
from datetime import timezone
import datetime


def login(request):
    if request.method == "POST":
        email_or_phone = request.POST['email_or_phone']
        if 'sign-in' in request.POST:
            password = request.POST['password']

            # check if user has entered correct credentials
            # user = authenticate(request=request, email_or_phone=email_or_phone, password=password)
            authBackend = CustomAuthenticationBackend()
            user = authBackend.authenticate(request=request, email_or_phone=email_or_phone, password=password)

            if user is not None and user.is_authenticated:
                django_login(request, user)
                next_url = request.GET.get('next')
                return redirect(next_url if next_url else '/')
            else:
                return redirect('/login')

        elif 'request-otp' in request.POST:
            otp = randint(1000, 9999)

            # account_sid = 'AC11de2df9f81f5b40d469bd0c8b5ccfd7'
            # auth_token = '9d53e967ffb87caa796c733f90ecd1ab'
            # client = TwilioClient(account_sid, auth_token)
            # message = client.messages.create(
            #     body=f'{otp} is your OTP for certify, valid for next 15 minutes',
            #     from_='+12512418305',
            #     to=email_or_phone
            # )

            dt = datetime.datetime.now(timezone.utc)
            utc_time = dt.replace(tzinfo=timezone.utc)

            user = User.objects.get(Q(email=email_or_phone) | Q(profile__phone_number=email_or_phone))
            user.profile.otp = otp
            user.profile.otp_valid_till = utc_time + datetime.timedelta(minutes=1)
            user.profile.save()

            context = {'otp_sent': True}
            return redirect('/login', context)
        elif 'verify-otp' in request.POST:
            otp = request.POST['otp']
            authBackend = CustomAuthenticationBackend()
            user = authBackend.authenticate(request=request, email_or_phone=email_or_phone, otp=otp)

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

        latest_batch_id = 0 if not Certificate.objects.exists() else Certificate.objects.order_by('-batch_id')[
            0].batch_id
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
