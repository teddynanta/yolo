from django.urls import path
from . import views

urlpatterns = [
    path('clock/', views.attendance_page, name='clock_page'),
    path('submit/', views.submit_attendance, name='submit_attendance'),
    path('submit-image/', views.submit_attendance_image, name='submit_attendance_image'),
    path('register-face/', views.register_face, name='register_face'),



]
