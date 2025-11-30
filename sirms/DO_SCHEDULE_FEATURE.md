# DO Schedule Feature

## Overview
The DO Schedule feature allows Discipline Officers to schedule and manage parent conferences, interviews, and follow-up meetings. All schedules are saved and accessible through a dedicated "DO Schedule" sidebar menu.

## Implementation Date
November 28, 2025

## Features

### 1. Schedule Types
- **Parent Conference**: Meetings with parents/guardians
- **Interview**: One-on-one interviews with students or parents
- **Follow-up Meeting**: Follow-up sessions for ongoing cases

### 2. Schedule Management
- Create new schedules
- View upcoming schedules
- View past schedules
- Update schedule status
- Delete schedules
- Add notes and outcomes

### 3. Status Tracking
- **Scheduled**: Meeting is scheduled
- **Completed**: Meeting was completed
- **Cancelled**: Meeting was cancelled
- **Rescheduled**: Meeting was rescheduled
- **No Show**: Attendee(s) did not show up

## Access

### Sidebar Menu
- **Location**: DO sidebar menu
- **Icon**: 📅 Calendar check icon
- **Label**: "DO Schedule"
- **URL**: `/do-schedule/`

### Permissions
- **Access**: Discipline Officers only
- **Other roles**: Redirected to dashboard with error message

## How to Use

### Creating a Schedule

1. Click "DO Schedule" in the sidebar
2. Click "Schedule Meeting" button
3. Fill in the form:
   - **Meeting Type**: Select type (Parent Conference, Interview, Follow-up)
   - **Student Email**: Optional - link to a specific student
   - **Date & Time**: When the meeting will occur
   - **Location**: Where the meeting will take place (default: Discipline Office)
   - **Attendees**: List who will attend
   - **Purpose**: Describe the purpose of the meeting
   - **Notes**: Optional notes or outcomes
   - **Status**: Current status (default: Scheduled)
4. Click "Schedule Meeting"

### Viewing Schedules

**Upcoming Schedules**:
- Displayed in green cards
- Shows all future scheduled meetings
- Includes date, time, location, attendees, and purpose
- Quick actions: Update, Delete

**Past Schedules**:
- Displayed in a table format
- Shows all past meetings
- Includes status badges (Completed, Cancelled, etc.)
- Can update status and add notes

### Updating Schedule Status

1. Click "Update" button on any schedule
2. Select new status from dropdown
3. Add notes about the meeting
4. Click "Update"

### Deleting a Schedule

1. Click "Delete" button on any schedule
2. Confirm deletion
3. Schedule is removed and student is notified (if linked)

## Notifications

### Student Notifications
Students receive notifications when:
- A schedule is created (if linked to the schedule)
- Schedule status is updated
- Schedule is deleted/cancelled

### DO Notifications
Discipline Officers receive:
- Confirmation when schedule is created
- Reminders for upcoming meetings (future enhancement)

## Database Model

### DOSchedule Model
```python
class DOSchedule(models.Model):
    report = ForeignKey to IncidentReport (optional)
    discipline_officer = ForeignKey to CustomUser (DO)
    student = ForeignKey to CustomUser (Student, optional)
    schedule_type = CharField (Parent Conference, Interview, Follow-up)
    scheduled_date = DateTimeField
    location = CharField (default: Discipline Office)
    attendees = TextField
    purpose = TextField
    notes = TextField
    status = CharField (Scheduled, Completed, Cancelled, etc.)
    created_at = DateTimeField
    updated_at = DateTimeField
```

## Form Fields

### Required Fields
- Meeting Type
- Date & Time
- Location
- Purpose

### Optional Fields
- Student Email (for linking to student)
- Attendees
- Notes
- Status (defaults to Scheduled)

## Statistics Dashboard

The DO Schedule page displays:
- **Total Schedules**: All schedules created
- **Scheduled**: Currently scheduled meetings
- **Completed**: Successfully completed meetings
- **Cancelled**: Cancelled meetings

## Integration with Reports

### Link to Incident Reports
- Schedules can be linked to specific incident reports
- When creating a schedule from a report, the case ID is pre-filled
- Purpose field auto-fills with "Regarding incident report [CASE_ID]"

### Student Linking
- Enter student email to automatically link the schedule
- System validates email and finds the student
- Student receives notifications about the schedule

## UI/UX Features

### Color Coding
- **Upcoming**: Green theme (green cards, green borders)
- **Completed**: Green badge
- **Cancelled**: Red badge
- **No Show**: Yellow badge
- **Rescheduled**: Gray badge

### Icons
- 📅 Calendar icons throughout
- 🕐 Clock for time
- 📍 Location marker
- 👥 Users for attendees
- 📋 Clipboard for purpose

### Responsive Design
- Works on all devices
- Mobile-friendly layout
- Touch-friendly buttons

## Files Created/Modified

### New Files
1. `sirms/incidents/do_schedule_views.py` - Views for DO schedule
2. `sirms/templates/do/do_schedule.html` - Main schedule page
3. `sirms/templates/do/create_do_schedule.html` - Create schedule form
4. `sirms/incidents/migrations/0023_doschedule.py` - Database migration

### Modified Files
1. `sirms/incidents/models.py` - Added DOSchedule model
2. `sirms/incidents/forms.py` - Added DOScheduleForm
3. `sirms/incidents/urls.py` - Added DO schedule URLs
4. `sirms/templates/base.html` - Added sidebar menu item

## URLs

- `/do-schedule/` - Main schedule page
- `/do-schedule/create/` - Create new schedule
- `/do-schedule/<id>/update/` - Update schedule status
- `/do-schedule/<id>/delete/` - Delete schedule

## Future Enhancements (Optional)

### Possible Additions
- Email reminders for upcoming meetings
- Calendar export (iCal format)
- Recurring schedules
- Bulk scheduling
- SMS notifications
- Integration with Google Calendar
- Print schedule reports
- Filter by date range
- Search functionality
- Export to PDF/Excel

### Analytics
- Meeting completion rate
- Average meeting duration
- Most common meeting types
- Parent attendance tracking
- Monthly/yearly statistics

## Benefits

### For Discipline Officers
- ✅ Centralized schedule management
- ✅ Never miss a parent conference
- ✅ Track meeting outcomes
- ✅ Professional record keeping
- ✅ Easy status updates

### For Students/Parents
- ✅ Receive notifications about meetings
- ✅ Know when and where to attend
- ✅ Clear communication
- ✅ Transparency in the process

### For the System
- ✅ Complete audit trail
- ✅ Better case management
- ✅ Improved parent engagement
- ✅ Professional documentation
- ✅ Compliance with procedures

## Testing Checklist

- [x] Database model created
- [x] Migration applied successfully
- [x] Forms working correctly
- [x] Views accessible by DO only
- [x] Sidebar menu item appears for DO
- [x] Create schedule form works
- [x] Schedule list displays correctly
- [x] Update status works
- [x] Delete schedule works
- [x] Notifications sent correctly
- [ ] Student linking works (to be tested)
- [ ] Report linking works (to be tested)

## Support

For questions about this feature, refer to the main SIRMS documentation or contact the system administrator.

## Summary

The DO Schedule feature provides Discipline Officers with a professional tool to manage parent conferences and interviews. It includes:
- Easy scheduling interface
- Status tracking
- Notification system
- Integration with incident reports
- Complete audit trail

The feature is now live and accessible at **http://localhost:8000/do-schedule/** for Discipline Officer accounts!
