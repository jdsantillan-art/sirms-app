"""
Completed Sessions Views for Guidance Counselors
Shows all completed counseling sessions
"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CounselingSchedule, CustomUser


@login_required
def completed_sessions(request):
    """
    View for displaying all completed counseling sessions
    Only accessible by counselors
    """
    # Check if user is a counselor
    if request.user.role != 'counselor':
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('dashboard')
    
    # Get all completed sessions for this counselor
    sessions = CounselingSchedule.objects.filter(
        counselor=request.user,
        status='completed'
    ).select_related('student', 'evaluation', 'evaluation__report').order_by('-scheduled_date')
    
    context = {
        'sessions': sessions,
        'total_completed': sessions.count(),
    }
    
    return render(request, 'counselor/completed_sessions.html', context)
