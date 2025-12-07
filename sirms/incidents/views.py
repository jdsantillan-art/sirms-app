"""
Minimal working views.py to replace the problematic one
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from django.utils import timezone
from django.http import JsonResponse
from django.db import models
from datetime import datetime, timedelta
import json

# Safe model imports
from .models import CustomUser, IncidentReport, Notification

# Try to import other models safely
try:
    from .models import (
        Classification, CounselingSession, IncidentType, 
        TeacherAssignment, Curriculum, ViolationHistory, 
        CaseEvaluation, LegalReference, InvolvedParty,
        VPFCase, VPFSchedule, CounselingSchedule, Counselor,
        InternalNote
    )
except ImportError:
    pass

# Safe form imports
try:
    from .forms import CustomUserCreationForm, IncidentReportForm
except ImportError:
    pass

# Safe utility imports
try:
    from .notification_utils import send_smart_notifications
except ImportError:
    def send_smart_notifications(*args, **kwargs):
        pass


def home(request):
    return render(request, 'home.html')


def health_check(request):
    return JsonResponse({'status': 'ok', 'service': 'sirms'})


def register(request):
    if request.method == 'POST':
        try:
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                user = form.save()
                messages.success(request, 'Registration successful! You can now log in.')
                
                # Auto-login after registration
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=password)
                if user:
                    login(request, user)
                    next_url = request.GET.get('next')
                    if next_url:
                        return redirect(next_url)
                    return redirect('dashboard')
                else:
                    messages.error(request, 'Registration succeeded, but auto-login failed. Please log in.')
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")
        except Exception as e:
            messages.error(request, 'Registration form error. Please try again.')
            form = CustomUserCreationForm()
    else:
        try:
            form = CustomUserCreationForm()
        except:
            form = None
    
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def dashboard(request):
    """Minimal working dashboard"""
    user = request.user
    context = {'user_role': user.role}
    
    # Basic empty analytics data
    context.update({
        'trend_data': json.dumps([]),
        'grade_data': json.dumps([]),
        'violation_type_data': json.dumps([]),
        'stacked_data': json.dumps([]),
        'resolution_data': json.dumps([]),
    })
    
    # Role-specific data with error handling
    try:
        if user.role == 'student':
            reports = IncidentReport.objects.filter(reported_student=user)
            context.update({
                'pending_reports': reports.filter(status='pending').count(),
                'under_review': reports.filter(status='under_review').count(),
                'resolved': reports.filter(status__in=['resolved', 'closed']).count(),
                'recent_reports': reports.order_by('-created_at')[:5],
                'counseling_sessions': [],
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
            # Calculate analytics data for initial load (monthly view)
            end_date = timezone.now()
            start_date = end_date - timedelta(days=365)
            
            # Trend data (12 months)
            trend_data = []
            for i in range(12):
                period_start = start_date + timedelta(days=30 * i)
                period_end = min(period_start + timedelta(days=30), end_date)
                count = reports.filter(
                    created_at__gte=period_start,
                    created_at__lt=period_end
                ).count()
                trend_data.append({
                    'month': period_start.strftime('%b'),
                    'reports': count
                })
            
            # Grade data
            grade_data = []
            for grade in range(7, 13):
                count = reports.filter(grade_level=str(grade)).count()
                grade_data.append({
                    'grade': f'Grade {grade}',
                    'count': count
                })
            
            # Month data (for monthly distribution)
            month_data = []
            month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            year_reports = reports.filter(created_at__gte=start_date)
            for month_num in range(1, 13):
                count = year_reports.filter(created_at__month=month_num).count()
                month_data.append({
                    'month': month_names[month_num - 1],
                    'reports': count
                })
            
            # Violation type data - Prohibited Acts vs Other School Policies
            try:
                prohibited_count = reports.filter(incident_type__severity='prohibited').count()
                school_policy_count = reports.filter(incident_type__severity='school_policy').count()
            except:
                prohibited_count = 0
                school_policy_count = 0
            
            violation_type_data = [
                {'name': 'Prohibited Acts', 'value': prohibited_count},
                {'name': 'Other School Policies', 'value': school_policy_count}
            ]
            
            context.update({
                'total_reports': reports.count(),
                'pending': reports.filter(status='pending').count(),
                'classified': reports.filter(status='classified').count(),
                'minor_cases_count': 0,
                'major_cases_count': 0,
                'recent_reports': reports.order_by('-created_at')[:10],
                'trend_data': json.dumps(trend_data),
                'grade_data': json.dumps(grade_data),
                'month_data': json.dumps(month_data),
                'violation_type_data': json.dumps(violation_type_data),
            })
        elif user.role == 'counselor':
            # Use same data as DO - all reports for analytics
            reports = IncidentReport.objects.all()
            # Calculate analytics data for initial load (monthly view)
            end_date = timezone.now()
            start_date = end_date - timedelta(days=365)
            
            # Trend data (12 months)
            trend_data = []
            for i in range(12):
                period_start = start_date + timedelta(days=30 * i)
                period_end = min(period_start + timedelta(days=30), end_date)
                count = reports.filter(
                    created_at__gte=period_start,
                    created_at__lt=period_end
                ).count()
                trend_data.append({
                    'month': period_start.strftime('%b'),
                    'reports': count
                })
            
            # Grade data
            grade_data = []
            for grade in range(7, 13):
                count = reports.filter(grade_level=str(grade)).count()
                grade_data.append({
                    'grade': f'Grade {grade}',
                    'count': count
                })
            
            # Month data (for monthly distribution)
            month_data = []
            month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            year_reports = reports.filter(created_at__gte=start_date)
            for month_num in range(1, 13):
                count = year_reports.filter(created_at__month=month_num).count()
                month_data.append({
                    'month': month_names[month_num - 1],
                    'reports': count
                })
            
            # Violation type data - Prohibited Acts vs Other School Policies
            try:
                prohibited_count = reports.filter(incident_type__severity='prohibited').count()
                school_policy_count = reports.filter(incident_type__severity='school_policy').count()
            except:
                prohibited_count = 0
                school_policy_count = 0
            
            violation_type_data = [
                {'name': 'Prohibited Acts', 'value': prohibited_count},
                {'name': 'Other School Policies', 'value': school_policy_count}
            ]
            
            # Calculate real counter card data for counselor
            try:
                # Prohibited Acts - count reports with prohibited severity
                total_prohibited_acts = reports.filter(incident_type__severity='prohibited').count()
                
                # OSP Cases - count reports with school_policy severity
                total_osp = reports.filter(incident_type__severity='school_policy').count()
                
                # Scheduled Sessions - count from CounselingSchedule
                try:
                    from .models import CounselingSchedule
                    scheduled_sessions_count = CounselingSchedule.objects.filter(
                        counselor=user,
                        status='scheduled'
                    ).count()
                except:
                    scheduled_sessions_count = 0
                
                # Completed Sessions - count from CounselingSchedule
                try:
                    from .models import CounselingSchedule
                    completed_sessions_count = CounselingSchedule.objects.filter(
                        counselor=user,
                        status='completed'
                    ).count()
                except:
                    completed_sessions_count = 0
            except Exception as e:
                print(f"Error calculating counselor counters: {e}")
                total_prohibited_acts = 0
                total_osp = 0
                scheduled_sessions_count = 0
                completed_sessions_count = 0
            
            context.update({
                'total_prohibited_acts': total_prohibited_acts,
                'total_osp': total_osp,
                'scheduled_sessions': scheduled_sessions_count,
                'completed_sessions': completed_sessions_count,
                'completed_vpf': 0,
                'total_vpf_referrals': 0,
                'counseling_success_rate': 0,
                'major_cases': 0,
                'pending_evaluations': 0,
                'recent_cases': [],
                'upcoming_sessions': [],
                'trend_data': json.dumps(trend_data),
                'grade_data': json.dumps(grade_data),
                'month_data': json.dumps(month_data),
                'violation_type_data': json.dumps(violation_type_data),
            })
        elif user.role == 'principal':
            reports = IncidentReport.objects.all()
            total_reports = reports.count()
            resolved_reports = reports.filter(status='resolved').count()
            resolution_rate = int((resolved_reports / total_reports * 100)) if total_reports > 0 else 0
            
            context.update({
                'total_reports': total_reports,
                'resolution_rate': resolution_rate,
                'active_sanctions': 0,
                'scheduled_sessions': 0,
                'repeat_offenders': 0,
                'total_students': CustomUser.objects.filter(role='student').count(),
                'active_teachers': CustomUser.objects.filter(role='teacher', is_active=True).count(),
                'active_cases': reports.exclude(status__in=['resolved', 'closed']).count(),
                'recent_reports': reports.order_by('-created_at')[:5],
            })
        elif user.role == 'esp_teacher':
            try:
                from .models import VPFCase, VPFSchedule
                vpf_cases = VPFCase.objects.filter(assigned_to=user)
                
                # Calculate VRF trend data (monthly view)
                end_date = timezone.now()
                start_date = end_date - timedelta(days=365)
                
                vrf_trend_data = []
                for i in range(12):
                    period_start = start_date + timedelta(days=30 * i)
                    period_end = min(period_start + timedelta(days=30), end_date)
                    count = vpf_cases.filter(
                        created_at__gte=period_start,
                        created_at__lt=period_end
                    ).count()
                    vrf_trend_data.append({
                        'month': period_start.strftime('%b'),
                        'reports': count
                    })
                
                context.update({
                    'scheduled_vpf_sessions': VPFSchedule.objects.filter(esp_teacher=user, status='scheduled').count() if 'VPFSchedule' in dir() else 0,
                    'completed_vpf': vpf_cases.filter(status='completed').count(),
                    'total_vpf_referrals': vpf_cases.count(),
                    'pending_vpf': vpf_cases.filter(status='pending').count(),
                    'ongoing_vpf': vpf_cases.filter(status='ongoing').count(),
                    'vrf_trend_data': json.dumps(vrf_trend_data),
                })
            except Exception as e:
                print(f"ESP dashboard error: {e}")
                context.update({
                    'scheduled_vpf_sessions': 0,
                    'completed_vpf': 0,
                    'total_vpf_referrals': 0,
                    'pending_vpf': 0,
                    'ongoing_vpf': 0,
                    'vrf_trend_data': json.dumps([]),
                })
        elif user.role in ['guidance', 'maintenance']:
            context.update({
                'total_users': CustomUser.objects.count(),
                'active_teachers': CustomUser.objects.filter(role='teacher', is_active=True).count(),
                'incident_types_count': 0,
                'legal_references_count': 0,
            })
    except Exception as e:
        print(f"Dashboard error for {user.role}: {e}")
        # Fallback empty data
        pass
    
    # Get notifications safely
    try:
        notifications = Notification.objects.filter(user=user, is_read=False).order_by('-created_at')[:5]
        context['notifications'] = notifications
        context['unread_count'] = Notification.objects.filter(user=user, is_read=False).count()
    except Exception as e:
        context['notifications'] = []
        context['unread_count'] = 0
    
    return render(request, 'dashboard.html', context)


@login_required
def report_incident(request):
    """Minimal working report incident"""
    try:
        if request.method == 'POST':
            form = IncidentReportForm(request.POST, request.FILES)
            if form.is_valid():
                # Create basic report
                report = IncidentReport()
                report.reporter = request.user
                
                # Set basic fields
                report.reporter_first_name = form.cleaned_data.get('reporter_first_name', request.user.first_name)
                report.reporter_middle_name = form.cleaned_data.get('reporter_middle_name', '')
                report.reporter_last_name = form.cleaned_data.get('reporter_last_name', request.user.last_name)
                
                report.curriculum = form.cleaned_data.get('curriculum')
                report.grade_level = form.cleaned_data.get('grade_level')
                report.section_name = form.cleaned_data.get('section_name')
                report.teacher_name = form.cleaned_data.get('teacher_name')
                
                report.involved_students = form.cleaned_data.get('involved_students')
                report.student_gender = form.cleaned_data.get('student_gender', '')
                report.incident_date = form.cleaned_data.get('incident_date')
                report.incident_time = form.cleaned_data.get('incident_time')
                report.incident_type = form.cleaned_data.get('incident_type')
                report.description = form.cleaned_data.get('description')
                report.evidence = form.cleaned_data.get('evidence')
                
                report.save()
                
                messages.success(request, f'Report {report.case_id} submitted successfully')
                
                # Try to send notifications
                try:
                    do_users = CustomUser.objects.filter(role='do')
                    for do_user in do_users:
                        Notification.objects.create(
                            user=do_user,
                            title='New Incident Report Submitted',
                            message=f'New incident report {report.case_id} filed by {request.user.get_full_name()}.',
                            report=report
                        )
                except Exception as e:
                    print(f"Notification error: {e}")
                
                return redirect('my_reports')
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field.replace('_', ' ').title()}: {error}")
        else:
            form = IncidentReportForm()
            # Pre-fill reporter information
            try:
                form.fields['reporter_first_name'].initial = request.user.first_name
                form.fields['reporter_middle_name'].initial = getattr(request.user, 'middle_name', '')
                form.fields['reporter_last_name'].initial = request.user.last_name
            except:
                pass
        
        # Get context data
        try:
            context = {
                'form': form,
                'incident_types': IncidentType.objects.all().order_by('severity', 'name'),
                'teacher_assignments': TeacherAssignment.objects.all(),
            }
        except:
            context = {
                'form': form,
                'incident_types': [],
                'teacher_assignments': [],
            }
        
        return render(request, 'report_incident.html', context)
        
    except Exception as e:
        print(f"Report incident error: {e}")
        messages.error(request, 'An error occurred. Please try again.')
        return redirect('dashboard')


@login_required
def my_reports(request):
    """Show reports created by the current user"""
    try:
        reports = IncidentReport.objects.filter(reporter=request.user).order_by('-created_at')
        return render(request, 'my_reports.html', {'reports': reports})
    except Exception as e:
        print(f"My reports error: {e}")
        return render(request, 'my_reports.html', {'reports': []})


# Placeholder functions for other views that might be called
@login_required
def all_reports(request):
    """All reports view - shows different reports based on user role"""
    try:
        user = request.user
        
        if user.role == 'do' or user.role == 'counselor' or user.role == 'guidance':
            # DO, Counselor, and Guidance see all reports (same content)
            reports = IncidentReport.objects.all().order_by('-created_at')
            
            # Handle filter parameters from counter card clicks
            filter_type = request.GET.get('type', '')
            filter_scheduled = request.GET.get('scheduled', '')
            filter_completed = request.GET.get('completed', '')
            
            # Apply filters based on counter card clicks
            if filter_type == 'prohibited':
                reports = reports.filter(incident_type__severity='prohibited')
            elif filter_type == 'school_policy':
                reports = reports.filter(incident_type__severity='school_policy')
            elif filter_scheduled == 'true':
                # Filter reports that have scheduled counseling sessions
                try:
                    from .models import CounselingSchedule, CaseEvaluation
                    scheduled_evaluations = CounselingSchedule.objects.filter(
                        status='scheduled',
                        counselor=user
                    ).values_list('evaluation_id', flat=True)
                    if scheduled_evaluations:
                        report_ids = CaseEvaluation.objects.filter(
                            id__in=scheduled_evaluations
                        ).values_list('report_id', flat=True)
                        reports = reports.filter(id__in=report_ids)
                    else:
                        reports = reports.none()
                except Exception as e:
                    print(f"Error filtering scheduled reports: {e}")
                    reports = reports.none()
            elif filter_completed == 'true':
                # Filter reports that have completed counseling sessions
                try:
                    from .models import CounselingSchedule, CaseEvaluation
                    completed_evaluations = CounselingSchedule.objects.filter(
                        status='completed',
                        counselor=user
                    ).values_list('evaluation_id', flat=True)
                    if completed_evaluations:
                        report_ids = CaseEvaluation.objects.filter(
                            id__in=completed_evaluations
                        ).values_list('report_id', flat=True)
                        reports = reports.filter(id__in=report_ids)
                    else:
                        reports = reports.none()
                except Exception as e:
                    print(f"Error filtering completed reports: {e}")
                    reports = reports.none()
            
            context = {
                'reports': reports,
                'user_role': user.role,
                'total_count': IncidentReport.objects.all().count(),
                'pending_count': IncidentReport.objects.filter(status='pending').count(),
                'under_review_count': IncidentReport.objects.filter(status='under_review').count(),
                'classified_count': IncidentReport.objects.filter(status='classified').count(),
                'resolved_count': IncidentReport.objects.filter(status='resolved').count(),
            }
            
        elif user.role == 'principal':
            # Principal sees all reports
            reports = IncidentReport.objects.all().order_by('-created_at')
            context = {
                'reports': reports,
                'user_role': user.role,
                'total_count': reports.count(),
                'pending_count': reports.filter(status='pending').count(),
                'under_review_count': reports.filter(status='under_review').count(),
                'classified_count': reports.filter(status='classified').count(),
                'resolved_count': reports.filter(status='resolved').count(),
            }
            
        else:
            # Other roles see limited reports
            reports = IncidentReport.objects.filter(
                Q(reporter=user) | Q(reported_student=user)
            ).order_by('-created_at')
            context = {
                'reports': reports,
                'user_role': user.role,
            }
        
        return render(request, 'all_reports.html', context)
        
    except Exception as e:
        print(f"All reports error: {e}")
        return render(request, 'all_reports.html', {'reports': [], 'user_role': request.user.role})


@login_required
def notifications(request):
    try:
        # Handle marking notification as read via POST
        if request.method == 'POST':
            notification_id = request.POST.get('notification_id')
            if notification_id:
                try:
                    notification = Notification.objects.get(id=notification_id, user=request.user)
                    notification.is_read = True
                    notification.save()
                except Notification.DoesNotExist:
                    pass
        
        user_notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
        return render(request, 'notifications.html', {'notifications': user_notifications})
    except:
        return render(request, 'notifications.html', {'notifications': []})


@login_required
def account_settings(request):
    return render(request, 'account_settings.html')


# Add any other essential views here as needed...

# Additional required functions for URLs
@login_required
def analytics_dashboard(request):
    """Analytics dashboard with real data"""
    from django.utils import timezone
    from django.db.models import Count, Q
    from datetime import datetime, timedelta
    import json
    
    try:
        user = request.user
        
        # Only allow DO and Guidance (counselor) roles
        if user.role not in ['do', 'counselor']:
            return redirect('dashboard')
        
        # Calculate school year start (June of current year or previous year)
        now = timezone.now()
        if now.month >= 6:
            school_year_start = datetime(now.year, 6, 1).date()
        else:
            school_year_start = datetime(now.year - 1, 6, 1).date()
        
        # Case Trend Analysis - Last 12 months (school year months)
        school_months = ['Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar', 'Apr', 'May']
        trend_data = []
        
        for i, month_name in enumerate(school_months):
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
            
            # Convert to datetime for query
            from datetime import time as dt_time
            month_start_dt = timezone.make_aware(datetime.combine(month_start, dt_time.min))
            month_end_dt = timezone.make_aware(datetime.combine(month_end, dt_time.max))
            
            month_reports = IncidentReport.objects.filter(
                created_at__range=[month_start_dt, month_end_dt]
            ).count()
            
            trend_data.append({
                'month': month_name,
                'reports': month_reports
            })
        
        # Reports by Grade Level - Bar Chart
        grade_data = []
        for grade in range(7, 13):
            count = IncidentReport.objects.filter(grade_level=str(grade)).count()
            grade_data.append({
                'grade': f'G{grade}',
                'count': count
            })
        
        # Prohibited Acts vs Other School Policies - Pie Chart
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
        
        # Stacked data for Major vs Minor (if needed)
        stacked_data = []
        for i, month_name in enumerate(school_months):
            month_num = (6 + i) if (6 + i) <= 12 else (6 + i - 12)
            year_offset = 0 if (6 + i) <= 12 else 1
            
            month_start = school_year_start.replace(month=month_num, day=1)
            if year_offset == 1:
                month_start = month_start.replace(year=month_start.year + 1)
            
            if month_num == 12:
                month_end = month_start.replace(day=31)
            else:
                next_month = month_start.replace(month=month_num + 1) if month_num < 12 else month_start.replace(year=month_start.year + 1, month=1)
                month_end = next_month - timedelta(days=1)
            
            from datetime import time as dt_time
            month_start_dt = timezone.make_aware(datetime.combine(month_start, dt_time.min))
            month_end_dt = timezone.make_aware(datetime.combine(month_end, dt_time.max))
            
            # Get major and minor counts
            major = IncidentReport.objects.filter(
                created_at__range=[month_start_dt, month_end_dt],
                classification__severity='major'
            ).count()
            
            minor = IncidentReport.objects.filter(
                created_at__range=[month_start_dt, month_end_dt],
                classification__severity='minor'
            ).count()
            
            stacked_data.append({
                'month': month_name,
                'major': major,
                'minor': minor
            })
        
        # Role-specific metrics
        if user.role == 'do':
            total_reports = IncidentReport.objects.count()
            pending = IncidentReport.objects.filter(status='pending').count()
            classified_today = IncidentReport.objects.filter(
                status='classified',
                created_at__date=timezone.now().date()
            ).count()
            major_cases_count = IncidentReport.objects.filter(
                classification__severity='major'
            ).count()
            
            context = {
                'user': user,
                'user_role': user.role,
                'total_reports': total_reports,
                'pending': pending,
                'classified_today': classified_today,
                'major_cases_count': major_cases_count,
                'trend_data': json.dumps(trend_data),
                'grade_data': json.dumps(grade_data),
                'violation_type_data': json.dumps(violation_type_data),
                'stacked_data': json.dumps(stacked_data),
            }
        elif user.role == 'counselor':
            major_cases = IncidentReport.objects.filter(
                classification__severity='major'
            ).count()
            
            from .models import CounselingSchedule
            scheduled_sessions = CounselingSchedule.objects.filter(
                status='scheduled'
            ).count()
            
            completed_sessions = CounselingSchedule.objects.filter(
                status='completed'
            ).count()
            
            counseling_success_rate = 0
            if scheduled_sessions + completed_sessions > 0:
                counseling_success_rate = round((completed_sessions / (scheduled_sessions + completed_sessions)) * 100)
            
            from .models import CaseEvaluation
            pending_evaluations = CaseEvaluation.objects.filter(
                status='pending'
            ).count()
            
            context = {
                'user': user,
                'user_role': user.role,
                'major_cases': major_cases,
                'scheduled_sessions': scheduled_sessions,
                'counseling_success_rate': counseling_success_rate,
                'pending_evaluations': pending_evaluations,
                'trend_data': json.dumps(trend_data),
                'grade_data': json.dumps(grade_data),
                'violation_type_data': json.dumps(violation_type_data),
                'stacked_data': json.dumps(stacked_data),
                'resolution_data': json.dumps([]),
            }
        else:
            context = {'user_role': user.role}
        
        return render(request, 'analytics_dashboard.html', context)
    except Exception as e:
        print(f"Analytics dashboard error: {e}")
        import traceback
        traceback.print_exc()
        return redirect('dashboard')


@login_required
def report_detail(request, case_id):
    """Report detail view"""
    try:
        report = get_object_or_404(IncidentReport, case_id=case_id)
        
        # Check permissions - allow users to view reports they created or are involved in
        if request.user.role == 'student':
            # Students can view reports where they are the reported student or the reporter
            if report.reported_student != request.user and report.reporter != request.user:
                messages.error(request, 'You do not have permission to view this report.')
                return redirect('dashboard')
        elif request.user.role not in ['do', 'counselor', 'principal']:
            # Other roles can only view reports they created
            if report.reporter != request.user:
                messages.error(request, 'You do not have permission to view this report.')
                return redirect('dashboard')
        
        context = {'report': report, 'user': request.user}
        
        # Add classification if exists
        try:
            if hasattr(report, 'classification') and report.classification:
                context['classification'] = report.classification
        except:
            pass
        
        # Add counseling sessions related to this report
        try:
            if report.reported_student:
                counseling_sessions = CounselingSession.objects.filter(
                    student=report.reported_student,
                    report=report
                ).order_by('scheduled_date')
                context['counseling_sessions'] = counseling_sessions
        except:
            pass
        
        # Add internal notes for authorized users
        try:
            if request.user.role in ['do', 'counselor', 'principal']:
                internal_notes = InternalNote.objects.filter(
                    report=report
                ).order_by('-created_at')
                context['internal_notes'] = internal_notes
        except:
            pass
        
        return render(request, 'report_detail.html', context)
    except Exception as e:
        messages.error(request, 'Report not found.')
        return redirect('all_reports')


@login_required
def counseling_schedule(request):
    """Display counseling schedules set by DO, Guidance, and ESP teachers for the reporter"""
    from django.utils import timezone
    from .models import DOSchedule, CounselingSchedule, VPFSchedule
    
    # Only allow students and teachers to view their schedules
    if request.user.role not in ['student', 'teacher']:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('dashboard')
    
    # Get all schedules where the current user is the reporter
    # 1. DO Schedules - where report.reporter = current_user
    do_schedules = DOSchedule.objects.filter(
        report__reporter=request.user
    ).select_related('report', 'discipline_officer', 'student').order_by('scheduled_date')
    
    # 2. Counseling Schedules (from Guidance) - where evaluation.report.reporter = current_user
    counseling_schedules = CounselingSchedule.objects.filter(
        evaluation__report__reporter=request.user
    ).select_related('evaluation__report', 'counselor', 'student').order_by('scheduled_date')
    
    # 3. VPF Schedules (from ESP) - where vpf_case.report.reporter = current_user
    vpf_schedules = VPFSchedule.objects.filter(
        vpf_case__report__reporter=request.user
    ).select_related('vpf_case__report', 'esp_teacher', 'vpf_case__student').order_by('scheduled_date')
    
    # Combine all schedules into a unified list with type information
    all_schedules = []
    
    # Add DO schedules
    for schedule in do_schedules:
        all_schedules.append({
            'type': 'DO',
            'schedule': schedule,
            'scheduled_date': schedule.scheduled_date,
            'status': schedule.status,
            'location': schedule.location,
            'notes': schedule.notes or schedule.purpose,
            'scheduled_by': schedule.discipline_officer.get_full_name() if schedule.discipline_officer else 'Discipline Officer',
            'student': schedule.student,
            'report': schedule.report,
            'schedule_type': schedule.get_schedule_type_display(),
        })
    
    # Add Counseling schedules
    for schedule in counseling_schedules:
        all_schedules.append({
            'type': 'Counseling',
            'schedule': schedule,
            'scheduled_date': schedule.scheduled_date,
            'status': schedule.status,
            'location': schedule.location,
            'notes': schedule.notes,
            'scheduled_by': schedule.counselor.get_full_name() if schedule.counselor else 'Guidance Counselor',
            'student': schedule.student,
            'report': schedule.evaluation.report if schedule.evaluation else None,
            'schedule_type': 'Counseling Session',
        })
    
    # Add VPF schedules
    for schedule in vpf_schedules:
        all_schedules.append({
            'type': 'VPF',
            'schedule': schedule,
            'scheduled_date': schedule.scheduled_date,
            'status': schedule.status,
            'location': schedule.location,
            'notes': schedule.notes,
            'scheduled_by': schedule.esp_teacher.get_full_name() if schedule.esp_teacher else 'ESP Teacher',
            'student': schedule.vpf_case.student if schedule.vpf_case else None,
            'report': schedule.vpf_case.report if schedule.vpf_case else None,
            'schedule_type': 'VPF Session',
        })
    
    # Sort by scheduled date
    all_schedules.sort(key=lambda x: x['scheduled_date'])
    
    # Separate upcoming and past schedules
    now = timezone.now()
    upcoming_schedules = [s for s in all_schedules if s['scheduled_date'] >= now and s['status'] in ['scheduled', 'rescheduled']]
    past_schedules = [s for s in all_schedules if s['scheduled_date'] < now or s['status'] in ['completed', 'missed', 'cancelled', 'no_show']]
    
    context = {
        'user_role': request.user.role,
        'all_schedules': all_schedules,
        'upcoming_schedules': upcoming_schedules,
        'past_schedules': past_schedules,
        'total_schedules': len(all_schedules),
    }
    
    return render(request, 'counseling_schedule.html', context)


@login_required
def create_sanction(request, case_id):
    """Create sanction placeholder"""
    try:
        report = get_object_or_404(IncidentReport, case_id=case_id)
        context = {'report': report}
        return render(request, 'create_sanction.html', context)
    except:
        messages.error(request, 'Report not found.')
        return redirect('all_reports')


# Additional functions that might be referenced in URLs
@login_required
def violation_history(request):
    """Violation history placeholder"""
    try:
        context = {'user_role': request.user.role}
        return render(request, 'violation_history.html', context)
    except:
        return redirect('dashboard')


@login_required
def legal_references(request):
    """Legal references placeholder"""
    try:
        context = {'user_role': request.user.role}
        return render(request, 'legal_references.html', context)
    except:
        return redirect('dashboard')


@login_required
def advisee_records(request):
    """Advisee records placeholder"""
    try:
        context = {'user_role': request.user.role}
        return render(request, 'advisee_records.html', context)
    except:
        return redirect('dashboard')


@login_required
def fact_check_reports(request):
    """Fact check reports - DO can verify and classify incident reports"""
    try:
        # Handle POST request for classification
        if request.method == 'POST':
            report_id = request.POST.get('report_id')
            action = request.POST.get('action')
            
            if report_id and action == 'verify':
                try:
                    report = IncidentReport.objects.get(id=report_id)
                    evidence_status = request.POST.get('evidence_status')
                    
                    if evidence_status == 'insufficient':
                        # Request more evidence
                        evidence_notes = request.POST.get('evidence_notes')
                        report.status = 'needs_evidence'
                        report.notes = f"Evidence needed: {evidence_notes}"
                        report.save()
                        
                        # Create notification for reporter
                        try:
                            Notification.objects.create(
                                user=report.reporter,
                                title='Additional Evidence Required',
                                message=f'Your report {report.case_id} needs additional evidence: {evidence_notes}',
                                report=report
                            )
                        except:
                            pass
                        
                        messages.success(request, f'Report {report.case_id} marked as needing more evidence.')
                    else:
                        # Classify the report
                        severity = request.POST.get('severity')
                        student_id = request.POST.get('student_id')
                        notes = request.POST.get('notes', '')
                        
                        # Update report status and classification
                        if severity == 'minor':
                            report.status = 'classified'
                            report.classification = 'minor'
                        elif severity == 'major':
                            report.status = 'classified'
                            report.classification = 'major'
                        
                        # Assign student if provided
                        if student_id:
                            try:
                                student = CustomUser.objects.get(id=student_id, role='student')
                                report.reported_student = student
                            except:
                                pass
                        
                        if notes:
                            report.notes = notes
                        
                        report.save()
                        
                        # Create notifications based on classification
                        try:
                            if severity == 'minor':
                                # Notify DO users
                                do_users = CustomUser.objects.filter(role='do')
                                for do_user in do_users:
                                    Notification.objects.create(
                                        user=do_user,
                                        title='Minor Case Classified',
                                        message=f'Report {report.case_id} classified as minor case for DO handling.',
                                        report=report
                                    )
                            elif severity == 'major':
                                # Notify counselors
                                counselors = CustomUser.objects.filter(role='counselor')
                                for counselor in counselors:
                                    Notification.objects.create(
                                        user=counselor,
                                        title='Major Case Referred',
                                        message=f'Report {report.case_id} classified as major case requiring counseling.',
                                        report=report
                                    )
                        except:
                            pass
                        
                        messages.success(request, f'Report {report.case_id} successfully classified as {severity} case.')
                    
                except Exception as e:
                    messages.error(request, f'Error processing report: {str(e)}')
            
            return redirect('fact_check_reports')
        
        # GET request - show pending reports
        reports = IncidentReport.objects.filter(status='pending').order_by('-created_at')
        
        # Get statistics
        total_pending = reports.count()
        today_reports = reports.filter(created_at__date=timezone.now().date()).count()
        urgent_reports = reports.filter(
            incident_type__severity='prohibited'
        ).count() if hasattr(reports.first(), 'incident_type') else 0
        
        # Get all students for the dropdown
        students = CustomUser.objects.filter(role='student', is_active=True).order_by('first_name', 'last_name')
        
        context = {
            'user_role': request.user.role,
            'reports': reports,
            'total_pending': total_pending,
            'today_reports': today_reports,
            'urgent_reports': urgent_reports,
            'students': students,
        }
        
        return render(request, 'do/fact_check_reports.html', context)
        
    except Exception as e:
        print(f"Fact check reports error: {e}")
        messages.error(request, 'Error loading fact check reports.')
        return redirect('dashboard')


@login_required
def major_case_review(request):
    """Major case review - Counselors review and evaluate major cases"""
    try:
        # Handle POST request for case evaluation
        if request.method == 'POST':
            case_id = request.POST.get('case_id')
            action = request.POST.get('action')
            
            if case_id and action:
                try:
                    report = IncidentReport.objects.get(case_id=case_id)
                    
                    if action == 'start_evaluation':
                        report.status = 'under_review'
                        report.save()
                        messages.success(request, f'Started evaluation for case {case_id}')
                        
                    elif action == 'schedule_counseling':
                        # Create counseling session
                        report.status = 'counseling_scheduled'
                        report.save()
                        messages.success(request, f'Counseling scheduled for case {case_id}')
                        
                    elif action == 'complete_evaluation':
                        evaluation_notes = request.POST.get('evaluation_notes', '')
                        recommendation = request.POST.get('recommendation', '')
                        
                        report.status = 'evaluated'
                        report.notes = f"Evaluation: {evaluation_notes}\nRecommendation: {recommendation}"
                        report.save()
                        
                        # Create case evaluation record
                        try:
                            CaseEvaluation.objects.create(
                                report=report,
                                counselor=request.user,
                                evaluation_notes=evaluation_notes,
                                recommendation=recommendation,
                                evaluation_date=timezone.now()
                            )
                        except:
                            pass
                        
                        messages.success(request, f'Evaluation completed for case {case_id}')
                        
                except Exception as e:
                    messages.error(request, f'Error processing case: {str(e)}')
            
            return redirect('major_case_review')
        
        # GET request - show the review page
        # Add your GET request handling here
        return render(request, 'counselor/major_case_review.html', {})
    except Exception as e:
        messages.error(request, f'Error: {str(e)}')
        return redirect('dashboard')


@login_required
def major_case_detail(request, case_id):
    """Major case detail placeholder"""
    try:
        report = get_object_or_404(IncidentReport, case_id=case_id)
        context = {'report': report}
        return render(request, 'counselor/major_case_detail.html', context)
    except:
        return redirect('major_case_review')


@login_required
def counseling_management(request):
    """Counseling management placeholder"""
    try:
        context = {'user_role': request.user.role}
        return render(request, 'counselor/counseling_management.html', context)
    except:
        return redirect('dashboard')


@login_required
def case_evaluation(request):
    """Case evaluation - routes VRF to ESP Teacher, others to Counseling Schedule"""
    if request.user.role not in ['counselor', 'guidance']:
        return redirect('dashboard')
    
    if request.method == 'POST':
        report_id = request.POST.get('report_id')
        commission = request.POST.get('commission')
        intervention = request.POST.get('intervention')
        status = request.POST.get('status')
        notes = request.POST.get('notes', '')
        
        try:
            report = IncidentReport.objects.get(id=report_id)
        except IncidentReport.DoesNotExist:
            messages.error(request, 'Report not found.')
            return redirect('case_evaluation')
        
        # Check if report has a student
        if not report.reported_student:
            messages.error(request, f'Cannot evaluate case {report.case_id}: No student associated with this report.')
            return redirect('case_evaluation')
        
        # Check if evaluation already exists
        if hasattr(report, 'evaluation'):
            messages.error(request, f'Case {report.case_id} has already been evaluated.')
            return redirect('case_evaluation')
        
        # Determine recommendation based on intervention
        recommendation = 'counseling'  # default
        if intervention and ('VPF' in intervention or 'Values Reflective Formation' in intervention):
            recommendation = 'monitoring'
        
        # Create evaluation
        try:
            evaluation = CaseEvaluation.objects.create(
                report=report,
                evaluated_by=request.user,
                recommendation=recommendation,
                verdict='pending',
                is_repeat_offender=False,
                evaluation_notes=f"Commission: {commission}\nIntervention: {intervention}\nStatus: {status}\n{notes}"
            )
            
            # Update report status
            report.status = 'evaluated'
            report.save()
            
            # If VRF selected, create VPF case for ESP Teacher to manage
            if intervention and ('VPF' in intervention or 'Values Reflective Formation' in intervention):
                vpf_case = VPFCase.objects.create(
                    report=report,
                    student=report.reported_student,
                    assigned_by=request.user,
                    commission_level=commission,
                    intervention=intervention,
                    status='pending',
                    notes=f"Commission: {commission}\nIntervention: {intervention}\nEvaluation Notes: {notes}"
                )
                
                # Notify ALL ESP Teachers (they will manage VPF)
                esp_teachers = CustomUser.objects.filter(role='esp_teacher')
                for esp_teacher in esp_teachers:
                    Notification.objects.create(
                        user=esp_teacher,
                        title='New VPF Case Assigned',
                        message=f'Case {report.case_id} has been assigned for VPF - {commission}. Student: {report.reported_student.get_full_name()}. Please schedule the VPF session.',
                        report=report
                    )
                
                # Notify the reporter (adviser/teacher)
                if report.reporter:
                    Notification.objects.create(
                        user=report.reporter,
                        title='Case Evaluated - VPF Assigned',
                        message=f'Case {report.case_id} has been evaluated. The student will undergo Values Reflective Formation (VPF) - {commission}. ESP Teacher will schedule the session.',
                        report=report
                    )
                
                # Notify the student
                if report.reported_student:
                    Notification.objects.create(
                        user=report.reported_student,
                        title='VPF Case Assigned',
                        message=f'You have been assigned to Values Reflective Formation (VPF) for case {report.case_id}. The ESP Teacher will schedule your session.',
                        report=report
                    )
                
                messages.success(request, f'✅ VPF case created for {report.reported_student.get_full_name()}. ESP Teachers have been notified. Case will appear in "For VRF" sidebar.')
            else:
                # Non-VPF intervention - Save to Counseling Schedule sidebar
                # Create a pending counseling schedule entry (counselor will set actual date/time later)
                counseling_schedule = CounselingSchedule.objects.create(
                    evaluation=evaluation,
                    counselor=request.user,
                    student=report.reported_student,
                    scheduled_date=timezone.now() + timedelta(days=7),  # Default 7 days from now
                    location='Guidance Office',
                    notes=f"Commission: {commission}\nIntervention: {intervention}\nStatus: {status}\n{notes}",
                    status='scheduled'
                )
                
                # Update report status to 'under_review' (ongoing) when counseling is scheduled
                report.status = 'under_review'
                report.save()
                
                # Notify the adviser (reporter)
                if report.reporter:
                    Notification.objects.create(
                        user=report.reporter,
                        title='Case Evaluated - Counseling Scheduled',
                        message=f'Case {report.case_id} has been evaluated. Intervention: {intervention}. The student will be scheduled for counseling.',
                        report=report
                    )
                
                # Notify the student
                if report.reported_student:
                    Notification.objects.create(
                        user=report.reported_student,
                        title='Counseling Session Scheduled',
                        message=f'Your case {report.case_id} has been evaluated. A counseling session will be scheduled. You will receive the schedule details soon.',
                        report=report
                    )
                
                messages.success(request, f'✅ Evaluation completed for {report.reported_student.get_full_name()}. Case saved to Counseling Schedule sidebar.')
            
            return redirect('case_evaluation')
            
        except Exception as e:
            messages.error(request, f'Error creating evaluation: {str(e)}')
            return redirect('case_evaluation')
    
    # Get cases ready for evaluation (not yet evaluated)
    cases_for_evaluation = IncidentReport.objects.filter(
        evaluation__isnull=True,
        reported_student__isnull=False
    ).exclude(
        status__in=['closed', 'resolved']
    ).order_by('-created_at')
    
    return render(request, 'counselor/case_evaluation.html', {
        'cases': cases_for_evaluation,
    })


@login_required
def counselor_schedule(request):
    """Counseling schedule page for non-VPF interventions"""
    if request.user.role not in ['counselor', 'guidance']:
        return redirect('dashboard')
    
    if request.method == 'POST':
        # Check if this is a status update request
        action = request.POST.get('action')
        if action == 'update_status':
            schedule_id = request.POST.get('schedule_id')
            new_status = request.POST.get('status')
            update_notes = request.POST.get('notes', '')
            
            schedule = get_object_or_404(CounselingSchedule, id=schedule_id, counselor=request.user)
            old_status = schedule.status
            schedule.status = new_status
            
            # Append notes if provided
            if update_notes:
                if schedule.notes:
                    schedule.notes += f"\n\n[{timezone.now().strftime('%Y-%m-%d %H:%M')}] Status updated from '{old_status}' to '{new_status}': {update_notes}"
                else:
                    schedule.notes = f"[{timezone.now().strftime('%Y-%m-%d %H:%M')}] Status updated from '{old_status}' to '{new_status}': {update_notes}"
            
            schedule.save()
            
            # Notify student if status changed
            if old_status != new_status:
                Notification.objects.create(
                    user=schedule.student,
                    title='Counseling Session Status Updated',
                    message=f'Your counseling session for case {schedule.evaluation.report.case_id} status has been updated to: {new_status}.',
                    report=schedule.evaluation.report
                )
            
            messages.success(request, f'Session status updated to {new_status}.')
            return redirect('counselor_schedule')
        
        # Regular scheduling request
        evaluation_id = request.POST.get('evaluation_id')
        scheduled_date_str = request.POST.get('scheduled_date')
        location = request.POST.get('location', '')
        notes = request.POST.get('notes', '')
        
        evaluation = get_object_or_404(CaseEvaluation, id=evaluation_id)
        
        # Parse the scheduled date and make it timezone-aware
        scheduled_date = datetime.fromisoformat(scheduled_date_str)
        
        # Make the datetime timezone-aware if it's naive
        if scheduled_date.tzinfo is None:
            scheduled_date = timezone.make_aware(scheduled_date)
        
        # Validation 1: Check if weekend
        if scheduled_date.weekday() >= 5:  # 5=Saturday, 6=Sunday
            messages.error(request, 'Weekend scheduling is not allowed. Please select a weekday.')
            return redirect(f'/counselor-schedule/?evaluation_id={evaluation_id}')
        
        # Validation 2: Check if in the past
        if scheduled_date < timezone.now():
            messages.error(request, 'Cannot schedule in the past. Please select a future date and time.')
            return redirect(f'/counselor-schedule/?evaluation_id={evaluation_id}')
        
        # Validation 3: Check for duplicate/conflict for this student
        time_window_start = scheduled_date - timedelta(hours=1)
        time_window_end = scheduled_date + timedelta(hours=1)
        
        existing_schedule = CounselingSchedule.objects.filter(
            student=evaluation.report.reported_student,
            scheduled_date__range=(time_window_start, time_window_end),
            status__in=['scheduled', 'rescheduled']
        ).exists()
        
        if existing_schedule:
            messages.error(request, f'Schedule conflict: {evaluation.report.reported_student.get_full_name()} already has a session scheduled within this time window. Please choose a different time.')
            return redirect(f'/counselor-schedule/?evaluation_id={evaluation_id}')
        
        # Create counseling schedule
        schedule = CounselingSchedule.objects.create(
            evaluation=evaluation,
            counselor=request.user,
            student=evaluation.report.reported_student,
            scheduled_date=scheduled_date,
            location=location,
            notes=notes,
            status='scheduled'
        )
        
        # Auto-update report status to 'under_review' (ongoing) when counseling is scheduled
        evaluation.report.status = 'under_review'
        evaluation.report.save()
        
        # Notify the student
        Notification.objects.create(
            user=evaluation.report.reported_student,
            title='Counseling Session Scheduled',
            message=f'Your counseling session for case {evaluation.report.case_id} has been scheduled for {schedule.scheduled_date.strftime("%B %d, %Y at %I:%M %p")}. Location: {location if location else "TBA"}',
            report=evaluation.report
        )
        
        # Notify the reporter
        if evaluation.report.reporter:
            Notification.objects.create(
                user=evaluation.report.reporter,
                title='Counseling Session Scheduled',
                message=f'A counseling session for case {evaluation.report.case_id} has been scheduled for {schedule.scheduled_date.strftime("%B %d, %Y at %I:%M %p")}.',
                report=evaluation.report
            )
        
        messages.success(request, f'Counseling session scheduled for {evaluation.report.reported_student.get_full_name()}. Notifications sent.')
        return redirect('counselor_schedule')
    
    # Get pending evaluations that need scheduling (non-VPF)
    pending_evaluations = CaseEvaluation.objects.filter(
        evaluated_by=request.user,
        counseling_schedules__isnull=True
    ).exclude(
        report__vpf_cases__isnull=False
    ).select_related('report', 'report__reported_student')
    
    # Get all scheduled sessions
    schedules = CounselingSchedule.objects.filter(
        counselor=request.user
    ).select_related('evaluation__report', 'student').order_by('scheduled_date')
    
    # Check if a specific evaluation is pre-selected
    selected_evaluation_id = request.GET.get('evaluation_id')
    selected_evaluation = None
    if selected_evaluation_id:
        try:
            selected_evaluation = pending_evaluations.get(id=selected_evaluation_id)
        except CaseEvaluation.DoesNotExist:
            pass
    
    return render(request, 'counselor/counselor_schedule.html', {
        'pending_evaluations': pending_evaluations,
        'schedules': schedules,
        'selected_evaluation': selected_evaluation,
        'today': timezone.now().date()
    })


@login_required
def evaluated_cases(request):
    """Evaluated cases placeholder"""
    try:
        context = {'user_role': request.user.role}
        return render(request, 'principal/evaluated_cases.html', context)
    except:
        return redirect('dashboard')


@login_required
def sanction_management(request):
    """Sanction management placeholder"""
    try:
        context = {'user_role': request.user.role}
        return render(request, 'principal/sanction_management.html', context)
    except:
        return redirect('dashboard')


@login_required
def final_verdicts(request):
    """Final verdicts placeholder"""
    try:
        context = {'user_role': request.user.role}
        return render(request, 'principal/final_verdicts.html', context)
    except:
        return redirect('dashboard')


@login_required
def student_monitoring(request):
    """Student monitoring placeholder"""
    try:
        context = {'user_role': request.user.role}
        return render(request, 'principal/student_monitoring.html', context)
    except:
        return redirect('dashboard')


@login_required
def reports_analytics(request):
    """Reports analytics placeholder"""
    try:
        context = {'user_role': request.user.role}
        return render(request, 'reports_analytics.html', context)
    except:
        return redirect('dashboard')


@login_required
def vpf_cases(request):
    """VPF Cases management for ESP Teachers - Only show cases assigned to them"""
    if request.user.role != 'esp_teacher':
        return redirect('dashboard')
    
    from .models import VPFCase, Counselor
    from django.db.models import Q
    
    # Find the Counselor record that matches this ESP teacher
    # Try matching by email first (most reliable), then by name
    esp_teacher_email = request.user.email
    esp_teacher_name = request.user.get_full_name()
    
    matching_counselors = Counselor.objects.filter(
        Q(email__iexact=esp_teacher_email) |  # Match by email (case-insensitive)
        Q(name__icontains=esp_teacher_name)    # Or match by name
    ).filter(is_active=True)
    
    # Get only VPF cases assigned to this ESP teacher
    if matching_counselors.exists():
        vpf_cases = VPFCase.objects.filter(
            esp_teacher_assigned__in=matching_counselors
        ).select_related(
            'student', 'report', 'assigned_by', 'esp_teacher_assigned'
        ).order_by('-assigned_at')
    else:
        # No matching counselor found, show empty list
        vpf_cases = VPFCase.objects.none()
    
    # Filter by status
    status_filter = request.GET.get('status', '')
    if status_filter:
        vpf_cases = vpf_cases.filter(status=status_filter)
    
    # Statistics
    total_cases = vpf_cases.count()
    pending_cases = vpf_cases.filter(status='pending').count()
    scheduled_cases = vpf_cases.filter(status='scheduled').count()
    completed_cases = vpf_cases.filter(status='completed').count()
    
    return render(request, 'esp/vpf_cases.html', {
        'vpf_cases': vpf_cases,
        'total_cases': total_cases,
        'pending_cases': pending_cases,
        'scheduled_cases': scheduled_cases,
        'completed_cases': completed_cases,
        'status_filter': status_filter,
    })


@login_required
def vpf_schedule(request):
    """VPF Schedule management for ESP Teachers"""
    if request.user.role != 'esp_teacher':
        return redirect('dashboard')
    
    from .models import VPFCase, VPFSchedule, Counselor
    from datetime import datetime, timedelta
    from django.db.models import Q
    
    if request.method == 'POST':
        vpf_case_id = request.POST.get('vpf_case_id')
        scheduled_date_str = request.POST.get('scheduled_date')
        location = request.POST.get('location', '')
        notes = request.POST.get('notes', '')
        
        vpf_case = get_object_or_404(VPFCase, id=vpf_case_id)
        
        # Parse the datetime string
        try:
            scheduled_date = datetime.fromisoformat(scheduled_date_str.replace('Z', '+00:00'))
        except:
            try:
                scheduled_date = datetime.strptime(scheduled_date_str, '%Y-%m-%dT%H:%M')
            except ValueError:
                scheduled_date = datetime.strptime(scheduled_date_str, '%Y-%m-%d %H:%M:%S')
        
        # Make timezone-aware if needed
        if scheduled_date.tzinfo is None:
            scheduled_date = timezone.make_aware(scheduled_date)
        
        # Check for duplicate schedule (same VPF case already scheduled)
        existing_schedule = VPFSchedule.objects.filter(
            vpf_case=vpf_case,
            status__in=['scheduled', 'ongoing']
        ).first()
        
        if existing_schedule:
            messages.error(request, f'This VPF case is already scheduled for {existing_schedule.scheduled_date.strftime("%B %d, %Y at %I:%M %p")}. Please cancel or complete the existing schedule first.')
            return redirect('vpf_schedule')
        
        # Check for time conflict (same ESP teacher, overlapping time)
        time_buffer = timedelta(hours=1)  # 1 hour buffer
        conflicting_schedules = VPFSchedule.objects.filter(
            esp_teacher=request.user,
            status__in=['scheduled', 'ongoing'],
            scheduled_date__gte=scheduled_date - time_buffer,
            scheduled_date__lte=scheduled_date + time_buffer
        )
        
        if conflicting_schedules.exists():
            conflict = conflicting_schedules.first()
            messages.error(request, f'Time conflict! You already have a session scheduled at {conflict.scheduled_date.strftime("%I:%M %p")} with {conflict.vpf_case.student.get_full_name()}. Please choose a different time.')
            return redirect('vpf_schedule')
        
        # Find matching counselor for this ESP teacher
        esp_teacher_email = request.user.email
        esp_teacher_name = request.user.get_full_name()
        matching_counselor = Counselor.objects.filter(
            Q(email__iexact=esp_teacher_email) |
            Q(name__icontains=esp_teacher_name)
        ).filter(is_active=True).first()
        
        # Create schedule
        schedule = VPFSchedule.objects.create(
            vpf_case=vpf_case,
            esp_teacher=request.user,
            counselor_assigned=matching_counselor,
            scheduled_date=scheduled_date,
            location=location,
            notes=notes,
            status='scheduled'
        )
        
        # Update VPF case status to 'scheduled'
        vpf_case.status = 'scheduled'
        vpf_case.save()
        
        # Notify student
        Notification.objects.create(
            user=vpf_case.student,
            title='VPF Session Scheduled',
            message=f'You have been scheduled for a Values Reflective Formation session on {scheduled_date.strftime("%B %d, %Y at %I:%M %p")}. Location: {location if location else "TBA"}. Please attend on time.',
            report=vpf_case.report
        )
        
        # Notify the guidance counselor who assigned the case
        if vpf_case.assigned_by:
            Notification.objects.create(
                user=vpf_case.assigned_by,
                title='VPF Session Scheduled',
                message=f'ESP Teacher {request.user.get_full_name()} has scheduled a VPF session for {vpf_case.student.get_full_name()} (Case {vpf_case.report.case_id}) on {scheduled_date.strftime("%B %d, %Y at %I:%M %p")}.',
                report=vpf_case.report
            )
        
        messages.success(request, f'VPF session scheduled for {vpf_case.student.get_full_name()} on {scheduled_date.strftime("%B %d, %Y at %I:%M %p")}')
        return redirect('vpf_schedule')
    
    # Find the Counselor record that matches this ESP teacher
    esp_teacher_email = request.user.email
    esp_teacher_name = request.user.get_full_name()
    
    matching_counselors = Counselor.objects.filter(
        Q(email__iexact=esp_teacher_email) |
        Q(name__icontains=esp_teacher_name)
    ).filter(is_active=True)
    
    # Get pending VPF cases assigned to this ESP teacher (not yet scheduled)
    if matching_counselors.exists():
        pending_vpf_cases = VPFCase.objects.filter(
            esp_teacher_assigned__in=matching_counselors,
            status='pending'
        ).select_related('student', 'report', 'esp_teacher_assigned')
    else:
        pending_vpf_cases = VPFCase.objects.none()
    
    # Get schedules for cases assigned to this ESP teacher
    if matching_counselors.exists():
        schedules = VPFSchedule.objects.filter(
            esp_teacher=request.user
        ).select_related('vpf_case__student', 'vpf_case__report', 'counselor_assigned').order_by('scheduled_date')
    else:
        schedules = VPFSchedule.objects.none()
    
    return render(request, 'esp/vpf_schedule.html', {
        'pending_vpf_cases': pending_vpf_cases,
        'schedules': schedules,
        'today': timezone.now().date()
    })


@login_required
def assign_vpf_teacher(request):
    """Assign VPF teacher placeholder"""
    try:
        context = {'user_role': request.user.role}
        return render(request, 'counselor/assign_vpf_teacher.html', context)
    except:
        return redirect('dashboard')


# Management functions
@login_required
def manage_curriculum(request):
    """Manage curriculum placeholder"""
    try:
        context = {'user_role': request.user.role}
        return render(request, 'maintenance/manage_curriculum.html', context)
    except:
        return redirect('dashboard')


@login_required
def manage_teachers(request):
    """Manage teachers placeholder"""
    try:
        context = {'user_role': request.user.role}
        return render(request, 'maintenance/manage_teachers.html', context)
    except:
        return redirect('dashboard')


@login_required
def manage_incident_types(request):
    """Manage incident types placeholder"""
    try:
        context = {'user_role': request.user.role}
        return render(request, 'maintenance/manage_incident_types.html', context)
    except:
        return redirect('dashboard')


@login_required
def manage_legal_references(request):
    """Manage legal references placeholder"""
    try:
        context = {'user_role': request.user.role}
        return render(request, 'maintenance/manage_legal_references.html', context)
    except:
        return redirect('dashboard')


@login_required
def manage_counselors(request):
    """Manage counselors placeholder"""
    try:
        context = {'user_role': request.user.role}
        return render(request, 'maintenance/manage_counselors.html', context)
    except:
        return redirect('dashboard')


@login_required
def manage_students(request):
    """Manage students placeholder"""
    try:
        context = {'user_role': request.user.role}
        return render(request, 'maintenance/manage_students.html', context)
    except:
        return redirect('dashboard')


@login_required
def backup_restore(request):
    """Backup restore placeholder"""
    try:
        context = {'user_role': request.user.role}
        return render(request, 'maintenance/backup_restore.html', context)
    except:
        return redirect('dashboard')


# API endpoints
@login_required
def dashboard_analytics_api(request):
    """Dashboard analytics API placeholder"""
    return JsonResponse({'status': 'ok', 'data': []})


@login_required
def export_report_api(request):
    """Export report API placeholder"""
    return JsonResponse({'status': 'ok', 'message': 'Export functionality not implemented'})


@login_required
def export_analytics(request):
    """Export analytics placeholder"""
    return JsonResponse({'status': 'ok', 'message': 'Export functionality not implemented'})


# Additional API endpoints that might be referenced
def get_tracks(request):
    """Get tracks API placeholder"""
    return JsonResponse({'tracks': []})


@login_required
def get_dashboard_analytics(request):
    """API endpoint for dynamic dashboard analytics based on time filter"""
    time_filter = request.GET.get('filter', 'monthly')
    user = request.user
    
    # Calculate date range based on filter
    end_date = timezone.now()
    if time_filter == 'monthly':
        # Last 12 months - use actual calendar months
        start_date = end_date - timedelta(days=365)
        periods = 12
        # Use actual month boundaries instead of fixed 30-day periods
        use_calendar_months = True
    elif time_filter == 'quarterly':
        # Last 8 quarters (2 years) - use actual quarters
        start_date = end_date - timedelta(days=730)
        periods = 8
        use_calendar_quarters = True
    else:  # yearly
        # Last 5 years - use actual calendar years
        start_date = end_date - timedelta(days=1825)
        periods = 5
        use_calendar_years = True
    
    response_data = {}
    
    if user.role == 'do' or user.role == 'counselor':
        # Use same data for both DO and Counselor - all reports filtered by time period
        # Calculate actual date range based on filter
        if time_filter == 'monthly':
            # Get last 12 actual calendar months
            from datetime import date
            current_date = end_date.date()
            actual_start_date = None
            for i in range(12):
                month_offset = 11 - i
                target_month = current_date.month - month_offset
                target_year = current_date.year
                while target_month <= 0:
                    target_month += 12
                    target_year -= 1
                if i == 0:
                    actual_start_date = timezone.make_aware(datetime.combine(date(target_year, target_month, 1), datetime.min.time()))
        elif time_filter == 'quarterly':
            # Get last 8 actual calendar quarters
            from datetime import date
            current_date = end_date.date()
            current_quarter = (current_date.month - 1) // 3 + 1
            current_year = current_date.year
            target_quarter = current_quarter - 7
            target_year = current_year
            while target_quarter <= 0:
                target_quarter += 4
                target_year -= 1
            quarter_start_month = (target_quarter - 1) * 3 + 1
            actual_start_date = timezone.make_aware(datetime.combine(date(target_year, quarter_start_month, 1), datetime.min.time()))
        else:  # yearly
            # Get last 5 actual calendar years
            from datetime import date
            target_year = end_date.year - 4
            actual_start_date = timezone.make_aware(datetime.combine(date(target_year, 1, 1), datetime.min.time()))
        
        reports = IncidentReport.objects.filter(created_at__gte=actual_start_date) if actual_start_date else IncidentReport.objects.filter(created_at__gte=start_date)
        
        # 1. Trend Cases (Wave graph) - Monthly/Quarterly/Yearly trend
        # Use actual calendar periods (months/quarters/years) instead of fixed day counts
        trend_data = []
        
        if time_filter == 'monthly':
            # Get last 12 actual calendar months
            from datetime import date
            current_date = end_date.date()
            for i in range(periods):
                # Calculate month and year (going backwards from current month)
                month_offset = periods - 1 - i
                target_month = current_date.month - month_offset
                target_year = current_date.year
                
                # Handle year rollover
                while target_month <= 0:
                    target_month += 12
                    target_year -= 1
                
                # Get first and last day of the month
                if target_month == 12:
                    next_month = 1
                    next_year = target_year + 1
                else:
                    next_month = target_month + 1
                    next_year = target_year
                
                period_start = timezone.make_aware(datetime.combine(date(target_year, target_month, 1), datetime.min.time()))
                period_end = timezone.make_aware(datetime.combine(date(next_year, next_month, 1), datetime.min.time()))
                
                period_reports = IncidentReport.objects.filter(
                    created_at__gte=period_start,
                    created_at__lt=period_end
                ).count()
                
                label = period_start.strftime('%b')
                trend_data.insert(0, {  # Insert at beginning to maintain chronological order
                    'month': label,
                    'reports': period_reports
                })
        
        elif time_filter == 'quarterly':
            # Get last 8 actual calendar quarters
            from datetime import date
            current_date = end_date.date()
            for i in range(periods):
                # Calculate quarter (going backwards from current quarter)
                quarter_offset = periods - 1 - i
                current_quarter = (current_date.month - 1) // 3 + 1
                current_year = current_date.year
                
                target_quarter = current_quarter - quarter_offset
                target_year = current_year
                
                # Handle year rollover
                while target_quarter <= 0:
                    target_quarter += 4
                    target_year -= 1
                
                # Get quarter start and end months
                quarter_start_month = (target_quarter - 1) * 3 + 1
                quarter_end_month = target_quarter * 3 + 1
                quarter_end_year = target_year
                
                if quarter_end_month > 12:
                    quarter_end_month = 1
                    quarter_end_year += 1
                
                period_start = timezone.make_aware(datetime.combine(date(target_year, quarter_start_month, 1), datetime.min.time()))
                period_end = timezone.make_aware(datetime.combine(date(quarter_end_year, quarter_end_month, 1), datetime.min.time()))
                
                period_reports = IncidentReport.objects.filter(
                    created_at__gte=period_start,
                    created_at__lt=period_end
                ).count()
                
                label = f'Q{target_quarter} {target_year}'
                trend_data.insert(0, {
                    'month': label,
                    'reports': period_reports
                })
        
        else:  # yearly
            # Get last 5 actual calendar years
            from datetime import date
            current_year = end_date.year
            for i in range(periods):
                target_year = current_year - (periods - 1 - i)
                
                period_start = timezone.make_aware(datetime.combine(date(target_year, 1, 1), datetime.min.time()))
                period_end = timezone.make_aware(datetime.combine(date(target_year + 1, 1, 1), datetime.min.time()))
                
                period_reports = IncidentReport.objects.filter(
                    created_at__gte=period_start,
                    created_at__lt=period_end
                ).count()
                
                label = str(target_year)
                trend_data.insert(0, {
                    'month': label,
                    'reports': period_reports
                })
        
        # 2. Grade Most Reported (Bar Graph) - Filtered by selected time period
        # Use the same filtered reports based on time period
        grade_data = []
        for grade in range(7, 13):
            count = reports.filter(grade_level=str(grade)).count()
            grade_data.append({
                'grade': f'Grade {grade}',
                'count': count
            })
        
        # 3. What Month Most Report (Line graph) - Use trend_data based on filter
        # The trend_data already contains the correct data for the selected filter
        month_data = trend_data.copy()  # Use the same trend data calculated above
        
        # Violation type data - Prohibited Acts vs Other School Policies - Filtered by time period
        # Use the same filtered reports based on time period
        try:
            prohibited_count = reports.filter(incident_type__severity='prohibited').count()
            school_policy_count = reports.filter(incident_type__severity='school_policy').count()
        except:
            prohibited_count = 0
            school_policy_count = 0
        
        violation_type_data = [
            {'name': 'Prohibited Acts', 'value': prohibited_count},
            {'name': 'Other School Policies', 'value': school_policy_count}
        ]
        
        response_data = {
            'trend_data': trend_data,
            'grade_data': grade_data,
            'month_data': month_data,
            'violation_type_data': violation_type_data,
        }
        
    elif user.role == 'esp_teacher':
        try:
            from .models import VPFCase, VPFSchedule
            
            # Get VPF cases for this ESP teacher
            vpf_cases = VPFCase.objects.filter(assigned_to=user)
            
            # 1. Status Distribution (Donut Chart) - Completed, Pending, Ongoing
            completed = vpf_cases.filter(status='completed').count()
            pending = vpf_cases.filter(status='pending').count()
            ongoing = vpf_cases.filter(status='ongoing').count()
            
            # 2. Most Incident refers to ESP For VRF (Wave/Line graph) - Trend over time
            vrf_trend_data = []
            for i in range(periods):
                period_start = start_date + timedelta(days=period_days * i)
                period_end = min(period_start + timedelta(days=period_days), end_date)
                
                period_count = vpf_cases.filter(
                    created_at__gte=period_start,
                    created_at__lt=period_end
                ).count()
                
                # Format label
                if time_filter == 'quarterly':
                    quarter = (period_start.month - 1) // 3 + 1
                    label = f'Q{quarter} {period_start.year}'
                elif time_filter == 'yearly':
                    label = str(period_start.year)
                else:  # monthly
                    label = period_start.strftime('%b')
                
                vrf_trend_data.append({
                    'month': label,
                    'reports': period_count
                })
            
            response_data = {
                'status_data': {
                    'completed': completed,
                    'pending': pending,
                    'ongoing': ongoing
                },
                'vrf_trend_data': vrf_trend_data,
            }
        except Exception as e:
            print(f"ESP analytics error: {e}")
            response_data = {
                'status_data': {'completed': 0, 'pending': 0, 'ongoing': 0},
                'vrf_trend_data': [],
            }
    
    return JsonResponse(response_data)


def get_grades(request):
    """Get grades API placeholder"""
    return JsonResponse({'grades': []})


def get_sections(request):
    """Get sections API placeholder"""
    return JsonResponse({'sections': []})


def get_teachers(request):
    """Get teachers API placeholder"""
    return JsonResponse({'teachers': []})


# Additional functions that might be needed
@login_required
def schedule_notification_detail(request, notification_id):
    """Schedule notification detail placeholder"""
    try:
        # Mark notification as read when viewed
        notification = Notification.objects.get(id=notification_id, user=request.user)
        if not notification.is_read:
            notification.is_read = True
            notification.save()
        
        context = {'notification_id': notification_id}
        return render(request, 'schedule_notification_detail.html', context)
    except:
        return redirect('notifications')


@login_required
def mark_notification_read(request, notification_id):
    """Mark notification as read and redirect to appropriate destination"""
    try:
        notification = Notification.objects.get(id=notification_id, user=request.user)
        
        # Mark as read
        if not notification.is_read:
            notification.is_read = True
            notification.save()
        
        # Redirect to appropriate destination
        if 'Session Scheduled' in notification.title or 'Appointment Scheduled' in notification.title:
            return redirect('schedule_notification_detail', notification_id=notification_id)
        elif notification.report:
            return redirect('report_detail', case_id=notification.report.case_id)
        else:
            return redirect('notifications')
    except Notification.DoesNotExist:
        return redirect('notifications')


# Test functions
def test_charts(request):
    """Test charts placeholder"""
    return render(request, 'test_charts.html', {})


def simple_chart_test(request):
    """Simple chart test placeholder"""
    return render(request, 'simple_chart_test.html', {})


# Additional counseling functions
@login_required
def complete_counseling_session(request, session_id):
    """Complete counseling session placeholder"""
    messages.success(request, 'Session completed successfully.')
    return redirect('counseling_management')


@login_required
def reschedule_counseling_session(request, session_id):
    """Reschedule counseling session placeholder"""
    messages.success(request, 'Session rescheduled successfully.')
    return redirect('counseling_management')


@login_required
def cancel_counseling_session(request, session_id):
    """Cancel counseling session placeholder"""
    messages.success(request, 'Session cancelled successfully.')
    return redirect('counseling_management')


@login_required
def complete_counseling_schedule(request, schedule_id):
    """Complete counseling schedule placeholder"""
    messages.success(request, 'Schedule completed successfully.')
    return redirect('counselor_schedule')


@login_required
def missed_counseling_schedule(request, schedule_id):
    """Missed counseling schedule placeholder"""
    messages.success(request, 'Schedule marked as missed.')
    return redirect('counselor_schedule')


@login_required
def update_vpf_status(request, vpf_id):
    """Update VPF status placeholder"""
    messages.success(request, 'VPF status updated successfully.')
    return redirect('vpf_cases')


# Additional placeholder functions to prevent URL errors
@login_required
def classify_violations(request):
    """Classify violations placeholder"""
    return redirect('fact_check_reports')


@login_required
def pre_counseling_schedule(request):
    """Pre-counseling schedule placeholder"""
    try:
        context = {'user_role': request.user.role}
        return render(request, 'do/pre_counseling_schedule.html', context)
    except:
        return redirect('dashboard')


@login_required
def case_history(request):
    """Case history placeholder"""
    try:
        context = {'user_role': request.user.role}
        return render(request, 'case_history.html', context)
    except:
        return redirect('dashboard')


@login_required
def internal_notes(request):
    """Internal notes placeholder"""
    try:
        context = {'user_role': request.user.role}
        return render(request, 'internal_notes.html', context)
    except:
        return redirect('dashboard')