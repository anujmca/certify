from django import template

register = template.Library()


@register.filter
def csv(list_obj):
    result = ''
    if list_obj:
        result = ', '.join(list_obj)
    return result
