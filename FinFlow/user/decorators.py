from django.shortcuts import redirect
from django.http import HttpResponse


def logout_message_required(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        return function(request, *args, **kwargs)
    return wrap


def login_message_required(function):

    def wrap(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/')
        return function(request, *args, **kwargs)

    return wrap