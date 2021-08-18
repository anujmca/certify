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
from services.views_restful import get_user_by_email_or_phone

from services.utilities import BaseToken


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
            otp = 1234
            if settings.IS_HARDCODED_OTP == False:
                otp = randint(1000, 9999)

                account_sid = 'AC11de2df9f81f5b40d469bd0c8b5ccfd7'
                auth_token = '5f9b586fc93ef34310ae7bef1c11e793'
                client = TwilioClient(account_sid, auth_token)
                message = client.messages.create(
                    body=f'{otp} is your OTP for certify, valid for next 15 minutes',
                    from_='+12512418305',
                    to=email_or_phone
                )

            dt = datetime.datetime.now(timezone.utc)
            utc_time = dt.replace(tzinfo=timezone.utc)

            user = get_user_by_email_or_phone(email_or_phone, email_or_phone)
            if user:
                user.profile.otp = otp
                user.profile.otp_valid_till = utc_time + datetime.timedelta(minutes=1)
                user.profile.save()

                context = {'otp_sent': True,
                           'email_or_phone': email_or_phone}

                request.session['redirect-context'] = context
            return redirect('/login')
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
