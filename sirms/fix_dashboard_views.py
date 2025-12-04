"""
Fixed dashboard function to replace the problematic one in views.py
"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Q, Count
from datetime import datetime, timedelta
import json
from .models import (
    CustomUser, IncidentReport, Classification, CounselingSession,
    Notification, IncidentType, ViolationHistory, CaseEvaluation,
    LegalReference
)


@login_required
def dashboard_fixed(request):
    user = request.user
    context = {'user_role': user.role}
    
    # Get current date and determine school year (June to May)
    current_date = timezone.now()
    current_month = current_date.month
    
    # School year starts in June
    if current_month >= 6:  # June onwards - current school year
        school_year_start = current_date.replace(month=6, day=1)
    else:  # Before June - previous school year
        school_year_start = current_date.replace(year=current_date.year - 1, month=6, day=1)
    
    # Generate trend data for school year months (June to May)
    school_months = ['June', 'July', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar', 'Apr', 'May']
    trend_data = []
    
    for i, month_name in enumerate(school_months):
        # Calculate the actual month number
        month_num = (6 + i) if (6 + i) <= 12 else (6 + i - 12)
        year_offset = 0 if (6 + i) <= 12 else 1
        
        month_start = school_year_start.replace(month=month_num, day=1)
        if year_offset == 1:
            month_start = month_start.replace(year=month_start.year + 1)
        
        # Get last day of month
        if month_num == 12:
            month_end = month_start.replace(day=31)
        else:
            next_month = month_start.replace(month=month_num + 1) if month_num < 12 else month_start.replace(year=month_start.year + 1, month=1)
            month_end = next_month - timedelta(days=1)
        
        month_reports = IncidentReport.objects.filter(
            created_at__range=[month_start, month_end]
        ).count()
        
        trend_data.append({
            'month': month_name,
            'reports': month_reports
        })
    
    # Grade data - for Reports by Grade Level
    grade_data = []
    for grade in range(7, 13):
        count = IncidentReport.objects.filter(grade_level=str(grade)).count()
        grade_data.append({
            'grade': f'Grade {grade}',
            'count': count
        })
    
    # Violation type data - Prohibited Acts vs Other School Policies (for PIE CHART)
    prohibited_count = IncidentReport.objects.filter(
        incident_type__severity='prohibited'
    ).count()
    
    school_policy_count = IncidentReport.objects.filter(
        incident_type__severity='school_policy'
    ).count()
    
    violation_type_data = [
        {'name': 'Prohibited Acts', 'value': prohibited_count},
        {'name': 'Other School Policies', 'value': school_policy_count}
    ]
    
    # Add analytics data to context
    context.update({
        'trend_data': json.dumps(trend_data),
        'grade_data': json.dumps(grade_data),
        'violation_type_data': json.dumps(violation_type_data),
        'resolution_data': json.dumps([]),  # Default empty for all roles
    })
    
    if user.role == 'student':
        reports = IncidentReport.objects.filter(reported_student=user)
        context.update({
            'pending_reports': reports.filter(status='pending').count(),
            'under_review': reports.filter(status='under_review').count(),
            'resolved': reports.filter(status__in=['resolved', 'closed']).count(),
            'recent_reports': reports.order_by('-created_at')[:5],
            'counseling_sessions': CounselingSession.objects.filter(student=user, status='scheduled'),
        })
    elif user.role == 'teacher':
        reports = IncidentReport.objects.filter(reporter=user)
        context.update({
            'total_reports': reports.count(),
            'pending': reports.filter(status='pending').count(),
            'recent_reports': reports.order_by('-created_at')[:5],
        })
    elif user.role == 'do':
        reports = IncidentReport.objects.all()
        
        # Count reports with classifications
        minor_cases = reports.filter(classification__severity='minor').count()
        major_cases = reports.filter(classification__severity='major').count()
        
        # If no classifications exist, count by status instead
        if minor_cases == 0 and major_cases == 0:
            # Count reports that would typically be minor (handled by DO)
            minor_cases = reports.filter(
                status__in=['pending', 'under_review', 'resolved']
            ).exclude(
                status='referred_to_counselor'
            ).count()
            
            # Count reports referred to counselor (major cases)
            major_cases = reports.filter(
                status='referred_to_counselor'
            ).count()
        
        context.update({
            'total_reports': reports.count(),
            'pending': reports.filter(status='pending').count(),
            'classified': reports.filter(status='classified').count(),
            'minor_cases_count': minor_cases,
            'major_cases_count': major_cases,
            'recent_reports': reports.order_by('-created_at')[:10],
        })
    elif user.role == 'counselor':
        major_cases = IncidentReport.objects.filter(classification__severity='major')
        upcoming_sessions = CounselingSession.objects.filter(
            counselor=user,
            status='scheduled',
            scheduled_date__gte=timezone.now()
        ).order_by('scheduled_date')[:5]
        
        # Calculate real counseling success rate
        total_sessions = CounselingSession.objects.filter(counselor=user).count()
        completed_sessions = CounselingSession.objects.filter(
            counselor=user, 
            status='completed'
        ).count()
        success_rate = int((completed_sessions / total_sessions * 100)) if total_sessions > 0 else 0
        
        # Count PA and OSP based on incident type severity
        total_prohibited_acts = IncidentReport.objects.filter(
            incident_type__severity='prohibited'
        ).count()
        
        total_osp = IncidentReport.objects.filter(
            incident_type__severity='school_policy'
        ).count()
        
        # Scheduled sessions - from CounselingSession
        scheduled_sessions_count = CounselingSession.objects.filter(
            counselor=user,
            status='scheduled'
        ).count()
        
        # Completed sessions - from CounselingSession with status='completed'
        completed_sessions_count = CounselingSession.objects.filter(
            counselor=user,
            status='completed'
        ).count()
        
        # Completed VPF - fallback count
        completed_vpf = IncidentReport.objects.filter(
            status='vpf_completed'
        ).count()
        total_vpf_referrals = IncidentReport.objects.filter(
            status__in=['vpf_assigned', 'vpf_in_progress', 'vpf_completed']
        ).count()
        
        context.update({
            'total_prohibited_acts': total_prohibited_acts,
            'total_osp': total_osp,
            'scheduled_sessions': scheduled_sessions_count,
            'completed_vpf': completed_vpf,
            'total_vpf_referrals': total_vpf_referrals,
            'counseling_success_rate': success_rate,
            'completed_sessions': completed_sessions_count,
            'major_cases': major_cases.count(),
            'pending_evaluations': major_cases.filter(status='classified').count(),
            'recent_cases': major_cases.order_by('-created_at')[:5],
            'upcoming_sessions': upcoming_sessions,
        })
    elif user.role == 'principal':
        reports = IncidentReport.objects.all()
        total_reports = reports.count()
        resolved_reports = reports.filter(status='resolved').count()
        resolution_rate = int((resolved_reports / total_reports * 100)) if total_reports > 0 else 0
        
        context.update({
            'total_reports': total_reports,
            'resolution_rate': resolution_rate,
            'active_sanctions': 0,  # Placeholder since Sanction model doesn't exist
            'scheduled_sessions': CounselingSession.objects.filter(status='scheduled').count(),
            'repeat_offenders': CaseEvaluation.objects.filter(is_repeat_offender=True).count(),
            'total_students': CustomUser.objects.filter(role='student').count(),
            'active_teachers': CustomUser.objects.filter(role='teacher', is_active=True).count(),
            'active_cases': reports.exclude(status__in=['resolved', 'closed']).count(),
            'recent_reports': reports.order_by('-created_at')[:5],
        })
    elif user.role == 'esp_teacher':
        # ESP Teacher Dashboard - simplified
        context.update({
            'scheduled_vpf_sessions': 0,
            'completed_vpf': 0,
            'total_vpf_referrals': 0,
            'pending_vpf': 0,
            'ongoing_vpf': 0,
        })
    elif user.role in ['guidance', 'maintenance']:
        context.update({
            'total_users': CustomUser.objects.count(),
            'active_teachers': CustomUser.objects.filter(role='teacher', is_active=True).count(),
            'incident_types_count': IncidentType.objects.count(),
            'legal_references_count': LegalReference.objects.count(),
        })
    
    notifications = Notification.objects.filter(user=user, is_read=False).order_by('-created_at')[:5]
    context['notifications'] = notifications
    context['unread_count'] = Notification.objects.filter(user=user, is_read=False).count()
    
    return render(request, 'dashboard.html', context)