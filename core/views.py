# core/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


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
