"""
Direct Report Views for DO and Guidance Counselors
Allows manual encoding of reports made directly to their offices
"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import (
    IncidentReport, CustomUser, Notification, IncidentType,
    TeacherAssignment, Curriculum
)
from .forms import IncidentReportForm


@login_required
def direct_report(request):
    """
    Direct Report feature for DO and Guidance Counselors
    Allows them to manually encode reports made directly to their offices
    """
    # Only DO and Counselors can access this
    if request.user.role not in ['do', 'counselor']:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = IncidentReportForm(request.POST, request.FILES)
        if form.is_valid():
            # Create the report manually
            report = IncidentReport()
            report.reporter = request.user  # DO or Counselor is the reporter
            
            # Set reporter information (from the form - the actual reporter's details)
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
            description = form.cleaned_data['description']
            if bullying_type:
                report.description = f"[Bullying Type: {bullying_type}]\n\n{description}"
            else:
                report.description = description
            
            report.evidence = form.cleaned_data['evidence']
            
            # Try to find and assign the reported student from involved_students
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
                        
                        # If found, assign as reported_student
                        if student:
                            report.reported_student = student
                            break
            
            # Set status based on who is creating the report
            if request.user.role == 'do':
                report.status = 'pending'  # DO will still need to classify
            elif request.user.role == 'counselor':
                report.status = 'under_review'  # Counselor can start reviewing immediately
            
            report.save()
            
            # Create notifications based on who created the report
            if request.user.role == 'do':
                # Notify the DO themselves (confirmation)
                Notification.objects.create(
                    user=request.user,
                    title='Direct Report Recorded',
                    message=f'Direct report {report.case_id} has been recorded. You can now proceed with fact-checking and classification.',
                    report=report
                )
            elif request.user.role == 'counselor':
                # Notify all DOs about the direct report from counselor
                do_users = CustomUser.objects.filter(role='do')
                for do_user in do_users:
                    Notification.objects.create(
                        user=do_user,
                        title='Direct Report from Guidance',
                        message=f'Guidance Counselor {request.user.get_full_name()} recorded direct report {report.case_id}.',
                        report=report
                    )
                
                # Notify the counselor themselves (confirmation)
                Notification.objects.create(
                    user=request.user,
                    title='Direct Report Recorded',
                    message=f'Direct report {report.case_id} has been recorded and is under review.',
                    report=report
                )
            
            # Notify the reported student if assigned
            if report.reported_student:
                Notification.objects.create(
                    user=report.reported_student,
                    title='Incident Report Filed',
                    message=f'An incident report {report.case_id} has been filed regarding you. Please check your dashboard for details.',
                    report=report
                )
            
            messages.success(request, f'Direct report {report.case_id} recorded successfully')
            return redirect('all_reports')
        else:
            # Display form errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.replace('_', ' ').title()}: {error}")
    else:
        form = IncidentReportForm()
        # Pre-fill reporter information with current user's info (can be changed)
        form.fields['reporter_first_name'].initial = ''
        form.fields['reporter_last_name'].initial = ''
    
    # Get context data for the template
    context = {
        'form': form,
        'incident_types': IncidentType.objects.all().order_by('severity', 'name'),
        'teacher_assignments': TeacherAssignment.objects.all(),
        'is_direct_report': True,  # Flag to indicate this is a direct report
    }
    
    return render(request, 'direct_report.html', context)
