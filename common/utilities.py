import ntpath

from django.contrib.auth import get_user_model
User = get_user_model()
from django.db.models import Q
from django_tenants.utils import connection

from certify import settings


def get_user_by_email_or_phone(email, phone):
    try:
        tenant_schema_name = connection.schema_name
        if tenant_schema_name == settings.PUBLIC_SCHEMA_NAME:
            return User.objects.get(Q(email=email) | Q(phone_number=phone))
        else:
            return User.objects.get(Q(email=email) | Q(phone_number=phone))
    except User.DoesNotExist:
        return None


def get_tenant_user_by_public_user(tenant_users, public_user):
    tenant_user = None
    try:
        if tenant_users.filter(email=public_user.email).exists():
            tenant_user = tenant_users.get(email=public_user.email)
        elif tenant_users.filter(phone_number=public_user.phone_number).exists():
            tenant_user = tenant_users.get(phone_number=public_user.phone_number)
    except:
        tenant_user = None
    return tenant_user


def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)