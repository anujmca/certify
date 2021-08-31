from django.http import HttpResponse
from django.shortcuts import redirect
from services import utilities as utl

# adding this "public" decorator for future use, in case some handling is required for public url
def public(view_func):
    def wrapper_func(request, *args, **kwargs):
        return view_func(request, *args, **kwargs)

    return wrapper_func


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            if request.user.groups.exists():
                groups = request.user.groups.all()
                # if any(group in groups for group in allowed_roles):
                if any(group in utl.get_user_group_names(request.user) for group in allowed_roles):
                    return view_func(request, *args, **kwargs)
            return HttpResponse('You are not authorised for this request')
        return wrapper_func
    return decorator




























