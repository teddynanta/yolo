from django.db import models
from django.contrib.auth.models import User

class Attendance(models.Model):
    TYPE_CHOICES = (
        ('in', 'Clock In'),
        ('out', 'Clock Out'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    # ✅ New field to store photo
    captured_image = models.ImageField(upload_to='attendance_photos/', null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.type} at {self.timestamp}"
