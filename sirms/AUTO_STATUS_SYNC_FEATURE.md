# Automatic Status Synchronization Feature

## Overview
Automatic bidirectional status synchronization between **Behavioral Concerns** (IncidentReport) and **DO Schedule**.

## How It Works

### 1. When DO Creates a Schedule (Behavioral Concern → DO Schedule)

**Trigger:** DO successfully creates a schedule for a behavioral concern

**Automatic Actions:**
- ✅ Behavioral Concern status updates from `classified` → `under_review` (Scheduled)
- ✅ Reporter receives notification: "Behavioral Concern Scheduled"
- ✅ Student receives notification about the appointment
- ✅ Adviser receives notification (if applicable)

**Code Location:** `incidents/do_schedule_views.py` - `create_do_schedule()` function

```python
# AUTO-SYNC: Update Behavioral Concern status to 'under_review' when DO schedule is created
if schedule.report:
    schedule.report.status = 'under_review'  # Represents "Scheduled" status
    schedule.report.save()
```

### 2. When DO Completes a Schedule (DO Schedule → Behavioral Concern)

**Trigger:** DO marks a DO Schedule as `completed`

**Automatic Actions:**
- ✅ Behavioral Concern status updates from `under_review` → `resolved` (Completed)
- ✅ Reporter receives notification: "Behavioral Concern Completed"
- ✅ Student receives notification about completion
- ✅ Case is marked as resolved in the system

**Code Location:** `incidents/do_schedule_views.py` - `update_do_schedule_status()` function

```python
# AUTO-SYNC: Update Behavioral Concern status when DO Schedule is completed
if schedule.report and new_status == 'completed':
    schedule.report.status = 'resolved'
    schedule.report.save()
```

## Status Flow Diagram

```
BEHAVIORAL CONCERN                    DO SCHEDULE
─────────────────                    ───────────
                                     
classified (Pending)                      
         │                                
         │  DO creates schedule           
         ├──────────────────────────► scheduled
         │                                │
under_review (Scheduled) ◄───────────────┘
         │                                
         │  DO marks as complete          
         │                                │
         ├──────────────────────────► completed
         │                                │
resolved (Completed) ◄───────────────────┘
```

## Status Mapping

| Behavioral Concern Status | DO Schedule Status | Meaning |
|--------------------------|-------------------|---------|
| `classified` | N/A | Pending schedule |
| `under_review` | `scheduled` | Appointment scheduled |
| `resolved` | `completed` | Case completed |

## Notifications Sent

### When Schedule is Created:
1. **Reporter:** "Behavioral Concern Scheduled" with date/time/location
2. **Student:** "Appointment Scheduled" with details
3. **Adviser:** "DO Appointment Scheduled" for their advisee
4. **DO:** "Schedule Created" confirmation

### When Schedule is Completed:
1. **Reporter:** "Behavioral Concern Completed" with completion date
2. **Student:** "Schedule Status Updated" to completed
3. **Adviser:** Informed via existing notification system

## Testing

Run the test script to verify synchronization:

```bash
python test_status_sync.py
```

The test will:
1. Create a DO Schedule for a behavioral concern
2. Verify status updates to "under_review"
3. Mark schedule as completed
4. Verify status updates to "resolved"
5. Offer cleanup option

## Implementation Files

1. **`incidents/do_schedule_views.py`**
   - `create_do_schedule()` - Handles schedule creation and status sync
   - `update_do_schedule_status()` - Handles status updates and completion sync

2. **`incidents/behavior_concerns_views.py`**
   - `behavior_concerns()` - Handles schedule creation from behavioral concerns page

3. **`incidents/models.py`**
   - `IncidentReport` - Behavioral concern model
   - `DOSchedule` - DO schedule model
   - `Notification` - Notification system

## User Experience

### For Discipline Officers (DO):
- Create schedule → Status automatically updates to "Scheduled"
- Mark as complete → Status automatically updates to "Resolved"
- No manual status updates needed

### For Reporters (Teachers):
- Receive notification when their report is scheduled
- Receive notification when case is completed
- Can track progress automatically

### For Students:
- Notified about appointments
- Notified about completion
- Clear communication throughout process

### For Advisers:
- Notified when advisee has scheduled appointment
- Can track student case progress

## Benefits

✅ **Eliminates Manual Work:** No need to update status in two places
✅ **Prevents Errors:** Automatic sync ensures consistency
✅ **Better Communication:** All parties notified automatically
✅ **Audit Trail:** Clear status history maintained
✅ **Time Saving:** Reduces administrative overhead

## Future Enhancements

- Add status sync for cancelled/rescheduled appointments
- Track status change history
- Generate reports on case resolution times
- Email notifications for status changes
