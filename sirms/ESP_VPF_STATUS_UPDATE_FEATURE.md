# ESP Teacher VPF Status Update Feature

## Overview
ESP Teachers can now update the status of their VPF (Values Reflective Formation) cases with notes. The guidance counselor who assigned the case receives automatic notifications.

## Features

### 1. Status Options
ESP Teachers can update VPF case status to:
- **Pending** - Case is waiting to be addressed
- **Ongoing** - Currently working with the student
- **Completed** - VPF session/intervention completed

### 2. Notes Requirement
- Notes are **required** with each status update
- Notes are timestamped and appended to case history
- Format: `[YYYY-MM-DD HH:MM] Status updated from 'old' to 'new' by [ESP Teacher Name]: [Notes]`

### 3. Automatic Notifications
When status is updated:
- **Guidance Counselor** (who assigned the case) receives notification
- Notification includes:
  - Case ID
  - Student name
  - New status
  - ESP Teacher's notes
  - Link to the report

## How to Use

### For ESP Teachers:

1. **Navigate to VPF Cases**
   - Go to sidebar → VPF Cases
   - View all cases assigned to you

2. **Update Status**
   - Click "Update Status" button next to any case
   - Modal opens with current status pre-selected

3. **Fill in Details**
   - Select new status (Pending, Ongoing, or Completed)
   - Add notes (required) - describe what happened, progress, etc.
   - Click "Update & Notify"

4. **Confirmation**
   - Success message appears
   - Page refreshes to show updated status
   - Guidance counselor receives notification automatically

### For Guidance Counselors:

1. **Receive Notifications**
   - Check notifications bell icon
   - See VPF status updates from ESP Teachers

2. **View Update History**
   - Go to case detail page
   - View all status updates with timestamps and notes

## User Interface

### VPF Cases Page
- New "Update Status" button added next to "View" button
- Button is green with edit icon
- Available for all cases regardless of current status

### Status Update Modal
- Clean, professional design
- Shows student name and case ID in title
- Status dropdown (required)
- Notes textarea (required)
- Info message: "Guidance counselor will be notified"
- Cancel and "Update & Notify" buttons

### Status Badges
Status is displayed with color-coded badges:
- **Pending**: Yellow badge
- **Ongoing**: Purple badge
- **Completed**: Green badge

## Technical Implementation

### Files Modified:
1. `templates/esp/vpf_cases.html` - Added button and modal
2. `incidents/views.py` - Added `update_vpf_status` view
3. `incidents/urls.py` - Added URL route

### Database Changes:
- No migration needed
- Uses existing VPFCase model fields:
  - `status` field (existing)
  - `notes` field (existing)

### API Endpoint:
- **URL**: `/vpf/update-status/<vpf_id>/`
- **Method**: POST
- **Parameters**:
  - `status`: New status value
  - `notes`: Update notes
- **Response**: JSON with success/error message

### Notification System:
- Uses existing Notification model
- Sent to `vpf_case.assigned_by` (guidance counselor)
- Includes report link for easy access

## Workflow Example

### Scenario: Student Completes VPF Session

1. **ESP Teacher** (Ms. Garcia):
   - Opens VPF Cases page
   - Finds case for John Doe (SIRMS-2024-001)
   - Current status: "Ongoing"
   - Clicks "Update Status"

2. **Update Form**:
   - Selects status: "Completed"
   - Adds notes: "Student completed all 3 VPF sessions. Showed significant improvement in behavior and understanding of school values. Recommended for case closure."
   - Clicks "Update & Notify"

3. **System Actions**:
   - Updates VPFCase status to "Completed"
   - Appends timestamped notes to case
   - Creates notification for guidance counselor

4. **Guidance Counselor** (Mr. Santos):
   - Receives notification: "VPF Status Updated - SIRMS-2024-001"
   - Reads: "ESP Teacher Ms. Garcia updated VPF case status to 'Completed' for John Doe. Notes: Student completed all 3 VPF sessions..."
   - Can click to view full case details

## Benefits

1. **Better Communication**: Guidance counselors stay informed of VPF progress
2. **Accountability**: All status changes are logged with timestamps
3. **Transparency**: Clear history of case progression
4. **Efficiency**: No need for manual emails or meetings for updates
5. **Documentation**: Complete audit trail of VPF interventions

## Status Progression

Typical VPF case flow:
```
Pending → Ongoing → Completed
   ↓         ↓          ↓
(Assigned) (Working) (Finished)
```

ESP Teachers can update to any status as needed based on the situation.

## Notes Best Practices

### Good Notes Examples:
- "First session completed. Student was receptive and engaged in discussion about respect and responsibility."
- "Second session scheduled for next week. Student showing improvement in classroom behavior per teacher feedback."
- "All sessions completed. Student demonstrated understanding of school values. Recommend case closure."

### What to Include:
- Session progress
- Student behavior/attitude
- Specific improvements or concerns
- Next steps or recommendations
- Any follow-up needed

## Testing Checklist

- [x] ESP Teacher can see "Update Status" button
- [x] Modal opens with correct case information
- [x] Status dropdown works
- [x] Notes field is required
- [x] Form validation works
- [x] Status updates successfully
- [x] Notes are appended with timestamp
- [x] Guidance counselor receives notification
- [x] Page refreshes after update
- [x] Status badge updates correctly

## Future Enhancements

Potential additions:
- Email notifications in addition to in-app
- Status change history view
- Bulk status updates
- Reminder notifications for pending cases
- Progress reports generation

## Support

If you encounter issues:
1. Check that you're logged in as ESP Teacher
2. Verify the case is assigned to you
3. Ensure both status and notes are filled
4. Check browser console for errors
5. Contact system administrator if problem persists
