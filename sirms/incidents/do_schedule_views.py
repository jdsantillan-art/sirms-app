"""
DO Schedule Views - Parent Conferences and Interviews
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import DOSchedule, IncidentReport, CustomUser, Notification, TeacherAssignment, Section
from .forms import DOScheduleForm


def notify_adviser_of_do_schedule(report, scheduled_date, location, do_name, schedule_type):
    """
    Notify the adviser/teacher of a student when DO schedule is created.
    Finds the teacher based on curriculum, grade, and section from the report.
    """
    if not report:
        return
    
    # Try to find the teacher/adviser based on the report's academic details
    teachers_to_notify = []
    
    # Method 1: Find by teacher_name field in the report
    if report.teacher_name:
        # Try to find teacher by name
        teacher_users = CustomUser.objects.filter(
            role='teacher',
            first_name__icontains=report.teacher_name.split()[0] if report.teacher_name.split() else report.teacher_name
        )
        if teacher_users.exists():
            teachers_to_notify.extend(teacher_users)
    
    # Method 2: Find by Section adviser (if section is linked)
    if report.section and report.section.adviser:
        if report.section.adviser not in teachers_to_notify:
            teachers_to_notify.append(report.section.adviser)
    
    # Method 3: Find by TeacherAssignment matching curriculum, grade, section
    if report.curriculum and report.grade_level and report.section_name:
        teacher_assignments = TeacherAssignment.objects.filter(
            curriculum=report.curriculum,
            grade_level=report.grade_level,
            section_name__iexact=report.section_name
        )
        
        for assignment in teacher_assignments:
            # Try to find the teacher user by name
            teacher_name_parts = assignment.teacher_name.split()
            if teacher_name_parts:
                matching_teachers = CustomUser.objects.filter(
                    role='teacher',
                    first_name__icontains=teacher_name_parts[0]
                )
                if len(teacher_name_parts) > 1:
                    matching_teachers = matching_teachers.filter(
                        last_name__icontains=teacher_name_parts[-1]
                    )
                
                for teacher in matching_teachers:
                    if teacher not in teachers_to_notify:
                        teachers_to_notify.append(teacher)
    
    # Send notifications to all found teachers
    student_name = report.reported_student.get_full_name() if report.reported_student else report.involved_students
    
    for teacher in teachers_to_notify:
        Notification.objects.create(
            user=teacher,
            title=f'{schedule_type} Scheduled for Your Student',
            message=f'A {schedule_type.lower()} has been scheduled for your student {student_name} (Case: {report.case_id}) on {scheduled_date.strftime("%B %d, %Y at %I:%M %p")}. Location: {location if location else "TBA"}. Discipline Officer: {do_name}.',
            report=report
        )


@login_required
def do_schedule(request):
    """View and manage DO schedules (parent conferences, interviews)"""
    # Only DOs can access this
    if request.user.role != 'do':
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('dashboard')
    
    # Get all schedules for this DO
    schedules = DOSchedule.objects.filter(
        discipline_officer=request.user
    ).select_related('student', 'report').order_by('scheduled_date')
    
    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter:
        schedules = schedules.filter(status=status_filter)
    
    # Separate upcoming and past schedules
    now = timezone.now()
    upcoming_schedules = schedules.filter(scheduled_date__gte=now, status='scheduled')
    past_schedules = schedules.filter(scheduled_date__lt=now).exclude(status='scheduled')
    
    # Statistics
    total_schedules = schedules.count()
    scheduled_count = schedules.filter(status='scheduled').count()
    completed_count = schedules.filter(status='completed').count()
    cancelled_count = schedules.filter(status='cancelled').count()
    
    context = {
        'schedules': schedules,
        'upcoming_schedules': upcoming_schedules,
        'past_schedules': past_schedules,
        'total_schedules': total_schedules,
        'scheduled_count': scheduled_count,
        'completed_count': completed_count,
        'cancelled_count': cancelled_count,
    }
    
    return render(request, 'do/do_schedule.html', context)


@login_required
def create_do_schedule(request):
    """Create a new DO schedule"""
    # Only DOs can access this
    if request.user.role != 'do':
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = DOScheduleForm(request.POST)
        if form.is_valid():
            schedule = form.save(commit=False)
            schedule.discipline_officer = request.user
            schedule.save()
            
            # Create notification for the student if assigned
            if schedule.student:
                Notification.objects.create(
                    user=schedule.student,
                    title=f'{schedule.get_schedule_type_display()} Scheduled',
                    message=f'A {schedule.get_schedule_type_display().lower()} has been scheduled for {schedule.scheduled_date.strftime("%B %d, %Y at %I:%M %p")}. Location: {schedule.location}',
                )
            
            # Notify the DO (confirmation)
            Notification.objects.create(
                user=request.user,
                title='Schedule Created',
                message=f'{schedule.get_schedule_type_display()} scheduled for {schedule.scheduled_date.strftime("%B %d, %Y at %I:%M %p")}.',
            )
            
            # Notify the adviser/teacher if report is linked
            if schedule.report:
                notify_adviser_of_do_schedule(
                    report=schedule.report,
                    scheduled_date=schedule.scheduled_date,
                    location=schedule.location,
                    do_name=request.user.get_full_name(),
                    schedule_type=schedule.get_schedule_type_display()
                )
            
            messages.success(request, f'{schedule.get_schedule_type_display()} scheduled successfully!')
            return redirect('do_schedule')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.replace('_', ' ').title()}: {error}")
    else:
        form = DOScheduleForm()
        # Pre-fill with case ID if provided
        case_id = request.GET.get('case_id')
        if case_id:
            try:
                report = IncidentReport.objects.get(case_id=case_id)
                form.initial['purpose'] = f'Regarding incident report {case_id}'
                if report.reported_student:
                    form.fields['student_email'].initial = report.reported_student.email
            except IncidentReport.DoesNotExist:
                pass
    
    context = {
        'form': form,
    }
    
    return render(request, 'do/create_do_schedule.html', context)


@login_required
def update_do_schedule_status(request, schedule_id):
    """Update the status of a DO schedule"""
    # Only DOs can access this
    if request.user.role != 'do':
        messages.error(request, 'You do not have permission to perform this action.')
        return redirect('dashboard')
    
    schedule = get_object_or_404(DOSchedule, id=schedule_id, discipline_officer=request.user)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        notes = request.POST.get('notes', '')
        
        if new_status in dict(DOSchedule.STATUS_CHOICES):
            old_status = schedule.status
            schedule.status = new_status
            if notes:
                schedule.notes = notes
            schedule.save()
            
            # Notify student if status changed
            if schedule.student and old_status != new_status:
                Notification.objects.create(
                    user=schedule.student,
                    title=f'Schedule Status Updated',
                    message=f'Your {schedule.get_schedule_type_display().lower()} scheduled for {schedule.scheduled_date.strftime("%B %d, %Y")} has been marked as {schedule.get_status_display()}.',
                )
            
            messages.success(request, f'Schedule status updated to {schedule.get_status_display()}')
        else:
            messages.error(request, 'Invalid status')
    
    return redirect('do_schedule')


@login_required
def delete_do_schedule(request, schedule_id):
    """Delete a DO schedule"""
    # Only DOs can access this
    if request.user.role != 'do':
        messages.error(request, 'You do not have permission to perform this action.')
        return redirect('dashboard')
    
    schedule = get_object_or_404(DOSchedule, id=schedule_id, discipline_officer=request.user)
    
    if request.method == 'POST':
        # Notify student if assigned
        if schedule.student:
            Notification.objects.create(
                user=schedule.student,
                title='Schedule Cancelled',
                message=f'The {schedule.get_schedule_type_display().lower()} scheduled for {schedule.scheduled_date.strftime("%B %d, %Y at %I:%M %p")} has been cancelled.',
            )
        
        schedule.delete()
        messages.success(request, 'Schedule deleted successfully')
    
    return redirect('do_schedule')
