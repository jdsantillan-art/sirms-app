"""
Direct Report Views for DO and Guidance Counselors
Allows manual encoding of reports made directly to their offices
"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from datetime import timedelta
from .models import (
    IncidentReport, CustomUser, Notification, IncidentType,
    TeacherAssignment, Curriculum, InvolvedParty, Section
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
                # Prevent duplicate submissions - check if similar report exists in last 5 seconds
                recent_duplicate = IncidentReport.objects.filter(
                    reporter=request.user,
                    incident_date=form.cleaned_data['incident_date'],
                    incident_time=form.cleaned_data['incident_time'],
                    created_at__gte=timezone.now() - timedelta(seconds=5)
                ).first()
                
                if recent_duplicate:
                    messages.info(request, f'Report {recent_duplicate.case_id} was already submitted. Please wait a moment.')
                    return redirect('all_reports')
                
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
                    
                    # Try to find teacher by name (optimized single query)
                    teacher_user = None
                    if teacher_name_input:
                        name_parts = teacher_name_input.strip().split()
                        if len(name_parts) >= 2:
                            try:
                                teacher_user = CustomUser.objects.filter(
                                    role='teacher'
                                ).filter(
                                    Q(first_name__icontains=name_parts[0]) & Q(last_name__icontains=name_parts[-1])
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
                    # Student incident - optimize section lookup
                    section_obj = None
                    section_name = form.cleaned_data.get('section_name')
                    grade_level = form.cleaned_data.get('grade_level')
                    
                    if section_name and grade_level:
                        try:
                            section_obj = Section.objects.filter(
                                name__iexact=section_name,
                                grade__level=grade_level
                            ).select_related('grade').first()
                        except:
                            pass
                    
                    # Create involved party
                    involved_party = InvolvedParty.objects.create(
                        party_type='student',
                        student=report.reported_student,  # Will be set later if found
                        name_if_unknown=form.cleaned_data['involved_students'] if not report.reported_student else '',
                        curriculum=form.cleaned_data.get('curriculum'),
                        grade_level=grade_level,
                        section=section_obj
                    )
                    
                    # Add to report's involved_parties (ManyToMany)
                    report.involved_parties.add(involved_party)
                
                # Optimized student search - single query using Q objects
                involved_students_text = form.cleaned_data.get('involved_students', '')
                if involved_students_text and party_type == 'student':
                    import re
                    potential_identifiers = re.split(r'[,;\n]+', involved_students_text)
                    
                    for identifier in potential_identifiers:
                        identifier = identifier.strip()
                        if not identifier:
                            continue
                        
                        # Optimized: Single query with Q objects instead of multiple queries
                        name_parts = identifier.split()
                        if len(name_parts) >= 2:
                            # Try all methods in one query
                            student = CustomUser.objects.filter(
                                role='student'
                            ).filter(
                                Q(email__iexact=identifier) |
                                Q(username__iexact=identifier) |
                                (Q(first_name__icontains=name_parts[0]) & Q(last_name__icontains=name_parts[-1]))
                            ).first()
                        else:
                            # Single identifier - try email or username only
                            student = CustomUser.objects.filter(
                                role='student'
                            ).filter(
                                Q(email__iexact=identifier) | Q(username__iexact=identifier)
                            ).first()
                        
                        # If found, assign as reported_student and update involved_party
                        if student:
                            report.reported_student = student
                            # Update the involved_party if it exists
                            if report.involved_parties.exists():
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
                
                # Send notifications asynchronously (non-blocking) - don't wait for completion
                # This speeds up the response significantly
                try:
                    # Create confirmation notification for the encoder first (fast)
                    Notification.objects.create(
                        user=request.user,
                        title='Direct Report Recorded',
                        message=f'Direct report {report.case_id} has been recorded successfully.',
                        report=report
                    )
                except Exception as e:
                    print(f"Confirmation notification error: {e}")
                
                # Send other notifications in background (non-blocking)
                # Wrap in try-except so it doesn't slow down the response
                try:
                    send_smart_notifications(report, party_type)
                except Exception as e:
                    # Log but don't fail the request
                    print(f"Notification error (non-blocking): {e}")
                
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
    
    # Get context data for the template (optimized queries)
    context = {
        'form': form,
        'incident_types': IncidentType.objects.all().order_by('severity', 'name')[:100],  # Limit to prevent slow loading
        'teacher_assignments': TeacherAssignment.objects.select_related('curriculum').all(),  # All teacher assignments for dropdowns
        'is_direct_report': True,  # Flag to indicate this is a direct report
    }
    
    return render(request, 'direct_report.html', context)
