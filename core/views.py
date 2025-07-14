import base64
import pickle
import cv2
import numpy as np
from PIL import Image
import face_recognition
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from users.models import UserProfile
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse


@user_passes_test(lambda u: u.is_superuser)
def delete_face(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    profile = user.userprofile
    profile.face_encoding = None
    if profile.face_image:
        profile.face_image.delete(save=False)
    profile.save()

    return HttpResponseRedirect(reverse('admin_dashboard'))

@user_passes_test(lambda u: u.is_superuser)  # or use a role check
def admin_dashboard(request):
    users = User.objects.all()
    return render(request, 'admin/admin_dashboard.html', {'users': users})

@user_passes_test(lambda u: u.is_superuser)
def admin_register_face(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    profile = user.userprofile

    if request.method == 'POST':
        image_data = request.POST.get('image_data')
        if not image_data:
            return HttpResponse("No image data", status=400)

        format, imgstr = image_data.split(';base64,')
        img_data = base64.b64decode(imgstr)
        np_img = np.frombuffer(img_data, np.uint8)
        frame = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(rgb_frame)
        if not face_locations:
            return HttpResponse("No face detected", status=400)

        encoding = face_recognition.face_encodings(rgb_frame, face_locations)[0]

        # Save image + encoding
        profile.face_encoding = pickle.dumps(encoding)
        img_file = ContentFile(img_data, name=f'{user.username}_face.jpg')
        profile.face_image = img_file
        profile.save()

        return HttpResponse("Face registered successfully!")

    return render(request, 'admin/admin_register_face.html', {'user': user})

@login_required
def admin_only_view(request):
    if request.user.userprofile.role.name != 'Admin':
        return redirect('not_authorized')
    return render(request, 'admin/admin_dashboard.html')

@login_required
def leader_dashboard(request):
    profile = request.user.userprofile
    if not profile.role or profile.role.name != 'Leader':
        return redirect('not_authorized')
    return render(request, 'leader/leader_dashboard.html')

@login_required
def user_dashboard(request):
    profile = request.user.userprofile
    if not profile.role or profile.role.name != 'User':
        return redirect('not_authorized')
    return render(request, 'user/user_dashboard.html')

@login_required
def redirect_by_role(request):
    role = request.user.userprofile.role.name
    if role == 'Admin':
        return redirect('admin_dashboard')
    elif role == 'Leader':
        return redirect('leader_dashboard')
    else:
        return redirect('user_dashboard')
