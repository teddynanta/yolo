from django.urls import path
from . import views

urlpatterns = [
    path('clock/', views.attendance_page, name='clock_page'),
    path('submit/', views.submit_attendance, name='submit_attendance'),
    path('submit-image/', views.submit_attendance_image, name='submit_attendance_image'),
    path('register-face/', views.register_face, name='register_face'),
    path('my-attendance/', views.my_attendance, name='my_attendance'),
    path('all-attendance/', views.all_attendance, name='all_attendance'),
    path("detect-face-yolo/", views.detect_faces_yolo, name="detect_face_yolo"),



]
