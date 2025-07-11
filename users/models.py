from django.db import models
from django.contrib.auth.models import User
from roles.models import Role
import pickle

class UserProfile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
  has_face_data = models.BooleanField(default=False)
  face_folder = models.CharField(max_length=255, blank=True, null=True)
  face_encoding = models.BinaryField(null=True, blank=True)  # 🧠 Add this line

  def __str__(self):
    return self.user.username