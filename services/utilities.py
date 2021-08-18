from pandas import *
from pptx import Presentation
import re

from enum import Enum


# from django.db.models import Q
# # from pandas import *
# from services.models import *
# from services.models import Profile


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


def is_valid_email(email):
    regex_email = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    try:
        if re.search(regex_email, email):
            return True
        else:
            return False
    except:
        return False
