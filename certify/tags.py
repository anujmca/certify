# custom_tags.py
from django import template

from certify import settings
from tenant import utilities
register = template.Library()

@register.simple_tag(takes_context=True)
def tenant_name(context):
    request = context['request']
    tenant = utilities.get_tenant(request)
    return settings.OUR_DISPLAY_NAME if tenant is None else tenant.name
