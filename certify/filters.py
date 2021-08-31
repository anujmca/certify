from django import template

from certify import settings
from services import utilities as utl
from django_tenants.utils import schema_context, connection

register = template.Library()


@register.filter
def csv(list_obj):
    result = ''
    if list_obj:
        result = ', '.join(list_obj)
    return result


@register.filter
def has_group(user, group_name):
    return group_name in utl.get_user_group_names(user)


@register.filter
def events(user):
    _events = [certificate.event for certificate in user.certificates.all()]
    return set(_events)


@register.filter
def tenant_specific_events(awardee):
    tenant_schema_name = connection.schema_name
    with schema_context(settings.PUBLIC_SCHEMA_NAME):
        return awardee.get_tenant_specific_events(tenant_schema_name=tenant_schema_name)


@register.filter
def tenant_specific_certificates(awardee):
    tenant_schema_name = connection.schema_name
    with schema_context(settings.PUBLIC_SCHEMA_NAME):
        return awardee.get_tenant_specific_certificates(tenant_schema_name=tenant_schema_name)
