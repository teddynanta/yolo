from django.contrib import admin
from .models import Attendance
# Register your models here.
from django.utils.html import format_html

class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'type', 'timestamp', 'captured_image_tag')
    readonly_fields = ('captured_image_tag',)

    def captured_image_tag(self, obj):
        if obj.captured_image:
            return format_html('<img src="{}" width="100" />', obj.captured_image.url)
        return "-"
    captured_image_tag.short_description = 'Captured Photo'

admin.site.register(Attendance, AttendanceAdmin)

