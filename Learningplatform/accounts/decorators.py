from django.shortcuts import redirect

def allowed_roles(allowed=[]):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if request.user.profile.role in allowed:
                return view_func(request, *args, **kwargs)
            return redirect('dashboard')
        return wrapper
    return decorator