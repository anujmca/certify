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
