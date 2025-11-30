# DO Behavioral Concerns Evaluation Feature

## Overview
Discipline Office (DO) staff can now evaluate behavioral concerns with specific actions and notify both the student (violator) and the reporter. This provides a structured approach to handling disciplinary cases.

## Features

### 1. Evaluation Actions
DO can select from three evaluation actions:
- **📝 Intake Interview** - Schedule an interview with the student
- **🔍 Investigate** - Conduct an investigation into the incident
- **👨‍👩‍👦 Parent Conference** - Schedule a conference with parents/guardians

### 2. Status Updates
Combined with evaluation actions, DO can update case status:
- **📋 Pending** - Awaiting Action
- **🔄 In Progress** - Being Handled
- **✅ Completed** - Case Resolved

### 3. Evaluation Notes
- Required notes field for documenting evaluation details
- Notes are timestamped and saved to case history
- Includes DO staff name, action taken, and detailed notes

### 4. Automatic Notifications
When evaluation is submitted:
- **Student (Violator)** receives notification with:
  - Case ID
  - Evaluation action taken
  - Specific instructions based on action type
  - Reminder to check with DO office
  
- **Reporter** receives notification with:
  - Case ID
  - Evaluation action taken
  - Current status
  - DO's evaluation notes

## How to Use

### For Discipline Office Staff:

1. **Navigate to Behavioral Concerns**
   - Go to sidebar → Behavior Concerns
   - View all cases handled by DO

2. **Evaluate a Case**
   - Click "Update Status" button on any case
   - Modal opens with evaluation form

3. **Fill in Evaluation Details**
   - **Evaluation Action** (required): Select action being taken
     - Intake Interview
     - Investigate
     - Parent Conference
   - **New Status** (required): Select current case status
   - **Evaluation Notes** (required): Document findings, actions, next steps

4. **Submit Evaluation**
   - Click "Update & Notify"
   - System saves evaluation and sends notifications
   - Success message confirms notifications sent

5. **View Evaluation History**
   - Each case shows "Update History" section
   - All evaluations are timestamped and logged
   - Complete audit trail of DO actions

## Notification Messages

### For Students (Based on Action):

**Intake Interview:**
```
The Discipline Office has scheduled an intake interview regarding your case. 
Please report to the DO office as instructed.
```

**Investigate:**
```
The Discipline Office is investigating your case. 
You may be called for questioning or clarification.
```

**Parent Conference:**
```
A parent conference has been scheduled regarding your case. 
Your parent/guardian will be contacted by the Discipline Office.
```

### For Reporters:
```
The Discipline Office has evaluated case [CASE_ID].

Action Taken: [ACTION]
Status: [STATUS]

Notes: [DO's evaluation notes]
```

## User Interface

### Behavioral Concerns Page
- Statistics dashboard showing total, pending, and completed cases
- List of all DO-handled cases with details
- "Update Status" button for each case (green button)

### Evaluation Modal
- Clean, professional design
- Shows case ID in title
- Three required fields:
  1. Evaluation Action dropdown
  2. Status dropdown
  3. Evaluation Notes textarea
- Info message: "Student (violator) and reporter will be automatically notified"
- Cancel and "Update & Notify" buttons

### Case Display
- Each case shows:
  - Case ID and status badge
  - Student and reporter information
  - Incident details
  - Update history (if any evaluations done)
  - Action buttons (View Details, Update Status)

## Technical Implementation

### Files Modified:
1. `templates/do/behavior_concerns.html` - Updated modal with evaluation action
2. `incidents/views.py` - Enhanced `behavior_concerns` view with evaluation logic

### Database Changes:
- No migration needed
- Uses existing models:
  - `IncidentReport` (status field)
  - `Classification` (internal_notes field)
  - `InternalNote` (for tracking)
  - `Notification` (for alerts)

### Evaluation Data Storage:
- **Classification.internal_notes**: Timestamped evaluation history
- **InternalNote**: Separate record for each evaluation
- **Format**: `[YYYY-MM-DD HH:MM] DO Evaluation by [Name]\nAction: [Action]\nStatus: [Status]\nNotes: [Notes]`

## Workflow Example

### Scenario: Student Caught Fighting

1. **DO Staff** (Mr. Johnson):
   - Opens Behavioral Concerns page
   - Finds case SIRMS-2024-015 (Fighting incident)
   - Current status: "Pending"
   - Clicks "Update Status"

2. **Evaluation Form**:
   - **Action**: Selects "Intake Interview"
   - **Status**: Changes to "In Progress"
   - **Notes**: "Scheduled intake interview for tomorrow 10 AM. Will interview both students involved to understand what happened. Parents will be contacted if necessary based on findings."
   - Clicks "Update & Notify"

3. **System Actions**:
   - Updates case status to "In Progress"
   - Saves evaluation with timestamp
   - Creates internal note for tracking
   - Sends notifications

4. **Student** (John Doe):
   - Receives notification: "Behavioral Concern Evaluation - Case SIRMS-2024-015"
   - Reads: "The Discipline Office has scheduled an intake interview regarding your case. Please report to the DO office as instructed."
   - Knows to expect interview

5. **Reporter** (Ms. Smith):
   - Receives notification: "DO Evaluation - Case SIRMS-2024-015"
   - Reads action taken and DO's notes
   - Stays informed of case progress

## Benefits

1. **Structured Process**: Standardized evaluation actions
2. **Clear Communication**: Students know what to expect
3. **Transparency**: Reporters stay informed of progress
4. **Documentation**: Complete audit trail of all evaluations
5. **Accountability**: All actions are logged with timestamps
6. **Efficiency**: Automated notifications save time

## Evaluation Action Guidelines

### When to Use Each Action:

**Intake Interview:**
- First-time offenders
- Need to gather student's perspective
- Minor incidents requiring clarification
- Building rapport before further action

**Investigate:**
- Conflicting accounts of incident
- Multiple students involved
- Need to gather evidence
- Serious allegations requiring verification

**Parent Conference:**
- Repeated violations
- Serious behavioral issues
- Parent involvement needed
- Suspension or major consequences considered

## Best Practices

### Good Evaluation Notes Examples:

**Intake Interview:**
```
Scheduled intake interview for [date/time]. Will discuss incident with student, 
review school policies, and determine appropriate next steps. Student has been 
notified to report to DO office.
```

**Investigate:**
```
Investigation initiated. Will interview witnesses, review evidence, and consult 
with teachers. Expected completion by [date]. Student and parents will be 
informed of findings.
```

**Parent Conference:**
```
Parent conference scheduled for [date/time]. Will discuss student's repeated 
violations, review behavior contract, and establish action plan. Both parents 
have been contacted and confirmed attendance.
```

### What to Include in Notes:
- Specific action being taken
- Timeline/schedule
- Who is involved
- Expected outcomes
- Next steps
- Any follow-up needed

## Testing Checklist

- [x] DO can see "Update Status" button
- [x] Modal opens with evaluation form
- [x] Evaluation action dropdown works
- [x] Status dropdown works
- [x] Notes field is required
- [x] Form validation works
- [x] Evaluation saves successfully
- [x] Student receives notification
- [x] Reporter receives notification
- [x] Evaluation history displays correctly
- [x] Internal notes are created

## Future Enhancements

Potential additions:
- Schedule specific dates for interviews/conferences
- Attach documents to evaluations
- Email notifications in addition to in-app
- Evaluation templates for common scenarios
- Bulk evaluation for multiple cases
- Parent notification system
- Follow-up reminders

## Support

If you encounter issues:
1. Check that you're logged in as DO
2. Verify all required fields are filled
3. Ensure case is assigned to DO
4. Check browser console for errors
5. Contact system administrator if problem persists
