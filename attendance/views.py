import base64
import cv2
import numpy as np
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
from .models import Attendance
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from users.models import UserProfile
import face_recognition
import pickle
from PIL import Image
from django.core.files.base import ContentFile
import base64, uuid


@login_required
def my_attendance(request):
    records = Attendance.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'attendance/my_attendance.html', {'records': records})


@user_passes_test(lambda u: u.userprofile.role.name == 'Leader' or u.is_superuser)
def all_attendance(request):
    records = Attendance.objects.select_related('user').order_by('-timestamp')
    return render(request, 'attendance/all_attendance.html', {'records': records})

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
            img_file = ContentFile(img_data, name=f'{request.user.username}_face.jpg')
            profile.face_encoding = pickle.dumps(face_encoding)
            profile.face_image = img_file
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
        attend_type = request.POST.get('type')  # 🧠 Must be 'in' or 'out'

        if not data_url or not attend_type:
            return HttpResponse("Missing image or type", status=400)

        format, imgstr = data_url.split(';base64,')
        img_data = base64.b64decode(imgstr)
        np_img = np.frombuffer(img_data, np.uint8)
        frame = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(rgb_frame)
        if not face_locations:
            return HttpResponse("No face detected", status=400)

        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        unknown_encoding = face_encodings[0]

        # Loop through known users
        from users.models import UserProfile
        known_users = UserProfile.objects.exclude(face_encoding__isnull=True)

        for profile in known_users:
            known_encoding = pickle.loads(profile.face_encoding)
            results = face_recognition.compare_faces([known_encoding], unknown_encoding, tolerance=0.5)

            if results[0]:  # Match found
                img_filename = f"{profile.user.username}_{uuid.uuid4().hex}.jpg"
                img_file = ContentFile(img_data, name=img_filename)
                attendance = Attendance(
                    user=profile.user,
                    type=attend_type,  # Or determine this from form input
                    timestamp=timezone.now()
                )
                attendance.captured_image.save(img_filename, img_file)
                attendance.save()
                # Save image
                return HttpResponse(f"{profile.user.username} clocked {attend_type} successfully!")

        return HttpResponse("Face not recognized", status=404)

    return HttpResponse("Only POST allowed", status=405)