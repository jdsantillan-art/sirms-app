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
        CaseEvaluation, LegalReference, InvolvedParty
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
            context.update({
                'total_reports': reports.count(),
                'pending': reports.filter(status='pending').count(),
                'classified': reports.filter(status='classified').count(),
                'minor_cases_count': 0,
                'major_cases_count': 0,
                'recent_reports': reports.order_by('-created_at')[:10],
            })
        elif user.role == 'counselor':
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
    try:
        reports = IncidentReport.objects.all().order_by('-created_at')
        return render(request, 'all_reports.html', {'reports': reports})
    except:
        return render(request, 'all_reports.html', {'reports': []})


@login_required
def notifications(request):
    try:
        user_notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
        return render(request, 'notifications.html', {'notifications': user_notifications})
    except:
        return render(request, 'notifications.html', {'notifications': []})


@login_required
def account_settings(request):
    return render(request, 'account_settings.html')


# Add any other essential views here as needed...