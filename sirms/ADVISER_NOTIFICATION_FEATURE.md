# Adviser/Teacher Automatic Notification Feature

## Overview
When Guidance Counselors, Discipline Officers (DO), or ESP Teachers schedule counseling sessions, the system now automatically notifies the student's adviser/teacher based on the student's curriculum, grade level, and section.

## How It Works

### Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│  Guidance/DO/ESP Teacher Creates Counseling Schedule        │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  Extract Student Info from Report:                          │
│  - Curriculum (e.g., K-12)                                  │
│  - Grade Level (e.g., 10)                                   │
│  - Section Name (e.g., "Section A")                         │
│  - Teacher Name (e.g., "Maria Santos")                      │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  Search for Matching Teachers (3 Methods):                  │
│  1. Match by teacher_name field                             │
│  2. Match by Section.adviser                                │
│  3. Match by TeacherAssignment (curriculum+grade+section)   │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  Create Notifications for All Matching Teachers             │
│  - Title: "[Type] Session Scheduled for Your Student"       │
│  - Message: Student, Case ID, Date/Time, Location           │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  Teachers See Notification in Dashboard                     │
│  - Bell icon shows unread count                             │
│  - Click to view details                                    │
│  - Link to case report                                      │
└─────────────────────────────────────────────────────────────┘
```

### Automatic Teacher Detection
The system uses multiple methods to find the correct adviser/teacher:

1. **Teacher Name Match**: Searches for teachers whose name matches the `teacher_name` field in the incident report
2. **Section Adviser**: If the report is linked to a Section with an assigned adviser, that teacher is notified
3. **Teacher Assignment**: Matches teachers based on curriculum, grade level, and section name from the TeacherAssignment records

### Notification Triggers

#### 1. Guidance Counselor Creates Counseling Schedule
- **When**: Counselor schedules a counseling session for a student
- **Who Gets Notified**: 
  - Student (existing)
  - Reporter (existing)
  - **Adviser/Teacher (NEW)** - based on student's curriculum, grade, section
- **Notification Content**: 
  - Title: "Counseling Session Scheduled for Your Student"
  - Details: Student name, case ID, date/time, location, counselor name

#### 2. ESP Teacher Creates VPF Schedule
- **When**: ESP Teacher schedules a Values Reflective Formation (VPF) session
- **Who Gets Notified**:
  - Student (existing)
  - **Adviser/Teacher (NEW)** - based on student's curriculum, grade, section
- **Notification Content**:
  - Title: "VPF Session Scheduled for Your Student"
  - Details: Student name, case ID, date/time, location, ESP teacher name

#### 3. Discipline Officer Creates DO Schedule
- **When**: DO schedules a parent conference, interview, or follow-up meeting
- **Who Gets Notified**:
  - Student (existing)
  - DO (confirmation - existing)
  - **Adviser/Teacher (NEW)** - based on student's curriculum, grade, section
- **Notification Content**:
  - Title: "[Schedule Type] Scheduled for Your Student"
  - Details: Student name, case ID, date/time, location, DO name

## Implementation Details

### Helper Functions

#### `notify_adviser_of_counseling()` (in views.py)
```python
def notify_adviser_of_counseling(report, scheduled_date, location, counselor_name, schedule_type='Counseling')
```
- Used by Guidance Counselors and ESP Teachers
- Finds and notifies advisers based on report details
- Supports both Counseling and VPF schedule types

#### `notify_adviser_of_do_schedule()` (in do_schedule_views.py)
```python
def notify_adviser_of_do_schedule(report, scheduled_date, location, do_name, schedule_type)
```
- Used by Discipline Officers
- Finds and notifies advisers based on report details
- Supports all DO schedule types (parent conference, interview, follow-up)

### Modified Views

1. **Counselor Schedule Creation** (`views.py` - counselor_schedule view)
   - Added call to `notify_adviser_of_counseling()` after creating CounselingSchedule

2. **VPF Schedule Creation** (`views.py` - vpf_schedule view)
   - Added call to `notify_adviser_of_counseling()` after creating VPFSchedule

3. **DO Schedule Creation** (`do_schedule_views.py` - create_do_schedule view)
   - Added call to `notify_adviser_of_do_schedule()` after creating DOSchedule

## Benefits

1. **Improved Communication**: Teachers/advisers are automatically informed when their students have counseling sessions
2. **Better Monitoring**: Advisers can track their students' behavioral interventions
3. **Coordination**: Teachers can prepare or follow up with students before/after sessions
4. **Transparency**: All stakeholders are kept in the loop about student support activities

## Teacher View

Teachers will receive notifications in their notification panel showing:
- Which student has a scheduled session
- Type of session (Counseling, VPF, Parent Conference, etc.)
- Date, time, and location
- Who scheduled it (Counselor, ESP Teacher, or DO)
- Related case ID for reference

## Example Notification

**Title**: Counseling Session Scheduled for Your Student

**Message**: A counseling session has been scheduled for your student Juan Dela Cruz (Case: 2024-0015) on December 15, 2024 at 2:00 PM. Location: Guidance Office. Counselor: Maria Santos.

## Technical Notes

- Multiple teachers may be notified if multiple matches are found (e.g., subject teachers and advisers)
- Notifications are only sent if a valid teacher match is found
- The system gracefully handles cases where no teacher is found (no error, just no notification)
- All notifications are stored in the Notification model and visible in the teacher's dashboard

## Future Enhancements

Potential improvements:
- Email notifications in addition to in-app notifications
- SMS notifications for urgent sessions
- Calendar integration for teachers
- Batch notification summaries (daily/weekly digest)
