from django.contrib import admin

# Register your models here.

from .models import Student, Course, Grade

admin.site.register(Course)
admin.site.register(Grade)
admin.site.register(Student)