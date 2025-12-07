"""
Behavior Concerns Views - DO handles minor cases
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import datetime
from .models import IncidentReport, DOSchedule, Notification, CustomUser, TeacherAssignment


def notify_adviser_of_schedule(report, scheduled_date, location, appointment_type):
    """Notify adviser when DO schedules an appointment"""
    if not report or not report.reported_student:
        return
    
    # Find adviser
    if report.reported_student.section:
        adviser_assignments = TeacherAssignment.objects.filter(
            section_name=report.reported_student.section
        )
        
        for assignment in adviser_assignments:
            if assignment.teacher:
                Notification.objects.create(
                    user=assignment.teacher,
                    title=f'DO Appointment Scheduled - {report.case_id}',
                    message=f'A {appointment_type} has been scheduled for your advisee {report.reported_student.get_full_name()} on {scheduled_date.strftime("%B %d, %Y at %I:%M %p")}. Location: {location or "TBA"}',
                    report=report
                )


@login_required
def behavior_concerns(request):
    """View and manage behavior concerns (cases handled by DO)"""
    # Only DOs can access
    if request.user.role != 'do':
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('dashboard')
    
    # Handle POST requests (update status or schedule appointment)
    if request.method == 'POST':
        action = request.POST.get('action')
        report_id = request.POST.get('report_id')
        
        if not report_id:
            messages.error(request, 'Report ID is required.')
            return redirect('behavior_concerns')
        
        try:
            report = IncidentReport.objects.get(id=report_id)
        except IncidentReport.DoesNotExist:
            messages.error(request, 'Report not found.')
            return redirect('behavior_concerns')
        
        # Handle status update
        if action == 'update_status':
            new_status = request.POST.get('status')
            if new_status in ['classified', 'under_review', 'resolved']:
                old_status = report.status
                report.status = new_status
                report.save()
                
                # Create notification for student
                if report.reported_student:
                    status_messages = {
                        'classified': 'Your case is pending review by the Discipline Office.',
                        'under_review': 'Your case is currently being handled by the Discipline Office.',
                        'resolved': 'Your case has been completed and resolved.'
                    }
                    Notification.objects.create(
                        user=report.reported_student,
                        title=f'Case Status Updated - {report.case_id}',
                        message=status_messages.get(new_status, 'Your case status has been updated.'),
                        report=report
                    )
                
                # Notify adviser
                if report.reported_student and report.reported_student.section:
                    adviser_assignments = TeacherAssignment.objects.filter(
                        section_name=report.reported_student.section
                    )
                    
                    for assignment in adviser_assignments:
                        if assignment.teacher:
                            Notification.objects.create(
                                user=assignment.teacher,
                                title=f'Student Case Update - {report.case_id}',
                                message=f'Your advisee {report.reported_student.get_full_name()} has a case status update to: {report.get_status_display()}',
                                report=report
                            )
                
                messages.success(request, f'Case status updated to {report.get_status_display()}')
            else:
                messages.error(request, 'Invalid status.')
        
        # Handle schedule appointment
        elif action == 'schedule_appointment':
            student_id = request.POST.get('student_id')
            appointment_type = request.POST.get('appointment_type')
            scheduled_date_str = request.POST.get('scheduled_date')
            location = request.POST.get('location', '')
            notes = request.POST.get('notes', '')
            
            if not all([student_id, appointment_type, scheduled_date_str]):
                messages.error(request, 'All required fields must be filled.')
                return redirect('behavior_concerns')
            
            try:
                student = CustomUser.objects.get(id=student_id)
                scheduled_date = datetime.fromisoformat(scheduled_date_str)
                
                # Map appointment type to schedule_type choices
                type_mapping = {
                    'Intake Interview': 'interview',
                    'Investigation Meeting': 'interview',
                    'Parent Conference': 'parent_conference',
                    'Follow-up Meeting': 'follow_up',
                }
                schedule_type_value = type_mapping.get(appointment_type, 'parent_conference')
                
                # Create DO Schedule
                schedule = DOSchedule.objects.create(
                    report=report,
                    discipline_officer=request.user,
                    student=student,
                    schedule_type=schedule_type_value,
                    scheduled_date=scheduled_date,
                    location=location or 'Discipline Office',
                    purpose=f'{appointment_type} for case {report.case_id}',
                    notes=notes,
                    attendees='',
                    status='scheduled'
                )
                
                # AUTO-SYNC: Update Behavioral Concern status to 'under_review' (Scheduled)
                report.status = 'under_review'
                report.save()
                
                # Notify student
                Notification.objects.create(
                    user=student,
                    title=f'{appointment_type} Scheduled',
                    message=f'You have a {appointment_type.lower()} scheduled on {scheduled_date.strftime("%B %d, %Y at %I:%M %p")}. Location: {location or "DO Office"}. Please be on time.',
                    report=report,
                    notification_type='counseling_scheduled'
                )
                
                # Notify reporter about the schedule
                if report.reporter:
                    Notification.objects.create(
                        user=report.reporter,
                        title='Behavioral Concern Scheduled',
                        message=f'The behavioral concern (Case: {report.case_id}) has been scheduled. A {appointment_type.lower()} will be held on {scheduled_date.strftime("%B %d, %Y at %I:%M %p")}.',
                        report=report,
                        notification_type='counseling_scheduled'
                    )
                
                # Notify adviser
                notify_adviser_of_schedule(report, scheduled_date, location or 'DO Office', appointment_type)
                
                messages.success(request, f'{appointment_type} scheduled successfully! Status updated to Scheduled. Student, reporter, and adviser have been notified.')
            
            except CustomUser.DoesNotExist:
                messages.error(request, 'Student not found.')
            except ValueError:
                messages.error(request, 'Invalid date format.')
            except Exception as e:
                messages.error(request, f'Error creating schedule: {str(e)}')
        
        return redirect('behavior_concerns')
    
    # GET request - display cases
    # Get cases classified as minor (handled by DO)
    from .models import Classification
    
    reports = IncidentReport.objects.filter(
        status__in=['classified', 'under_review', 'resolved'],
        classification__severity='minor'  # Only minor cases (DO handles)
    ).select_related(
        'reported_student', 'reporter', 'incident_type', 'classification'
    ).prefetch_related('classification').order_by('-created_at')
    
    # Filter only cases that are classified as minor (handled by DO)
    
    # Statistics
    total_cases = reports.count()
    pending_cases = reports.filter(status='classified').count()
    completed_cases = reports.filter(status='resolved').count()
    
    context = {
        'reports': reports,
        'total_cases': total_cases,
        'pending_cases': pending_cases,
        'completed_cases': completed_cases,
    }
    
    return render(request, 'do/behavior_concerns.html', context)
