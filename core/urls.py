"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from core import views
from core.views import admin_dashboard, admin_register_face, delete_face


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('students.urls')),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # path('admin-dashboard/', views.admin_only_view, name='admin_dashboard'),
    path('leader-dashboard/', views.leader_dashboard, name='leader_dashboard'),
    path('user-dashboard/', views.user_dashboard, name='user_dashboard'),
    path('redirect-by-role/', views.redirect_by_role, name='redirect_by_role'),
    path('', include('attendance.urls')),
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('admin-dashboard/register-face/<int:user_id>/', admin_register_face, name='admin_register_face'),
    path('admin-dashboard/delete-face/<int:user_id>/', delete_face, name='delete_face'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

