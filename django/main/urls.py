from django.urls import path, include, re_path

from .views import *



urlpatterns = [    
    path('', index, name='index'),
    path('students/', students, name='students'),
    path('course/', courses, name='course'),
    path('grade/', grade, name='grade'),
    
       
]