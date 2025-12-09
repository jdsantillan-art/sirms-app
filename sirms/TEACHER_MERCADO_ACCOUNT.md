# Teacher Account: Ms. Stephanie Mercado

## Account Details

**Name:** Ms. Stephanie Mercado  
**Username:** `stephanie.mercado`  
**Password:** `Teacher2024!`  
**Email:** stephanie.mercado@school.edu  
**Employee ID:** TCH-2024-008  
**Department:** Junior High School  

## Assignment

- **Grade Level:** Grade 8
- **Section:** Section 2
- **Subject:** ICT (Information and Communications Technology)
- **Role:** Class Adviser
- **School Year:** 2024-2025

## Dashboard Features

When Ms. Mercado logs in, she will see:

1. **Student Reports Dashboard** - Same as student view but shows:
   - All incident reports from her Grade 8 Section 2 students
   - Report status (Pending, Under Review, Resolved, etc.)
   - Involved parties and incident details
   - Timeline of updates

2. **Notification System** - She receives notifications for:
   - ✓ New incident reports from her students
   - ✓ Guidance Counselor updates and evaluations
   - ✓ DO (Discipline Officer) schedule assignments
   - ✓ ESP Teacher assignments and updates
   - ✓ Case status changes
   - ✓ Counseling session schedules

3. **Email Notifications** - Enabled by default:
   - Automatic email alerts for all updates
   - Real-time notification of student incidents
   - Updates from all departments (Guidance, DO, ESP)

## How to Create This Account

### Option 1: Using Django Shell
```bash
cd sirms
python manage.py shell
```

Then run:
```python
from django.contrib.auth.models import User
from incidents.models import Teacher, TeacherAssignment

# Create user
user, created = User.objects.get_or_create(
    username='stephanie.mercado',
    defaults={
        'email': 'stephanie.mercado@school.edu',
        'first_name': 'Stephanie',
        'last_name': 'Mercado'
    }
)
user.set_password('Teacher2024!')
user.save()

# Create teacher profile
teacher, _ = Teacher.objects.get_or_create(
    user=user,
    defaults={
        'employee_id': 'TCH-2024-008',
        'department': 'Junior High School',
        'contact_number': '09XX-XXX-XXXX',
        'email_notifications_enabled': True
    }
)
teacher.email_notifications_enabled = True
teacher.save()

# Create assignment
assignment, _ = TeacherAssignment.objects.get_or_create(
    teacher=teacher,
    grade_level='Grade 8',
    section='Section 2',
    defaults={
        'subject': 'ICT',
        'is_adviser': True,
        'school_year': '2024-2025'
    }
)
assignment.is_adviser = True
assignment.subject = 'ICT'
assignment.save()

print("✓ Account created successfully!")
```

### Option 2: Using Batch File
```bash
cd sirms
create_teacher_mercado.bat
```

### Option 3: Using Django Admin Panel
1. Login to Django admin: `/admin`
2. Go to Users → Add User
3. Create username: `stephanie.mercado`, password: `Teacher2024!`
4. Go to Teachers → Add Teacher
5. Link to the user, set employee_id: `TCH-2024-008`
6. Enable email notifications
7. Go to Teacher Assignments → Add Assignment
8. Link to teacher, set Grade 8, Section 2, ICT, is_adviser=True

## Login Instructions

1. Go to SIRMS login page
2. Enter username: **stephanie.mercado**
3. Enter password: **Teacher2024!**
4. Click Login

## What Ms. Mercado Will See

### Dashboard View
- **My Students' Reports** - All incidents reported by or involving Grade 8 Section 2 students
- **Pending Cases** - Reports awaiting action
- **Active Cases** - Currently being processed
- **Resolved Cases** - Completed incidents

### Notification Features
- Bell icon with notification count
- Real-time updates when:
  - Student submits a report
  - Guidance evaluates the case
  - DO schedules counseling
  - ESP Teacher is assigned
  - Case status changes

### Report Details
When clicking on a report, she can see:
- Student information (reporter and involved parties)
- Incident details and evidence
- Current status and assigned personnel
- Timeline of all actions taken
- Comments from Guidance, DO, and ESP Teacher
- Scheduled counseling sessions

## Notification Flow Example

**When a student reports an incident:**

1. **Student** (Grade 8 Section 2) submits incident report
2. **Ms. Mercado** receives notification: "New incident report from [Student Name]"
3. **Guidance Counselor** reviews → Ms. Mercado notified: "Case under review by Guidance"
4. **DO** schedules session → Ms. Mercado notified: "Counseling session scheduled for [Date/Time]"
5. **ESP Teacher** assigned → Ms. Mercado notified: "ESP Teacher assigned to case"
6. **Case resolved** → Ms. Mercado notified: "Case marked as resolved"

## Important Notes

- Email notifications are **ENABLED by default**
- Ms. Mercado can only view reports from **her assigned class** (Grade 8 Section 2)
- She has **read-only access** to reports (cannot modify or resolve)
- She can **add comments** to provide context or updates
- Dashboard updates in **real-time** when new actions occur

## Testing the Account

After creation, test by:
1. Login with the credentials
2. Check dashboard loads correctly
3. Have a Grade 8 Section 2 student submit a test report
4. Verify Ms. Mercado receives notification
5. Check email notification is sent
6. Verify she can view report details

## Security

- Password should be changed on first login
- Email should be updated to actual school email
- Contact number should be updated with real number
- Account has teacher-level permissions only
