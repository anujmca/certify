# custom_tags.py
from django import template
from tenant import utilities
register = template.Library()

@register.simple_tag(takes_context=True)
def tenant_name(context):
    request = context['request']
    return utilities.get_tenant(request).name
