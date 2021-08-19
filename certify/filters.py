from django import template
from services import utilities as utl

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
