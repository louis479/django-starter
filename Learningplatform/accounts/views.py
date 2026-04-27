from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Course, Enrollment, Profile
from .decorators import allowed_roles


def ensure_user_profile(user):
    if user.is_authenticated:
        Profile.objects.get_or_create(user=user, defaults={'role': 'student'})

def home_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        return redirect('login')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            ensure_user_profile(user)
            login(request, user)
            return redirect('dashboard') 
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'accounts/login.html')


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')
        role = request.POST.get('role', 'student')

        if not username or not password:
            messages.error(request, 'Username and password are required.')
        elif password != confirm_password:
            messages.error(request, 'Passwords do not match.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
        else:
            user = User.objects.create_user(username=username, password=password)
            user.profile.role = role if role in {'student', 'instructor'} else 'student'
            user.profile.save()
            messages.success(request, 'Account created successfully. Please sign in.')
            return redirect('login')

    return render(request, 'accounts/register.html')


@login_required(login_url='login')
def dashboard_view(request):
    ensure_user_profile(request.user)
    enrollments = Enrollment.objects.filter(user=request.user)
    created_courses = Course.objects.filter(created_by=request.user)
    context = {
        'enrollments': enrollments,
        'created_courses': created_courses,
        'total_courses': Course.objects.count(),
    }
    return render(request, 'accounts/dashboard.html', context)

@login_required(login_url='login')
def course_list(request):
    ensure_user_profile(request.user)
    courses = Course.objects.all()
    return render(request, 'accounts/course_list.html', {'courses': courses})

@login_required(login_url='login')
@allowed_roles(['instructor'])
def create_course(request):
    ensure_user_profile(request.user)
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')

        Course.objects.create(
            title=title,
            description=description,
            created_by=request.user
        )
        messages.success(request, 'Course created successfully.')
        return redirect('courses')

    return render(request, 'accounts/create_course.html')

@login_required(login_url='login')
@allowed_roles(['student'])
def enroll_course(request, course_id):
    ensure_user_profile(request.user)
    course = get_object_or_404(Course, id=course_id)
    Enrollment.objects.get_or_create(user=request.user, course=course)
    return redirect('dashboard')

def logout_view(request):
    logout(request)
    return redirect('login')  
