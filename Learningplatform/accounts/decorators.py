from django.shortcuts import redirect
from .models import Profile

def allowed_roles(allowed=[]):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            profile, _ = Profile.objects.get_or_create(
                user=request.user,
                defaults={'role': 'student'},
            )
            if profile.role in allowed:
                return view_func(request, *args, **kwargs)
            return redirect('dashboard')
        return wrapper
    return decorator
