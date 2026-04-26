from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Course, Enrollment
from .decorators import allowed_roles

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
            login(request, user)
            return redirect('dashboard') 
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'accounts/login.html')


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
        else:
            User.objects.create_user(username=username, password=password)
            messages.success(request, 'Account created successfully')
            return redirect('login')

    return render(request, 'accounts/register.html')


@login_required(login_url='login')
def dashboard_view(request):
    enrollments = Enrollment.objects.filter(user=request.user)
    return render(request, 'accounts/dashboard.html', {'enrollments': enrollments})

@login_required(login_url='login')
def course_list(request):
    courses = Course.objects.all()
    return render(request, 'accounts/course_list.html', {'courses': courses})

@login_required(login_url='login')
def enroll_course(request, course_id):
    course = Course.objects.get(id=course_id)

    if not Enrollment.objects.filter(user=request.user, course=course).exists():
        Enrollment.objects.create(user=request.user, course=course)
    return redirect('dashboard')

@login_required(login_url='login')
@allowed_roles(['instructor'])
def create_course(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')

        Course.objects.create(
            title=title,
            description=description,
            created_by=request.user
        )
        return redirect('courses')

    return render(request, 'accounts/create_course.html')

@login_required(login_url='login')
@allowed_roles(['student'])
def enroll_course(request, course_id):

def logout_view(request):
    logout(request)
    return redirect('login')  