from pandas import *
from pptx import Presentation
import re

from enum import Enum


# from django.db.models import Q
# # from pandas import *
# from services.models import *
# from services.models import Profile


class BaseToken:
    id = 'id'
    first_name = 'first_name'
    last_name = 'last_name'
    phone_number = 'phone_number'
    email_id = 'email_id'


DEFAULT_TOKENS = [BaseToken.id, BaseToken.first_name, BaseToken.last_name, BaseToken.phone_number, BaseToken.email_id]


class Groups:
    issuer = 'issuer'
    awardee = 'awardee'


def get_user_group_names(user):
    return [group.name for group in user.groups.all()] if user is not None and user.groups is not None else []


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

    tokens.sort()
    return tokens


def is_valid_email(email):
    regex_email = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    try:
        if re.search(regex_email, email):
            return True
        else:
            return False
    except:
        return False


# import sys
# import argparse
# import os
# import fnmatch
# import win32com
#
# # import tkinter as Tkinter

from win32com.client import Dispatch
import pythoncom
from django.db import models
from django.core.files import File

def get_jpg_file(file):
    ppt_dispatch = None
    output_file_path = None
    try:
        pythoncom.CoInitialize()
        ppt_dispatch = Dispatch('Powerpoint.Application')
        ppt_dispatch.Presentations.Open(file.path, WithWindow=0)
        firstSlideRange = ppt_dispatch.Presentations[0].Slides.Range([1])
        output_file_path = f'c:\\temp\\abc.jpg'
        firstSlideRange.Export(output_file_path, 'JPG')
    except:
        output_file_path = None
    finally:
        if ppt_dispatch:
            ppt_dispatch.Quit()
    return output_file_path
