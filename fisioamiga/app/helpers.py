import functools
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect
from .models import *

def datos_admin(view_func):
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        
        if User.objects.filter(user=request.user).count() == 1:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse('/stepform/')
        return redirect('/stepform/')
    return wrapper
