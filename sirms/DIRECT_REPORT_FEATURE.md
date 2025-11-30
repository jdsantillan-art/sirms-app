# Direct Report Feature

## Overview
The Direct Report feature allows Discipline Officers (DO) and Guidance Counselors to manually encode incident reports that are made directly to their offices (in-person reports).

## Feature Location
- **Sidebar Menu**: "Direct Report" (appears at the top of the sidebar for DO and Guidance roles)
- **URL**: `/direct-report/`
- **Icon**: 🏥 (file-medical)

## Access Control
- **Discipline Officers (DO)**: ✅ Full access
- **Guidance Counselors**: ✅ Full access
- **Other roles**: ❌ No access (redirected to dashboard)

## How It Works

### 1. For Discipline Officers (DO)
When a DO creates a direct report:
- The report is saved with status `pending`
- DO receives a confirmation notification
- The report follows the normal workflow:
  - Fact-checking
  - Classification (minor/major)
  - Routing to appropriate handler

### 2. For Guidance Counselors
When a Guidance Counselor creates a direct report:
- The report is saved with status `under_review`
- All DOs are notified about the direct report
- Counselor receives a confirmation notification
- The report can be immediately reviewed and evaluated

### 3. Student Notification
- If a student is successfully linked (via email/username), they receive a notification
- The notification informs them that a report has been filed regarding them

## Form Fields

### Reporter Information
- **First Name** (required): Name of the person who reported to the office
- **Middle Name** (optional)
- **Last Name** (required)

### Academic Information
- **Curriculum** (required): Junior High School or Senior High School
- **Grade Level**: Auto-populated based on curriculum
- **Section**: Auto-populated based on grade level
- **Teacher**: Auto-filled based on section selection

### Involved Students
- **Names or IDs**: Can enter student email, username, or just names
- System attempts to auto-link students if email/username is provided
- If no match found, the name is stored for later assignment

### Incident Details
- **Date** (required): When the incident occurred
- **Time** (required): Time of the incident
- **Violation Type** (required): Prohibited Acts or Other School Policies
- **Bullying Type**: Appears automatically if "Bullying" is selected
- **Legal References**: Displayed automatically based on violation type
- **Description**: Detailed description of the incident
- **Evidence**: Optional file upload (PDF, images, videos)

## System Process Flow

```
Direct Report Created
        ↓
[DO creates] → Status: pending → Fact-check → Classify → Route
        ↓
[Counselor creates] → Status: under_review → Evaluate → Schedule/VPF
        ↓
Notifications sent to:
- Reporter (DO/Counselor) - Confirmation
- Student (if linked) - Incident filed
- DOs (if created by Counselor) - New direct report
```

## Key Features

### 1. Same Form as Regular Report
- Uses the same incident report form structure
- Maintains consistency across the system
- All validation rules apply

### 2. Auto-Linking Students
- System attempts to find and link students automatically
- Searches by email first, then username
- If not found, stores name for manual assignment later

### 3. Dynamic Dropdowns
- Curriculum → Grade Level → Section → Teacher
- All dropdowns update automatically based on selections
- Teacher names are auto-filled from the database

### 4. Legal References
- Automatically displays relevant laws and policies
- Shows when violation type is selected
- Helps ensure compliance with regulations

### 5. Bullying Type Selection
- Appears only when "Bullying" violation is selected
- Required field when visible
- Options: Physical, Psychological, Sexual, Emotional, Cyber, Social, Gender-based

## Benefits

### For Discipline Officers
- ✅ Quick encoding of walk-in reports
- ✅ Maintains complete audit trail
- ✅ Follows standard workflow
- ✅ All notifications work automatically

### For Guidance Counselors
- ✅ Can record reports made directly to guidance office
- ✅ Immediate access to review and evaluate
- ✅ DOs are kept informed
- ✅ Seamless integration with counseling workflow

### For the System
- ✅ All reports are recorded in one place
- ✅ No reports are lost or forgotten
- ✅ Complete tracking and analytics
- ✅ Maintains data integrity

## Design Consistency
- **Green theme**: Matches the SIRMS color scheme
- **Responsive**: Works on all devices
- **User-friendly**: Clear labels and instructions
- **Accessible**: Proper form validation and error messages

## Technical Implementation

### Files Created/Modified
1. **sirms/incidents/direct_report_views.py** - New view file
2. **sirms/incidents/urls.py** - Added route
3. **sirms/templates/base.html** - Added sidebar links
4. **sirms/templates/direct_report.html** - New template

### Database
- Uses existing `IncidentReport` model
- No schema changes required
- All relationships maintained

### Notifications
- Uses existing notification system
- Automatic notification creation
- Role-based notification routing

## Testing Checklist

- [ ] DO can access Direct Report page
- [ ] Guidance Counselor can access Direct Report page
- [ ] Other roles are blocked from accessing
- [ ] Form validation works correctly
- [ ] Student auto-linking works
- [ ] Notifications are sent correctly
- [ ] Reports appear in All Reports
- [ ] Workflow continues normally
- [ ] Evidence upload works
- [ ] Legal references display correctly

## Future Enhancements (Optional)
- Add bulk import for multiple reports
- Add templates for common incident types
- Add quick-fill from previous reports
- Add voice-to-text for description field
- Add photo capture directly from camera

## Support
For issues or questions about this feature, contact the system administrator or refer to the main SIRMS documentation.
