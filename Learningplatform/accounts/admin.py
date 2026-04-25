from django.contrib import admin
from .models import Course, Enrollment, Profile

# Register your models here.
admin.site.register(Course)
admin.site.register(Enrollment)
admin.site.register(Profile)



