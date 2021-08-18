from django.utils import timezone
from django.utils import translation

from io import StringIO, BytesIO
from django.contrib.auth import authenticate, logout as django_logout, login as django_login
from django.db.models import Q
from django.shortcuts import render, redirect
from django.utils.deprecation import MiddlewareMixin
from pandas import *
from generators import pptxGenerator as generator
from services.models import *
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User

from services.views_restful import get_user_by_email_or_phone


class CustomAuthenticationBackend(MiddlewareMixin):
    def authenticate(self, request, email_or_phone=None, password=None, otp=None):
        try:
            user = get_user_by_email_or_phone(email=email_or_phone, phone=email_or_phone)
            if password:
                pwd_valid = user.check_password(password)
                if pwd_valid:
                    return user
                return None
            elif otp:
                return user if user.profile.otp == otp else None
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


# class InternationalizationMiddleware(MiddlewareMixin):
#     """
#     Middleware to set timezone and language preference of the logged in user.
#     """
#
#     def process_request(self, request):
#         user = request.user
#         if user.is_authenticated:
#             try:
#                 # Set preferences
#                 timezone.activate(user.profile.timezone)
#                 translation.activate(user.profile.language)
#
#             except PortalUser.DoesNotExist:
#                 pass
#
#         request.current_timezone = timezone.get_current_timezone()
#         request.current_language = translation.get_language()