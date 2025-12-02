# Behavior Concerns Schedule Fix

## Problem
When clicking the calendar/schedule button in Behavior Concerns and submitting the "Schedule Appointment" modal, it shows a server error and doesn't display in the DO Schedule sidebar.

## Root Cause
The behavior concerns view was missing - it was referenced in URLs but the actual view function didn't exist.

## Solution Implemented

### 1. Created `behavior_concerns_views.py`
- New dedicated view file for behavior concerns functionality
- Handles two POST actions:
  - `update_status`: Updates case status (Pending/Ongoing/Completed)
  - `schedule_appointment`: Creates DO Schedule and sends notifications

### 2. Updated `urls.py`
- Imported the new `behavior_concerns_views` module
- Updated the behavior-concerns URL to use the new view

### 3. Added `DOSchedule` Model (if not exists)
- Model for storing DO appointments
- Fields: report, discipline_officer, student, schedule_type, scheduled_date, location, purpose, notes, status
- Status choices: scheduled, completed, cancelled, rescheduled, no_show

## Features

### Schedule Appointment Flow:
1. DO clicks calendar icon on a case
2. Modal opens with form:
   - Appointment Type (Intake Interview, Investigation Meeting, Parent Conference, Follow-up Meeting)
   - Date & Time
   - Location
   - Notes
3. On submit:
   - Creates DOSchedule record
   - Notifies student with appointment details
   - Notifies adviser (if student has one)
   - Shows success message
   - Redirects to behavior concerns page

### Update Status Flow:
1. DO clicks edit icon on a case
2. Modal opens with status dropdown
3. On submit:
   - Updates report status
   - Notifies student
   - Notifies adviser
   - Shows success message

## Notifications Sent

### When Scheduling Appointment:
- **Student**: "You have a [Type] scheduled on [Date] at [Time]. Location: [Location]. Please be on time."
- **Adviser**: "A [Type] has been scheduled for your advisee [Student Name] on [Date] at [Time]. Location: [Location]."

### When Updating Status:
- **Student**: Status-specific message (Pending/Ongoing/Completed)
- **Adviser**: "Your advisee [Student Name] has a case status update to: [Status]"

## Next Steps

1. **Run Migrations** (if DOSchedule model was added):
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

2. **Test the Feature**:
   - Login as DO
   - Go to Behavior Concerns
   - Click calendar icon on a case
   - Fill in appointment details
   - Submit
   - Check DO Schedule sidebar - appointment should appear
   - Check notifications - student and adviser should be notified

3. **Verify DO Schedule Sidebar**:
   - The scheduled appointment should appear in the DO Schedule sidebar
   - Should show: Type, Student, Date/Time, Status

## Files Modified
- `sirms/incidents/behavior_concerns_views.py` (NEW)
- `sirms/incidents/urls.py` (UPDATED)
- `sirms/incidents/models.py` (UPDATED - added DOSchedule if not exists)

## Status
✅ View created
✅ URL updated
✅ Model added
⏳ Pending migration (if needed)
⏳ Pending testing

