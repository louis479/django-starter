from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('courses/', views.course_list, name='courses'),
    path('enroll/<int:course_id>/', views.enroll_course, name='enroll'),
    path('create-course/', views.create_course, name='create_course'),
]