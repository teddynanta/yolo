import base64
import cv2
import numpy as np
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
from .models import Attendance
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from users.models import UserProfile
import face_recognition
import pickle
from PIL import Image


@login_required
def register_face(request):
    if request.method == 'POST':
        image_data = request.POST.get('image_data')

        if not image_data:
            return HttpResponse("No image data", status=400)

        # Decode base64 image
        try:
            format, imgstr = image_data.split(';base64,') 
            img_data = base64.b64decode(imgstr)
            np_arr = np.frombuffer(img_data, np.uint8)
            frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
            cv2.imwrite("debug1.jpg", frame)

        except Exception as e:
            return HttpResponse(f"Failed to decode image: {str(e)}", status=400)

        if frame is None or len(frame.shape) != 3 or frame.shape[2] != 3:
            return HttpResponse("Invalid image format", status=400)

        # Resize (optional, normalize quality)
        frame = cv2.resize(frame, (400, 400))

        # Convert to RGB using PIL
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        rgb_pil = Image.fromarray(rgb_frame.astype(np.uint8), 'RGB')
        rgb_pil = rgb_pil.convert('RGB')
        rgb_array = np.array(rgb_pil)

        # Face detection
        try:
            print("Final dtype:", rgb_array.dtype)
            print("Final shape:", rgb_array.shape)
            print("Final type:", type(rgb_array))
            face_locations = face_recognition.face_locations(rgb_array)
            if not face_locations:
                return HttpResponse("No face detected", status=400)

            face_encoding = face_recognition.face_encodings(rgb_array, face_locations)[0]
        except Exception as e:
            return HttpResponse(f"Face recognition failed: {str(e)}", status=500)

        # Save to user profile
        try:
            profile = request.user.userprofile
            profile.face_encoding = pickle.dumps(face_encoding)
            profile.save()
        except Exception as e:
            return HttpResponse(f"Failed to save encoding: {str(e)}", status=500)

        return HttpResponse("Face data saved successfully!")

    return render(request, 'attendance/register_face.html')

def attendance_page(request):
    return render(request, 'attendance/clock.html')

def submit_attendance(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        attend_type = request.POST.get('type')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return HttpResponse("User not found", status=404)

        Attendance.objects.create(
            user=user,
            type=attend_type,
            timestamp=timezone.now()
        )

        return HttpResponse(f"{user.username} clocked {attend_type} successfully!")

    return HttpResponse("Invalid request", status=400)

@csrf_exempt
def submit_attendance_image(request):
    if request.method == 'POST':
        data_url = request.POST.get('image_data')

        if not data_url:
            return HttpResponse("No image data", status=400)

        # Decode base64 image
        format, imgstr = data_url.split(';base64,') 
        img_data = base64.b64decode(imgstr)
        np_img = np.frombuffer(img_data, np.uint8)
        frame = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

        # Save image for debug
        cv2.imwrite("debug.jpg", frame)

        # Later: run face recognition here...

        return HttpResponse("Image received and saved!")
    return HttpResponse("Only POST allowed", status=405)
