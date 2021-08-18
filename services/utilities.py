from pandas import *
from pptx import Presentation
from enum import Enum

from django.db.models import Q
# from pandas import *
from services.models import *


class BaseToken():
    id = 'id'
    first_name = 'first_name'
    last_name = 'last_name'
    phone_number = 'phone_number'
    email_id = 'email_id'


DEFAULT_TOKENS = [BaseToken.id, BaseToken.first_name, BaseToken.last_name, BaseToken.phone_number, BaseToken.email_id]


def get_excel_headers(data_sheet):
    data_sheet_excel = ExcelFile(data_sheet)
    df = data_sheet_excel.parse(data_sheet_excel.sheet_names[0])
    df = df.reindex(sorted(df.columns), axis=1)
    return df.columns


def get_ppt_tokens(template_file):
    tokens = list()
    ppt = Presentation(template_file)
    slide = ppt.slides[0]
    for shape in ppt.slides[0].shapes:
        if hasattr(shape, 'text'):
            tokens.append(shape.text)

    return tokens.sort()


def get_user_by_awardee(df_awardee):
    phone = df_awardee[BaseToken.phone_number]
    email = df_awardee[BaseToken.email_id]

    user = get_user_by_email_or_phone(email, phone)
    password = None

    if user is None:
        user_name = email if email else phone if phone else None
        if user_name:
            password = User.objects.make_random_password() if settings.IS_HARDCODED_PASSWORD_GENERATED == False else 'Gurgaon1'
            user = User.objects.create_user(username=user_name, email=email, password=password)
            user.first_name = df_awardee[BaseToken.first_name]
            user.last_name = df_awardee[BaseToken.last_name]
            user.save()
            profile = Profile.objects.create(user=user)
            profile.phone_number = phone
            profile.client_user_id = df_awardee[BaseToken.id]
            profile.save()
            user.save()

    return user, password


def get_user_by_email_or_phone(email, phone):
    try:
        return User.objects.get(Q(email=email) | Q(profile__phone_number=phone))
    except User.DoesNotExist:
        return None
