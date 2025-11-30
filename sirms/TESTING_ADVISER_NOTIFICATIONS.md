# Testing Adviser Notification Feature

## Quick Test Guide

### Prerequisites
1. Have at least one teacher account registered
2. Have at least one incident report with:
   - Student assigned
   - Teacher name filled in
   - Curriculum, grade level, and section specified

### Test Scenario 1: Guidance Counselor Creates Counseling Schedule

1. **Login as Guidance Counselor**
   - Username: (your counselor account)
   
2. **Navigate to Counseling Schedule**
   - Go to Dashboard → Counseling Schedule
   - Or directly: `/counselor-schedule/`

3. **Create a Schedule**
   - Select an evaluation that needs scheduling
   - Choose date and time
   - Enter location
   - Submit

4. **Verify Notifications**
   - Login as the teacher/adviser of that student
   - Check notifications (bell icon)
   - Should see: "Counseling Session Scheduled for Your Student"
   - Message should include: student name, case ID, date/time, location

### Test Scenario 2: ESP Teacher Creates VPF Schedule

1. **Login as ESP Teacher**
   - Username: (your ESP teacher account)

2. **Navigate to VPF Schedule**
   - Go to Dashboard → VPF Schedule
   - Or directly: `/vpf-schedule/`

3. **Create a VPF Schedule**
   - Select a pending VPF case
   - Choose date and time
   - Enter location
   - Submit

4. **Verify Notifications**
   - Login as the teacher/adviser of that student
   - Check notifications
   - Should see: "VPF Session Scheduled for Your Student"

### Test Scenario 3: Discipline Officer Creates DO Schedule

1. **Login as Discipline Officer**
   - Username: (your DO account)

2. **Navigate to DO Schedule**
   - Go to Dashboard → DO Schedule
   - Or directly: `/do-schedule/create/`

3. **Create a Schedule**
   - Select schedule type (Parent Conference, Interview, etc.)
   - Link to a case (optional but needed for teacher notification)
   - Choose student
   - Set date/time and location
   - Submit

4. **Verify Notifications**
   - Login as the teacher/adviser of that student
   - Check notifications
   - Should see: "[Schedule Type] Scheduled for Your Student"

## Using the Test Script

Run the test script to check recent notifications:

```bash
cd sirms
python manage.py shell < test_adviser_notifications.py
```

This will show:
- Total teachers in the system
- Recent notifications sent to teachers
- Recent counseling/VPF/DO schedules created
- Teacher information from reports

## Expected Results

### For Teachers
When a counseling session is scheduled for their student, teachers should receive:

**Notification Title**: 
- "Counseling Session Scheduled for Your Student" (Guidance)
- "VPF Session Scheduled for Your Student" (ESP Teacher)
- "[Type] Scheduled for Your Student" (DO)

**Notification Message** includes:
- Student name
- Case ID
- Date and time
- Location
- Who scheduled it (counselor/ESP teacher/DO name)

### Notification Visibility
- Appears in notification bell icon (top right)
- Shows unread count badge
- Can be marked as read
- Links to the related case report

## Troubleshooting

### Teacher Not Receiving Notifications

**Check 1: Teacher Information in Report**
```python
# In Django shell
from incidents.models import IncidentReport
report = IncidentReport.objects.get(case_id='2024-XXXX')
print(f"Teacher Name: {report.teacher_name}")
print(f"Grade: {report.grade_level}")
print(f"Section: {report.section_name}")
print(f"Curriculum: {report.curriculum}")
```

**Check 2: Teacher Account Exists**
```python
from incidents.models import CustomUser
teachers = CustomUser.objects.filter(role='teacher')
for t in teachers:
    print(f"{t.get_full_name()} - {t.username}")
```

**Check 3: Teacher Assignment Records**
```python
from incidents.models import TeacherAssignment
assignments = TeacherAssignment.objects.all()
for a in assignments:
    print(f"{a.teacher_name} - Grade {a.grade_level} {a.section_name}")
```

**Check 4: Section Adviser**
```python
from incidents.models import Section
sections = Section.objects.all()
for s in sections:
    print(f"{s} - Adviser: {s.adviser}")
```

### Common Issues

1. **Teacher name doesn't match**: 
   - Report has "Juan Dela Cruz" but teacher account is "Juan D. Cruz"
   - Solution: System uses first name matching, should still work

2. **No teacher assigned to section**:
   - Section exists but no adviser assigned
   - Solution: Assign adviser in admin panel or use TeacherAssignment

3. **Teacher account not created**:
   - Teacher name in report but no user account
   - Solution: Create teacher account with matching name

## Manual Verification

### Check Notifications Table
```python
from incidents.models import Notification
from django.utils import timezone

# Get recent teacher notifications
recent = timezone.now() - timezone.timedelta(hours=24)
notifs = Notification.objects.filter(
    user__role='teacher',
    created_at__gte=recent
)

for n in notifs:
    print(f"\nTeacher: {n.user.get_full_name()}")
    print(f"Title: {n.title}")
    print(f"Message: {n.message}")
    print(f"Time: {n.created_at}")
```

### Check Schedule Creation
```python
from incidents.models import CounselingSchedule, VPFSchedule, DOSchedule
from django.utils import timezone

recent = timezone.now() - timezone.timedelta(hours=24)

# Counseling schedules
cs = CounselingSchedule.objects.filter(created_at__gte=recent)
print(f"Recent Counseling Schedules: {cs.count()}")

# VPF schedules
vs = VPFSchedule.objects.filter(created_at__gte=recent)
print(f"Recent VPF Schedules: {vs.count()}")

# DO schedules
ds = DOSchedule.objects.filter(created_at__gte=recent)
print(f"Recent DO Schedules: {ds.count()}")
```

## Success Criteria

✅ Teacher receives notification when counseling is scheduled
✅ Notification includes all relevant details
✅ Notification appears in teacher's dashboard
✅ Multiple teachers can be notified if multiple matches found
✅ System works for Guidance, ESP Teacher, and DO schedules
✅ No errors if teacher not found (graceful handling)

## Next Steps

After successful testing:
1. Train staff on the new feature
2. Ensure all reports have accurate teacher information
3. Keep TeacherAssignment records up to date
4. Monitor notification delivery
5. Gather feedback from teachers
