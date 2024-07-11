from django.shortcuts import redirect
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth.models import User
from functools import wraps


def authenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            http_referrer = request.META.get('HTTP_REFERER')
            # if http_referrer:
            #     return HttpResponseRedirect(http_referrer)

            # else:
            #     return redirect('homepage')

            return redirect('personal-homepage', username=request.user.username)
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            elif group == 'admin':
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponseForbidden("You don't have permission to access this page.")
        return wrapper_func
    return decorator
