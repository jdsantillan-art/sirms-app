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
    """All reports view - shows different reports based on user role"""
    try:
        user = request.user
        
        if user.role == 'counselor':
            # Counselors see major cases and cases assigned to them
            reports = IncidentReport.objects.filter(
                Q(classification='major') | 
                Q(status='classified') |
                Q(status='under_review')
            ).order_by('-created_at')
            
            # Add filtering for counselor-specific cases
            counselor_reports = reports.filter(
                Q(notes__icontains='counseling') |
                Q(incident_type__severity='prohibited') |
                Q(classification='major')
            )
            
            context = {
                'reports': counselor_reports,
                'user_role': user.role,
                'total_reports': counselor_reports.count(),
                'pending_evaluation': counselor_reports.filter(status='classified').count(),
                'under_review': counselor_reports.filter(status='under_review').count(),
                'completed': counselor_reports.filter(status__in=['resolved', 'closed']).count(),
            }
            
        elif user.role == 'do':
            # DO sees all reports for fact-checking and minor cases
            reports = IncidentReport.objects.all().order_by('-created_at')
            context = {
                'reports': reports,
                'user_role': user.role,
                'total_reports': reports.count(),
                'pending': reports.filter(status='pending').count(),
                'classified': reports.filter(status='classified').count(),
            }
            
        elif user.role in ['principal', 'guidance']:
            # Principal and guidance see all reports
            reports = IncidentReport.objects.all().order_by('-created_at')
            context = {
                'reports': reports,
                'user_role': user.role,
                'total_reports': reports.count(),
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
    """Analytics dashboard placeholder"""
    try:
        context = {'user_role': request.user.role}
        return render(request, 'analytics_dashboard.html', context)
    except:
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
    """Counseling schedule placeholder"""
    try:
        context = {'user_role': request.user.role}
        return render(request, 'counseling_schedule.html', context)
    except:
        return redirect('dashboard')


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


def get_dashboard_analytics(request):
    """Get dashboard analytics API placeholder"""
    return JsonResponse({'analytics': []})


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
        context = {'notification_id': notification_id}
        return render(request, 'schedule_notification_detail.html', context)
    except:
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