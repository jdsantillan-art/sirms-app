"""
Incident Type Views for Guidance Counselors
Shows incidents filtered by type (PA or OSP)
"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import IncidentReport, IncidentType


@login_required
def prohibited_acts(request):
    """
    View for displaying all Prohibited Acts incidents
    Only accessible by counselors, DO, and principal
    """
    # Check permissions
    if request.user.role not in ['counselor', 'do', 'principal']:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('dashboard')
    
    # Get all reports with Prohibited Acts incident types
    reports = IncidentReport.objects.filter(
        incident_type__severity='prohibited'
    ).select_related(
        'incident_type', 'reported_student', 'reporter', 'classification'
    ).order_by('-created_at')
    
    # Get statistics
    total_count = reports.count()
    pending_count = reports.filter(status='pending').count()
    classified_count = reports.filter(status='classified').count()
    resolved_count = reports.filter(status__in=['resolved', 'closed']).count()
    
    context = {
        'reports': reports,
        'total_count': total_count,
        'pending_count': pending_count,
        'classified_count': classified_count,
        'resolved_count': resolved_count,
        'page_title': 'Prohibited Acts',
        'page_type': 'PA',
    }
    
    return render(request, 'counselor/incident_type_list.html', context)


@login_required
def other_school_policies(request):
    """
    View for displaying all Other School Policies incidents
    Only accessible by counselors, DO, and principal
    """
    # Check permissions
    if request.user.role not in ['counselor', 'do', 'principal']:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('dashboard')
    
    # Get all reports with Other School Policies incident types
    reports = IncidentReport.objects.filter(
        incident_type__severity='school_policy'
    ).select_related(
        'incident_type', 'reported_student', 'reporter', 'classification'
    ).order_by('-created_at')
    
    # Get statistics
    total_count = reports.count()
    pending_count = reports.filter(status='pending').count()
    classified_count = reports.filter(status='classified').count()
    resolved_count = reports.filter(status__in=['resolved', 'closed']).count()
    
    context = {
        'reports': reports,
        'total_count': total_count,
        'pending_count': pending_count,
        'classified_count': classified_count,
        'resolved_count': resolved_count,
        'page_title': 'Other School Policies',
        'page_type': 'OSP',
    }
    
    return render(request, 'counselor/incident_type_list.html', context)
