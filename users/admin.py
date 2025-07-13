from django.contrib import admin
from .models import UserProfile
from django.utils.html import format_html

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'has_face_encoding', 'face_image_tag')
    readonly_fields = ('has_face_encoding', 'face_image_tag')

    def has_face_encoding(self, obj):
        return obj.face_encoding is not None
    has_face_encoding.boolean = True
    has_face_encoding.short_description = 'Has face data'

    def face_image_tag(self, obj):
        if obj.face_image:
            return format_html('<img src="{}" width="100" />', obj.face_image.url)
        return "-"
    face_image_tag.short_description = 'Registered Face'

admin.site.register(UserProfile, UserProfileAdmin)
