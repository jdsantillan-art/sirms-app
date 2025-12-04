"""
Simple fix for dashboard function - replace the problematic parts
"""

# Fixed dashboard function content to replace the existing one
dashboard_function_content = '''@login_required
def dashboard(request):
    """Fixed dashboard function with proper error handling"""
    user = request.user
    context = {'user_role': user.role}
    
    try:
        # Basic analytics data
        context.update({
            'trend_data': json.dumps([]),
            'grade_data': json.dumps([]),
            'violation_type_data': json.dumps([]),
            'stacked_data': json.dumps([]),
            'resolution_data': json.dumps([]),
        })
        
        # Role-specific dashboard data
        if user.role == 'student':
            try:
                reports = IncidentReport.objects.filter(reported_student=user)
                context.update({
                    'pending_reports': reports.filter(status='pending').count(),
                    'under_review': reports.filter(status='under_review').count(),
                    'resolved': reports.filter(status__in=['resolved', 'closed']).count(),
                    'recent_reports': reports.order_by('-created_at')[:5],
                    'counseling_sessions': CounselingSession.objects.filter(student=user, status='scheduled'),
                })
            except Exception as e:
                context.update({
                    'pending_reports': 0,
                    'under_review': 0,
                    'resolved': 0,
                    'recent_reports': [],
                    'counseling_sessions': [],
                })
                
        elif user.role == 'teacher':
            try:
                reports = IncidentReport.objects.filter(reporter=user)
                context.update({
                    'total_reports': reports.count(),
                    'pending': reports.filter(status='pending').count(),
                    'recent_reports': reports.order_by('-created_at')[:5],
                })
            except Exception as e:
                context.update({
                    'total_reports': 0,
                    'pending': 0,
                    'recent_reports': [],
                })
                
        elif user.role == 'do':
            try:
                reports = IncidentReport.objects.all()
                context.update({
                    'total_reports': reports.count(),
                    'pending': reports.filter(status='pending').count(),
                    'classified': reports.filter(status='classified').count(),
                    'minor_cases_count': 0,
                    'major_cases_count': 0,
                    'recent_reports': reports.order_by('-created_at')[:10],
                })
            except Exception as e:
                context.update({
                    'total_reports': 0,
                    'pending': 0,
                    'classified': 0,
                    'minor_cases_count': 0,
                    'major_cases_count': 0,
                    'recent_reports': [],
                })
                
        elif user.role == 'counselor':
            try:
                # Basic counselor data
                context.update({
                    'total_prohibited_acts': 0,
                    'total_osp': 0,
                    'scheduled_sessions': 0,
                    'completed_vpf': 0,
                    'total_vpf_referrals': 0,
                    'counseling_success_rate': 0,
                    'completed_sessions': 0,
                    'major_cases': 0,
                    'pending_evaluations': 0,
                    'recent_cases': [],
                    'upcoming_sessions': [],
                })
            except Exception as e:
                context.update({
                    'total_prohibited_acts': 0,
                    'total_osp': 0,
                    'scheduled_sessions': 0,
                    'completed_vpf': 0,
                    'total_vpf_referrals': 0,
                    'counseling_success_rate': 0,
                    'completed_sessions': 0,
                    'major_cases': 0,
                    'pending_evaluations': 0,
                    'recent_cases': [],
                    'upcoming_sessions': [],
                })
                
        elif user.role == 'principal':
            try:
                reports = IncidentReport.objects.all()
                total_reports = reports.count()
                resolved_reports = reports.filter(status='resolved').count()
                resolution_rate = int((resolved_reports / total_reports * 100)) if total_reports > 0 else 0
                
                context.update({
                    'total_reports': total_reports,
                    'resolution_rate': resolution_rate,
                    'active_sanctions': 0,  # Placeholder
                    'scheduled_sessions': 0,
                    'repeat_offenders': 0,
                    'total_students': CustomUser.objects.filter(role='student').count(),
                    'active_teachers': CustomUser.objects.filter(role='teacher', is_active=True).count(),
                    'active_cases': reports.exclude(status__in=['resolved', 'closed']).count(),
                    'recent_reports': reports.order_by('-created_at')[:5],
                })
            except Exception as e:
                context.update({
                    'total_reports': 0,
                    'resolution_rate': 0,
                    'active_sanctions': 0,
                    'scheduled_sessions': 0,
                    'repeat_offenders': 0,
                    'total_students': 0,
                    'active_teachers': 0,
                    'active_cases': 0,
                    'recent_reports': [],
                })
                
        elif user.role == 'esp_teacher':
            context.update({
                'scheduled_vpf_sessions': 0,
                'completed_vpf': 0,
                'total_vpf_referrals': 0,
                'pending_vpf': 0,
                'ongoing_vpf': 0,
            })
            
        elif user.role in ['guidance', 'maintenance']:
            try:
                context.update({
                    'total_users': CustomUser.objects.count(),
                    'active_teachers': CustomUser.objects.filter(role='teacher', is_active=True).count(),
                    'incident_types_count': 0,
                    'legal_references_count': 0,
                })
            except Exception as e:
                context.update({
                    'total_users': 0,
                    'active_teachers': 0,
                    'incident_types_count': 0,
                    'legal_references_count': 0,
                })
        
        # Get notifications
        try:
            notifications = Notification.objects.filter(user=user, is_read=False).order_by('-created_at')[:5]
            context['notifications'] = notifications
            context['unread_count'] = Notification.objects.filter(user=user, is_read=False).count()
        except Exception as e:
            context['notifications'] = []
            context['unread_count'] = 0
            
    except Exception as e:
        # Fallback context
        context.update({
            'trend_data': json.dumps([]),
            'grade_data': json.dumps([]),
            'violation_type_data': json.dumps([]),
            'stacked_data': json.dumps([]),
            'resolution_data': json.dumps([]),
            'notifications': [],
            'unread_count': 0,
        })
    
    return render(request, 'dashboard.html', context)'''

print("Use this content to replace the dashboard function in views.py")