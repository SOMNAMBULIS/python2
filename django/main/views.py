from django.shortcuts import render
from django.http import HttpResponse
from .models import Student, Course, Grade

# Create your views here.

def index(r):
    return render(r, 'base.html')


def students(r):
    students = Student.objects.all()
    return render(r, 'students.html', 
                    context={'students':students})

def courses(r):
    courses = Course.objects.all()
    return render(r, 'courses.html', 
                    context={'course':courses})

def grade(r):
    grade = Grade.objects.all()
    return render(r, 'grade.html', 
                    context={'grade':grade})