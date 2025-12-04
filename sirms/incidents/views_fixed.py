"""
Fixed views.py with proper error handling and model imports
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

# Import models with error handling
try:
    from .models import (
        CustomUser, IncidentReport, Classification, CounselingSession,
        Notification, IncidentType, Section, TeacherAssignment,
        Curriculum, Track, Grade, ViolationHistory, CaseEvaluation,
        InternalNote, SystemBackup, ReportAnalytics, LegalReference,
        InvolvedParty, CounselingSchedule
    )
except ImportError as e:
    print(f"Model import error: {e}")
    # Fallback imports
    from .models import CustomUser, IncidentReport, Notification

# Import forms with error handling
try:
    from .forms import (
        CustomUserCreationForm, IncidentReportForm, ClassificationForm,
        CounselingSessionForm, CaseEvaluationForm,
        InternalNoteForm, CurriculumForm, TrackForm, GradeForm,
        SectionForm, TeacherAssignmentForm, IncidentTypeForm, ReportAnalyticsForm
    )
except ImportError as e:
    print(f"Form import error: {e}")
    from .forms import CustomUserCreationForm, IncidentReportForm

# Import utilities with error handling
try:
    from .notification_utils import send_smart_notifications
except ImportError:
    def send_smart_notifications(*args, **kwargs):
        pass  # Fallback function


def home(request):
    return render(request, 'home.html')


def health_check(request):
    """Simple health check endpoint for Render"""
    return JsonResponse({'status': 'ok', 'service': 'sirms'})


def register(request):
    if request.method == 'POST':
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
    else:
        form = CustomUserCreationForm()
    
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
    """Fixed dashboard function with proper error handling"""
    user = request.user
    context = {'user_role': user.role}
    
    try:
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
            try:
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
            except Exception as e:
                print(f"Error processing month {month_name}: {e}")
                trend_data.append({
                    'month': month_name,
                    'reports': 0
                })
        
        # Grade data - for Reports by Grade Level
        grade_data = []
        for grade in range(7, 13):
            try:
                count = IncidentReport.objects.filter(grade_level=str(grade)).count()
                grade_data.append({
                    'grade': f'Grade {grade}',
                    'count': count
                })
            except Exception as e:
                print(f"Error processing grade {grade}: {e}")
                grade_data.append({
                    'grade': f'Grade {grade}',
                    'count': 0
                })
        
        # Violation type data - Prohibited Acts vs Other School Policies
        try:
            prohibited_count = IncidentReport.objects.filter(
                incident_type__severity='prohibited'
            ).count()
            
            school_policy_count = IncidentReport.objects.filter(
                incident_type__severity='school_policy'
            ).count()
        except Exception as e:
            print(f"Error getting violation counts: {e}")
            prohibited_count = 0
            school_policy_count = 0
        
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
                print(f"Error in student dashboard: {e}")
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
                print(f"Error in teacher dashboard: {e}")
                context.update({
                    'total_reports': 0,
                    'pending': 0,
                    'recent_reports': [],
                })
                
        elif user.role == 'do':
            try:
                reports = IncidentReport.objects.all()
                
                # Count reports with classifications
                try:
                    minor_cases = reports.filter(classification__severity='minor').count()
                    major_cases = reports.filter(classification__severity='major').count()
                except:
                    minor_cases = 0
                    major_cases = 0
                
                # If no classifications exist, count by status instead
                if minor_cases == 0 and major_cases == 0:
                    minor_cases = reports.filter(
                        status__in=['pending', 'under_review', 'resolved']
                    ).exclude(
                        status='referred_to_counselor'
                    ).count()
                    
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
            except Exception as e:
                print(f"Error in DO dashboard: {e}")
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
                # Get major cases
                try:
                    major_cases = IncidentReport.objects.filter(classification__severity='major')
                except:
                    major_cases = IncidentReport.objects.none()
                
                # Get upcoming sessions
                try:
                    upcoming_sessions = CounselingSession.objects.filter(
                        counselor=user,
                        status='scheduled',
                        scheduled_date__gte=timezone.now()
                    ).order_by('scheduled_date')[:5]
                except:
                    upcoming_sessions = []
                
                # Calculate counseling success rate
                try:
                    total_sessions = CounselingSession.objects.filter(counselor=user).count()
                    completed_sessions = CounselingSession.objects.filter(
                        counselor=user, 
                        status='completed'
                    ).count()
                    success_rate = int((completed_sessions / total_sessions * 100)) if total_sessions > 0 else 0
                except:
                    total_sessions = 0
                    completed_sessions = 0
                    success_rate = 0
                
                # Count PA and OSP
                try:
                    total_prohibited_acts = IncidentReport.objects.filter(
                        incident_type__severity='prohibited'
                    ).count()
                    
                    total_osp = IncidentReport.objects.filter(
                        incident_type__severity='school_policy'
                    ).count()
                except:
                    total_prohibited_acts = 0
                    total_osp = 0
                
                # Scheduled sessions count
                try:
                    scheduled_sessions_count = CounselingSession.objects.filter(
                        counselor=user,
                        status='scheduled'
                    ).count()
                except:
                    scheduled_sessions_count = 0
                
                # VPF counts (fallback)
                completed_vpf = 0
                total_vpf_referrals = 0
                
                context.update({
                    'total_prohibited_acts': total_prohibited_acts,
                    'total_osp': total_osp,
                    'scheduled_sessions': scheduled_sessions_count,
                    'completed_vpf': completed_vpf,
                    'total_vpf_referrals': total_vpf_referrals,
                    'counseling_success_rate': success_rate,
                    'completed_sessions': completed_sessions,
                    'major_cases': major_cases.count(),
                    'pending_evaluations': major_cases.filter(status='classified').count(),
                    'recent_cases': major_cases.order_by('-created_at')[:5],
                    'upcoming_sessions': upcoming_sessions,
                })
            except Exception as e:
                print(f"Error in counselor dashboard: {e}")
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
                    'scheduled_sessions': CounselingSession.objects.filter(status='scheduled').count(),
                    'repeat_offenders': CaseEvaluation.objects.filter(is_repeat_offender=True).count(),
                    'total_students': CustomUser.objects.filter(role='student').count(),
                    'active_teachers': CustomUser.objects.filter(role='teacher', is_active=True).count(),
                    'active_cases': reports.exclude(status__in=['resolved', 'closed']).count(),
                    'recent_reports': reports.order_by('-created_at')[:5],
                })
            except Exception as e:
                print(f"Error in principal dashboard: {e}")
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
            # ESP Teacher Dashboard - simplified
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
                    'incident_types_count': IncidentType.objects.count(),
                    'legal_references_count': LegalReference.objects.count(),
                })
            except Exception as e:
                print(f"Error in guidance dashboard: {e}")
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
            print(f"Error getting notifications: {e}")
            context['notifications'] = []
            context['unread_count'] = 0
            
    except Exception as e:
        print(f"Major error in dashboard: {e}")
        # Fallback context
        context.update({
            'trend_data': json.dumps([]),
            'grade_data': json.dumps([]),
            'violation_type_data': json.dumps([]),
            'resolution_data': json.dumps([]),
            'notifications': [],
            'unread_count': 0,
        })
    
    return render(request, 'dashboard.html', context)


@login_required
def report_incident(request):
    """Fixed report incident function with proper error handling"""
    try:
        if request.method == 'POST':
            form = IncidentReportForm(request.POST, request.FILES)
            if form.is_valid():
                # Prevent duplicate submissions
                recent_duplicate = IncidentReport.objects.filter(
                    reporter=request.user,
                    created_at__gte=timezone.now() - timedelta(seconds=5)
                ).first()
                
                if recent_duplicate:
                    messages.info(request, f'Report {recent_duplicate.case_id} was already submitted.')
                    return redirect('my_reports')
                
                # Create the report
                report = IncidentReport()
                report.reporter = request.user
                
                # Set reporter information
                report.reporter_first_name = form.cleaned_data['reporter_first_name']
                report.reporter_middle_name = form.cleaned_data['reporter_middle_name']
                report.reporter_last_name = form.cleaned_data['reporter_last_name']
                
                # Set academic information
                report.curriculum = form.cleaned_data['curriculum']
                report.grade_level = form.cleaned_data['grade_level']
                report.section_name = form.cleaned_data['section_name']
                report.teacher_name = form.cleaned_data['teacher_name']
                
                # Set other fields
                report.involved_students = form.cleaned_data['involved_students']
                report.student_gender = form.cleaned_data.get('student_gender', '')
                report.incident_date = form.cleaned_data['incident_date']
                report.incident_time = form.cleaned_data['incident_time']
                report.incident_type = form.cleaned_data['incident_type']
                
                # Handle bullying type if provided
                bullying_type = request.POST.get('bullying_type', '')
                if bullying_type:
                    report.bullying_type = bullying_type
                
                report.description = form.cleaned_data['description']
                report.evidence = form.cleaned_data['evidence']
                
                # Try to find and assign the reported student
                involved_students_text = form.cleaned_data['involved_students']
                if involved_students_text:
                    import re
                    potential_identifiers = re.split(r'[,;\n]+', involved_students_text)
                    
                    for identifier in potential_identifiers:
                        identifier = identifier.strip()
                        if identifier:
                            # Try to find student by email
                            student = CustomUser.objects.filter(
                                role='student',
                                email__iexact=identifier
                            ).first()
                            
                            # If not found by email, try username
                            if not student:
                                student = CustomUser.objects.filter(
                                    role='student',
                                    username__iexact=identifier
                                ).first()
                            
                            # If not found by username, try to match by full name
                            if not student:
                                name_parts = identifier.split()
                                if len(name_parts) >= 2:
                                    first_name = name_parts[0]
                                    last_name = name_parts[-1]
                                    
                                    student = CustomUser.objects.filter(
                                        role='student',
                                        first_name__iexact=first_name,
                                        last_name__iexact=last_name
                                    ).first()
                            
                            # If found, assign as reported_student
                            if student:
                                report.reported_student = student
                                break
                
                report.save()
                
                # Handle involved parties
                try:
                    reporter_is_victim = request.POST.get('reporter_is_victim') == 'on'
                    is_confidential = request.POST.get('is_confidential') == 'on'
                    party_type = request.POST.get('party_type')
                    
                    # Update report with new fields
                    report.reporter_is_victim = reporter_is_victim
                    report.is_confidential = is_confidential
                    report.save()
                    
                    # Create involved party based on type
                    if party_type == 'student' and report.reported_student:
                        involved_party = InvolvedParty.objects.create(
                            party_type='student',
                            student=report.reported_student,
                        )
                        report.involved_parties.add(involved_party)
                        
                    elif party_type == 'teacher':
                        teacher_name = request.POST.get('teacher_name')
                        department = request.POST.get('department', '')
                        
                        if teacher_name:
                            involved_party = InvolvedParty.objects.create(
                                party_type='teacher',
                                name_if_unknown=teacher_name,
                                department=department,
                            )
                            report.involved_parties.add(involved_party)
                    
                    # If reporter is victim, add them as involved party
                    if reporter_is_victim and request.user.role == 'student':
                        victim_party = InvolvedParty.objects.create(
                            party_type='student',
                            student=request.user,
                            is_confirmed=True,
                            confirmed_by=request.user,
                            confirmed_at=timezone.now(),
                        )
                        report.involved_parties.add(victim_party)
                except Exception as e:
                    print(f"Error handling involved parties: {e}")
                
                messages.success(request, f'Report {report.case_id} submitted successfully')
                
                # Send notifications
                try:
                    send_smart_notifications(report, 'report_submitted')
                except Exception as e:
                    print(f"Notification error: {e}")
                    # Fallback notification
                    try:
                        do_users = CustomUser.objects.filter(role='do')
                        for do_user in do_users:
                            Notification.objects.create(
                                user=do_user,
                                title='New Incident Report Submitted',
                                message=f'New incident report {report.case_id} filed by {request.user.get_full_name()}.',
                                report=report
                            )
                    except Exception as e2:
                        print(f"Fallback notification error: {e2}")
                
                return redirect('my_reports')
            else:
                # Display form errors
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field.replace('_', ' ').title()}: {error}")
        else:
            form = IncidentReportForm()
            # Pre-fill reporter information
            form.fields['reporter_first_name'].initial = request.user.first_name
            form.fields['reporter_middle_name'].initial = getattr(request.user, 'middle_name', '')
            form.fields['reporter_last_name'].initial = request.user.last_name
        
        # Get context data for the template
        try:
            context = {
                'form': form,
                'incident_types': IncidentType.objects.all().order_by('severity', 'name'),
                'teacher_assignments': TeacherAssignment.objects.all(),
            }
        except Exception as e:
            print(f"Error getting context data: {e}")
            context = {
                'form': form,
                'incident_types': [],
                'teacher_assignments': [],
            }
        
        return render(request, 'report_incident.html', context)
        
    except Exception as e:
        print(f"Major error in report_incident: {e}")
        messages.error(request, 'An error occurred. Please try again.')
        return redirect('dashboard')


@login_required
def my_reports(request):
    """Show reports created by the current user"""
    try:
        reports = IncidentReport.objects.filter(reporter=request.user).order_by('-created_at')
        return render(request, 'my_reports.html', {'reports': reports})
    except Exception as e:
        print(f"Error in my_reports: {e}")
        return render(request, 'my_reports.html', {'reports': []})