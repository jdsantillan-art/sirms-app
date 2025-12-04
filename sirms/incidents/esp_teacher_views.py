# ESP Teacher Management Views
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from django.db import models
from django.utils import timezone
from .models import Counselor, VPFCase, CustomUser, Notification
from .forms import ESPTeacherForm


@login_required
def manage_esp_teachers(request):
    """View to manage ESP teachers (max 5)"""
    if request.user.role != 'counselor':
        messages.error(request, 'Access denied. Only counselors can manage ESP teachers.')
        return redirect('dashboard')
    
    esp_teachers = Counselor.objects.filter(is_active=True).order_by('name')
    esp_count = esp_teachers.count()
    
    context = {
        'esp_teachers': esp_teachers,
        'esp_count': esp_count,
        'max_teachers': 5,
        'can_add_more': esp_count < 5,
    }
    return render(request, 'counselor/manage_esp_teachers.html', context)


@login_required
def add_esp_teacher(request):
    """Add new ESP teacher"""
    if request.user.role != 'counselor':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    # Check if already have 5 teachers
    esp_count = Counselor.objects.filter(is_active=True).count()
    if esp_count >= 5:
        messages.error(request, 'Maximum of 5 ESP teachers reached. Please deactivate one before adding more.')
        return redirect('manage_esp_teachers')
    
    if request.method == 'POST':
        form = ESPTeacherForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'ESP Teacher added successfully!')
            return redirect('manage_esp_teachers')
    else:
        form = ESPTeacherForm()
    
    context = {
        'form': form,
        'action': 'Add',
    }
    return render(request, 'counselor/esp_teacher_form.html', context)


@login_required
def edit_esp_teacher(request, teacher_id):
    """Edit ESP teacher"""
    if request.user.role != 'counselor':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    teacher = get_object_or_404(Counselor, id=teacher_id)
    
    if request.method == 'POST':
        form = ESPTeacherForm(request.POST, instance=teacher)
        if form.is_valid():
            form.save()
            messages.success(request, 'ESP Teacher updated successfully!')
            return redirect('manage_esp_teachers')
    else:
        form = ESPTeacherForm(instance=teacher)
    
    context = {
        'form': form,
        'teacher': teacher,
        'action': 'Edit',
    }
    return render(request, 'counselor/esp_teacher_form.html', context)


@login_required
def delete_esp_teacher(request, teacher_id):
    """Deactivate ESP teacher"""
    if request.user.role != 'counselor':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    teacher = get_object_or_404(Counselor, id=teacher_id)
    
    # Check if teacher has active VPF cases
    active_cases = VPFCase.objects.filter(
        esp_teacher_assigned=teacher,
        status__in=['pending', 'scheduled', 'ongoing']
    ).count()
    
    if active_cases > 0:
        messages.error(request, f'Cannot deactivate. This teacher has {active_cases} active VPF case(s).')
        return redirect('manage_esp_teachers')
    
    teacher.is_active = False
    teacher.save()
    messages.success(request, f'{teacher.name} has been deactivated.')
    return redirect('manage_esp_teachers')


@login_required
def assign_esp_teacher_to_vpf(request, vpf_case_id):
    """Assign ESP teacher to VPF case - sends to ESP Teacher's VPF Cases display"""
    if request.user.role not in ['counselor', 'guidance']:
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    from .models import CustomUser, Notification
    
    vpf_case = get_object_or_404(VPFCase, id=vpf_case_id)
    
    if request.method == 'POST':
        teacher_id = request.POST.get('esp_teacher_id')
        if teacher_id:
            teacher = get_object_or_404(Counselor, id=teacher_id, is_active=True)
            vpf_case.esp_teacher_assigned = teacher
            # Keep status as 'pending' until ESP teacher schedules it
            vpf_case.status = 'pending'
            vpf_case.save()
            
            # Find the ESP Teacher user account that matches this Counselor record
            # Match by email first, then by name
            esp_teacher_user = CustomUser.objects.filter(
                Q(email__iexact=teacher.email) | 
                Q(first_name__icontains=teacher.name.split()[0] if teacher.name else '') |
                Q(last_name__icontains=teacher.name.split()[-1] if teacher.name else '')
            ).filter(role='esp_teacher', is_active=True).first()
            
            # Notify the specific ESP Teacher
            if esp_teacher_user:
                Notification.objects.create(
                    user=esp_teacher_user,
                    title='VPF Case Assigned to You',
                    message=f'Case {vpf_case.report.case_id} for student {vpf_case.student.get_full_name()} has been assigned to you. Please schedule the VPF session.',
                    report=vpf_case.report
                )
            
            # Notify the student
            Notification.objects.create(
                user=vpf_case.student,
                title='VPF Teacher Assigned',
                message=f'Your VPF case ({vpf_case.report.case_id}) has been assigned to {teacher.name}. You will be notified when the session is scheduled.',
                report=vpf_case.report
            )
            
            messages.success(request, f'ESP Teacher {teacher.name} assigned to VPF case successfully! The case will now appear in their VPF Cases display.')
        else:
            messages.error(request, 'Please select an ESP teacher.')
        
        return redirect('for_vpf')
    
    # Get active ESP teachers
    esp_teachers = Counselor.objects.filter(is_active=True).annotate(
        active_cases=Count('vpf_cases_assigned', filter=models.Q(vpf_cases_assigned__status__in=['pending', 'scheduled', 'ongoing']))
    ).order_by('name')
    
    context = {
        'vpf_case': vpf_case,
        'esp_teachers': esp_teachers,
    }
    return render(request, 'counselor/assign_esp_teacher.html', context)



@login_required
def for_vpf_cases(request):
    """View VPF cases that need ESP teacher assignment"""
    if request.user.role not in ['counselor', 'guidance']:
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    # Get all VPF cases
    vpf_cases = VPFCase.objects.select_related(
        'report', 'student', 'assigned_by', 'esp_teacher_assigned'
    ).order_by('-assigned_at')
    
    # Separate into pending and assigned
    pending_vpf = vpf_cases.filter(esp_teacher_assigned__isnull=True)
    assigned_vpf = vpf_cases.filter(esp_teacher_assigned__isnull=False)
    
    context = {
        'pending_vpf': pending_vpf,
        'assigned_vpf': assigned_vpf,
        'total_vpf': vpf_cases.count(),
        'pending_count': pending_vpf.count(),
        'assigned_count': assigned_vpf.count(),
    }
    return render(request, 'counselor/for_vpf.html', context)
