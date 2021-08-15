from django.conf import settings


def settings_export(request):
    """
    Django template context preprocessor to allow access of settings variables in yhe templates.
    """

    return {
        "settings": settings
    }