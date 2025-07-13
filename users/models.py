from django.db import models
from django.contrib.auth.models import User
from roles.models import Role
import pickle

# users/models.py
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
    face_encoding = models.BinaryField(null=True, blank=True)
    face_image = models.ImageField(upload_to='face_images/', null=True, blank=True)  # ✅ New field


    def __str__(self):
      return self.user.username