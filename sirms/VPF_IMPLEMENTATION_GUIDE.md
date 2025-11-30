# VPF (Values Reflective Formation) Implementation Guide

## ✅ Completed Changes:

### 1. **Evaluation Modal Updated**
- Changed "Recommendation" to "Commission Level" dropdown
- Added cascading dropdowns:
  - **1st Commission**: Parent Conference with Adviser/Subject Teacher, Counseling/Follow-up
  - **2nd Commission**: Parent Conference, Counseling/Follow-up, VPF
  - **3rd Commission**: Parent Conference, Counseling/Follow-up, VPF
- JavaScript handles dynamic intervention options

### 2. **Models Added**
- Added `esp_teacher` role to CustomUser
- Created `VPFCase` model to track VPF assignments
- Created `VPFSchedule` model for ESP teacher to manage schedules

## 🔧 Remaining Implementation Steps:

### 3. **Update case_evaluation view** (incidents/views.py)
```python
@login_required
def case_evaluation(request):
    if request.method == 'POST':
        report_id = request.POST.get('report_id')
        commission = request.POST.get('commission')
        intervention = request.POST.get('intervention')
        verdict = request.POST.get('verdict')
        is_repeat = request.POST.get('is_repeat_offender') == 'on'
        
        # Create evaluation
        report = IncidentReport.objects.get(id=report_id)
        evaluation = CaseEvaluation.objects.create(
            report=report,
            evaluated_by=request.user,
            recommendation=intervention,
            verdict=verdict,
            is_repeat_offender=is_repeat
        )
        
        # If VPF selected, create VPF case
        if 'VPF' in intervention:
            VPFCase.objects.create(
                report=report,
                student=report.reported_student,
                assigned_by=request.user,
                commission_level=commission,
                intervention=intervention,
                status='pending'
            )
            
            # Notify ESP teachers
            esp_teachers = CustomUser.objects.filter(role='esp_teacher')
            for esp in esp_teachers:
                Notification.objects.create(
                    user=esp,
                    title='New VPF Case Assigned',
                    message=f'Case {report.case_id} requires VPF scheduling',
                    report=report
                )
        
        messages.success(request, 'Evaluation submitted successfully')
        return redirect('case_evaluation')
```

### 4. **Create ESP Teacher Interface**

#### A. Add ESP sidebar in base.html:
```html
{% elif user.role == 'esp_teacher' %}
<a href="{% url 'vpf_cases' %}" class="nav-item">
    <i class="fas fa-users"></i>
    <span class="sidebar-text">VPF Cases</span>
</a>
<a href="{% url 'vpf_schedule' %}" class="nav-item">
    <i class="fas fa-calendar-alt"></i>
    <span class="sidebar-text">VPF Schedule</span>
</a>
```

#### B. Create VPF Cases view (templates/esp/vpf_cases.html):
- List all VPF cases
- Show student details and status
- Filter by status (pending, scheduled, ongoing, completed)

#### C. Create VPF Schedule view (templates/esp/vpf_schedule.html):
- Calendar/list view of schedules
- Form to create new schedule
- Assign counselor from Counselor model
- Set date/time and location
- Send notification to student

### 5. **Update "For VPF" in Guidance Sidebar**
The "For VPF" link (formerly Case History) should show:
- All cases with VPF intervention selected
- Current status of each VPF case
- Link to view details

### 6. **Database Migration**
Run these commands:
```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. **Create ESP Teacher Account**
```python
python manage.py shell
from incidents.models import CustomUser
esp = CustomUser.objects.create_user(
    username='esp_teacher',
    password='password123',
    first_name='ESP',
    last_name='Teacher',
    role='esp_teacher',
    email='esp@school.edu'
)
```

## 📋 Workflow Summary:

1. **Counselor evaluates case** → Selects Commission + Intervention
2. **If VPF selected** → Creates VPFCase record
3. **ESP Teacher notified** → Sees case in "VPF Cases"
4. **ESP schedules VPF session** → Assigns counselor, sets date/time
5. **Student notified** → Receives notification to attend VPF
6. **VPF session conducted** → ESP marks as completed
7. **Case tracked** → Visible in "For VPF" for counselors

## 🎯 Key Features:

- ✅ Cascading dropdowns for Commission/Intervention
- ✅ Automatic VPF case creation
- ✅ ESP Teacher role and interface
- ✅ VPF scheduling system
- ✅ Automatic notifications
- ✅ Status tracking
- ✅ Counselor assignment for VPF

## 📝 Notes:

- VPF = Values Reflective Formation
- ESP Teacher manages VPF counselors and schedules
- Students receive notifications for VPF attendance
- All VPF cases tracked separately from regular counseling
