"""
Completed Reports Views for Guidance Counselors
Shows all completed counseling sessions and reports ready for export
"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import datetime, timedelta
from .models import CounselingSchedule, CaseEvaluation, IncidentReport


@login_required
def completed_reports(request):
    """
    View for displaying all completed counseling reports
    Only accessible by counselors and guidance
    """
    # Check if user is a counselor or guidance
    if request.user.role not in ['counselor', 'guidance']:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('dashboard')
    
    # Get all completed counseling sessions
    completed_sessions = CounselingSchedule.objects.filter(
        counselor=request.user,
        status='completed'
    ).select_related(
        'student', 'evaluation', 'evaluation__report', 'evaluation__report__incident_type', 'counselor'
    ).order_by('-completed_date')
    
    # Get evaluated cases (completed evaluations)
    evaluated_cases = CaseEvaluation.objects.filter(
        counselor=request.user,
        status='evaluated'
    ).select_related(
        'report', 'report__incident_type', 'report__reported_student', 'counselor'
    ).order_by('-evaluated_date')
    
    # Combine both into a unified list for display
    reports = []
    
    # Add completed sessions
    for session in completed_sessions:
        if session.evaluation and session.evaluation.report:
            reports.append({
                'type': 'session',
                'report': session.evaluation.report,
                'student': session.student,
                'scheduled_date': session.scheduled_date,
                'completed_date': session.completed_date or session.updated_at,
                'counselor': session.counselor,
                'notes': session.notes,
                'location': session.location,
            })
    
    # Calculate statistics
    total_completed = len(reports)
    total_sessions = completed_sessions.count()
    total_evaluated = evaluated_cases.count()
    
    # This month count
    now = timezone.now()
    first_day_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    this_month_count = len([r for r in reports if r['completed_date'] >= first_day_of_month])
    
    context = {
        'reports': reports,
        'total_completed': total_completed,
        'total_sessions': total_sessions,
        'total_evaluated': total_evaluated,
        'this_month_count': this_month_count,
    }
    
    return render(request, 'counselor/completed_reports.html', context)
