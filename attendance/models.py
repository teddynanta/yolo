from django.db import models

# Create your models here.
class Attendance(models.Model):
  STATUS_CHOICES = [
    ('present', 'Present'),
    ('absent', 'Absent'),
    ('late', 'Late'),
  ]
  TYPE_CHOICES = [
    ('clock_in', 'Clock In'),
    ('clock_out', 'Clock Out'),
  ]

  user = models.ForeignKey('students.Student', on_delete=models.CASCADE)
  date = models.DateField(auto_now_add=True)
  check_in = models.TimeField(null=True, blank=True)
  check_out = models.TimeField(null=True, blank=True)
  status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='absent')
  type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='clock_in')

  def __str__(self):
    return f"{self.user.name} - {self.date} - {self.type} - {self.status}"
