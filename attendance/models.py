from django.db import models
from django.contrib.auth.models import User

class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=10)  # in / out
    timestamp = models.DateTimeField()

    def __str__(self):
            return f"{self.user.username} - {self.type.upper()} at {self.timestamp.strftime('%Y-%m-%d %H:%M')}"