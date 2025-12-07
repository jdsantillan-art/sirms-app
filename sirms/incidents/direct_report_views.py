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
    TeacherAssignment, Curriculum, InvolvedParty
)
from .forms import IncidentReportForm
from .notification_utils import send_smart_notifications


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
            try:
                # Create the report manually
                report = IncidentReport()
                report.reporter = request.user  # DO or Counselor is the reporter
                
                # Set reporter information (from the form - the actual reporter's details)
                report.reporter_first_name = form.cleaned_data.get('reporter_first_name', '')
                report.reporter_middle_name = form.cleaned_data.get('reporter_middle_name', '')
                report.reporter_last_name = form.cleaned_data.get('reporter_last_name', '')
                
                # Set academic information
                report.curriculum = form.cleaned_data.get('curriculum')
                report.grade_level = form.cleaned_data.get('grade_level', '')
                report.section_name = form.cleaned_data.get('section_name', '')
                report.teacher_name = form.cleaned_data.get('teacher_name', '')
                
                # Set other fields
                report.involved_students = form.cleaned_data.get('involved_students', '')
                report.student_gender = form.cleaned_data.get('student_gender', '')
                report.incident_date = form.cleaned_data['incident_date']
                report.incident_time = form.cleaned_data['incident_time']
                report.incident_type = form.cleaned_data.get('incident_type')
                
                # Handle bullying type if provided
                bullying_type = request.POST.get('bullying_type', '')
                description = form.cleaned_data.get('description', '')
                if bullying_type:
                    report.description = f"[Bullying Type: {bullying_type}]\n\n{description}"
                else:
                    report.description = description
                
                report.evidence = form.cleaned_data.get('evidence')
                
                # NEW: Handle proper process fields
                report.reporter_is_victim = request.POST.get('reporter_is_victim') == 'on'
                report.is_confidential = request.POST.get('is_confidential') == 'on'
                
                # Save the report first to get an ID
                report.save()
                
                # NEW: Create InvolvedParty record
                party_type = request.POST.get('party_type', 'student')
                
                if party_type == 'teacher':
                    # Teacher incident
                    teacher_name_input = request.POST.get('teacher_name', '')
                    department = request.POST.get('department', '')
                    
                    # Try to find teacher by name
                    teacher_user = None
                    if teacher_name_input:
                        name_parts = teacher_name_input.strip().split()
                        if len(name_parts) >= 2:
                            try:
                                teacher_user = CustomUser.objects.filter(
                                    role='teacher',
                                    first_name__icontains=name_parts[0],
                                    last_name__icontains=name_parts[-1]
                                ).first()
                            except:
                                pass
                    
                    # Create involved party
                    involved_party = InvolvedParty.objects.create(
                        party_type='teacher',
                        teacher=teacher_user,
                        name_if_unknown=teacher_name_input if not teacher_user else '',
                        department=department
                    )
                    
                    # Add to report's involved_parties (ManyToMany)
                    report.involved_parties.add(involved_party)
                    
                    # Mark as confidential for teacher incidents
                    report.is_confidential = True
                    report.save()
                else:
                    # Student incident
                    # Try to find section object
                    section_obj = None
                    if form.cleaned_data.get('section_name') and form.cleaned_data.get('curriculum'):
                        try:
                            # Try to find section by name and grade
                            from .models import Section
                            section_obj = Section.objects.filter(
                                name__iexact=form.cleaned_data['section_name'],
                                grade__level=form.cleaned_data['grade_level']
                            ).first()
                        except:
                            pass
                    
                    # Create involved party
                    involved_party = InvolvedParty.objects.create(
                        party_type='student',
                        student=report.reported_student,  # Will be set later if found
                        name_if_unknown=form.cleaned_data['involved_students'] if not report.reported_student else '',
                        curriculum=form.cleaned_data.get('curriculum'),
                        grade_level=form.cleaned_data.get('grade_level'),
                        section=section_obj
                    )
                    
                    # Add to report's involved_parties (ManyToMany)
                    report.involved_parties.add(involved_party)
                
                # Try to find and assign the reported student from involved_students
                involved_students_text = form.cleaned_data.get('involved_students', '')
                if involved_students_text and party_type == 'student':
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
                            
                            # If not found, try by name
                            if not student:
                                name_parts = identifier.split()
                                if len(name_parts) >= 2:
                                    student = CustomUser.objects.filter(
                                        role='student',
                                        first_name__icontains=name_parts[0],
                                        last_name__icontains=name_parts[-1]
                                    ).first()
                            
                            # If found, assign as reported_student and update involved_party
                            if student:
                                report.reported_student = student
                                # Update the involved_party if it exists
                                if party_type == 'student' and report.involved_parties.exists():
                                    involved_party = report.involved_parties.filter(party_type='student').first()
                                    if involved_party:
                                        involved_party.student = student
                                        involved_party.name_if_unknown = ''
                                        involved_party.save()
                                break
                
                # Set status based on who is creating the report
                if request.user.role == 'do':
                    report.status = 'pending'  # DO will still need to classify
                elif request.user.role == 'counselor':
                    report.status = 'under_review'  # Counselor can start reviewing immediately
                
                report.save()
                
                # NEW: Use smart notification system
                try:
                    send_smart_notifications(report, party_type)
                except Exception as e:
                    # If notification fails, still continue
                    print(f"Notification error: {e}")
                
                # Create confirmation notification for the encoder
                try:
                    Notification.objects.create(
                        user=request.user,
                        title='Direct Report Recorded',
                        message=f'Direct report {report.case_id} has been recorded successfully. Notifications sent to relevant parties.',
                        report=report
                    )
                except Exception as e:
                    print(f"Notification creation error: {e}")
                
                messages.success(request, f'Direct report {report.case_id} recorded successfully')
                return redirect('all_reports')
            except Exception as e:
                # Log the error for debugging
                import traceback
                print(f"Direct report error: {e}")
                print(traceback.format_exc())
                messages.error(request, f'Error creating direct report: {str(e)}')
                # Return to form with errors
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
