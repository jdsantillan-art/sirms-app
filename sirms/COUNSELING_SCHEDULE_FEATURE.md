# Counseling Schedule Feature

## Overview
The Counseling Schedule feature allows counselors to schedule and manage counseling sessions for all non-VPF interventions. This feature works similarly to the VPF Schedule system used by ESP Teachers.

## How It Works

### 1. Case Evaluation Flow
When a counselor evaluates a case in the **Referral Evaluation** page:

- **VPF Cases** (Values Reflective Formation):
  - Automatically routed to ESP Teachers
  - Managed through the VPF Schedule system
  - NOT included in the Counseling Schedule

- **All Other Interventions**:
  - 1st Commission: Parent Conference, Counseling/Follow-up/Supervised Intervention
  - 2nd Commission: Parent Conference, Counseling/Follow-up/Supervised Intervention
  - 3rd Commission: Parent Conference, Counseling/Follow-up/Supervised Intervention
  - Automatically redirected to **Counseling Schedule** page
  - Counselor can schedule the session immediately

### 2. Counseling Schedule Page
**URL**: `/counselor-schedule/`

**Features**:
- **Pending Cases Section**: Shows all evaluated cases that need scheduling
- **Calendar View**: Visual calendar showing all scheduled sessions
- **List View**: Table view of all scheduled sessions with details
- **Schedule Modal**: Quick scheduling interface with:
  - Date & Time picker
  - Location field
  - Notes field
  - Automatic notifications to student and reporter

### 3. Session Management
Counselors can:
- ✅ **Mark as Completed**: When session is finished
- ❌ **Mark as Missed**: When student doesn't attend
- 📝 **View Notes**: See session details and notes
- 📅 **View in Calendar**: See all sessions in monthly calendar view

### 4. Notifications
The system automatically sends notifications to:
- **Student**: When session is scheduled, completed, or missed
- **Reporter** (Teacher who filed the report): When session is scheduled

## Database Structure

### CounselingSchedule Model
```python
- evaluation: Link to CaseEvaluation
- counselor: Counselor managing the session
- student: Student attending the session
- scheduled_date: Date and time of session
- location: Where the session will take place
- notes: Additional notes about the session
- status: scheduled, completed, missed, rescheduled
```

## User Flow Example

1. **Counselor evaluates a case**:
   - Case ID: SIRMS-2024-001
   - Student: John Doe
   - Commission: 2nd Commission
   - Intervention: Counseling/Follow-up/Supervised Intervention

2. **System redirects to Counseling Schedule**:
   - Case appears in "Pending Counseling Cases" section
   - Pre-selected for quick scheduling

3. **Counselor clicks "Schedule Session"**:
   - Modal opens with student and case info
   - Counselor selects date/time, location, adds notes
   - Clicks "Schedule & Notify"

4. **System creates schedule and sends notifications**:
   - Student receives notification with date, time, location
   - Reporter receives notification that session is scheduled
   - Schedule appears in calendar and list views

5. **After the session**:
   - Counselor marks as "Completed" or "Missed"
   - Student receives notification of status

## Key Differences from VPF Schedule

| Feature | VPF Schedule | Counseling Schedule |
|---------|-------------|---------------------|
| **Managed By** | ESP Teachers | Counselors |
| **Intervention Type** | Values Reflective Formation only | All non-VPF interventions |
| **Auto-Redirect** | No | Yes, after evaluation |
| **Commission Levels** | 2nd and 3rd only | All (1st, 2nd, 3rd) |

## Benefits

1. **Streamlined Workflow**: Automatic redirect after evaluation
2. **Better Organization**: All counseling sessions in one place
3. **Improved Communication**: Automatic notifications to all parties
4. **Visual Management**: Calendar view for easy scheduling
5. **Status Tracking**: Track completed, missed, and scheduled sessions

## Access
- **Role Required**: Counselor
- **Navigation**: Dashboard → Counselor Schedule (or auto-redirect from evaluation)
