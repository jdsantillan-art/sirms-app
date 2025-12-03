# 🔄 Status Sync Visual Guide

## Quick Reference: Automatic Status Updates

### Scenario 1: DO Creates Schedule

```
┌─────────────────────────────────────────────────────────────┐
│  BEHAVIORAL CONCERNS PAGE (DO View)                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Case: 2025-0042                                            │
│  Status: [Classified] ← Pending                             │
│  Student: John Doe                                          │
│                                                              │
│  [Schedule Appointment] ← DO clicks this                    │
└─────────────────────────────────────────────────────────────┘
                          │
                          │ DO fills form and submits
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  SCHEDULE CREATED                                           │
├─────────────────────────────────────────────────────────────┤
│  ✅ DO Schedule created                                     │
│  ✅ Status: Scheduled                                       │
│  ✅ Date: Dec 6, 2025 at 2:00 PM                           │
└─────────────────────────────────────────────────────────────┘
                          │
                          │ AUTOMATIC SYNC
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  BEHAVIORAL CONCERN UPDATED                                 │
├─────────────────────────────────────────────────────────────┤
│  Case: 2025-0042                                            │
│  Status: [Under Review] ← AUTOMATICALLY UPDATED!            │
│  Student: John Doe                                          │
│                                                              │
│  📧 Notifications sent to:                                  │
│     • Reporter (Teacher)                                    │
│     • Student                                               │
│     • Adviser                                               │
└─────────────────────────────────────────────────────────────┘
```

### Scenario 2: DO Completes Schedule

```
┌─────────────────────────────────────────────────────────────┐
│  DO SCHEDULE PAGE                                           │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Parent Conference - John Doe                               │
│  Date: Dec 6, 2025 at 2:00 PM                              │
│  Status: [Scheduled]                                        │
│                                                              │
│  [Mark as Complete] ← DO clicks this                        │
└─────────────────────────────────────────────────────────────┘
                          │
                          │ DO confirms completion
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  SCHEDULE COMPLETED                                         │
├─────────────────────────────────────────────────────────────┤
│  ✅ Status updated to: Completed                            │
│  ✅ Meeting notes saved                                     │
└─────────────────────────────────────────────────────────────┘
                          │
                          │ AUTOMATIC SYNC
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  BEHAVIORAL CONCERN RESOLVED                                │
├─────────────────────────────────────────────────────────────┤
│  Case: 2025-0042                                            │
│  Status: [Resolved] ← AUTOMATICALLY UPDATED!                │
│  Student: John Doe                                          │
│                                                              │
│  📧 Notifications sent to:                                  │
│     • Reporter (Teacher): "Case Completed"                  │
│     • Student: "Status Updated"                             │
└─────────────────────────────────────────────────────────────┘
```

## Status Badge Colors

| Status | Badge Color | Meaning |
|--------|------------|---------|
| 🟡 Classified | Yellow | Pending schedule |
| 🔵 Under Review | Blue | Scheduled/In progress |
| 🟢 Resolved | Green | Completed |

## Notification Examples

### 1. When Schedule is Created

**To Reporter (Teacher):**
```
📧 Behavioral Concern Scheduled

The behavioral concern (Case: 2025-0042) has been scheduled. 
A parent conference will be held on December 6, 2025 at 2:00 PM.
Location: Discipline Office
```

**To Student:**
```
📧 Parent Conference Scheduled

You have a parent conference scheduled on December 6, 2025 at 2:00 PM.
Location: DO Office
Please be on time.
```

**To Adviser:**
```
📧 DO Appointment Scheduled - 2025-0042

A parent conference has been scheduled for your advisee John Doe 
on December 6, 2025 at 2:00 PM.
Location: Discipline Office
```

### 2. When Schedule is Completed

**To Reporter (Teacher):**
```
📧 Behavioral Concern Completed

The behavioral concern (Case: 2025-0042) has been resolved.
The parent conference was successfully completed on December 6, 2025.
```

**To Student:**
```
📧 Schedule Status Updated

Your parent conference scheduled for December 6, 2025 
has been marked as Completed.
```

## Timeline View

```
Day 1: Report Submitted
  └─ Status: Pending
       │
Day 2: DO Classifies as Minor
  └─ Status: Classified
       │
Day 3: DO Creates Schedule ⚡ AUTO-SYNC
  └─ Status: Under Review (Scheduled)
       │
Day 5: Meeting Held
       │
Day 5: DO Marks Complete ⚡ AUTO-SYNC
  └─ Status: Resolved
```

## What Happens Behind the Scenes

### When Creating Schedule:

```python
# 1. DO submits schedule form
schedule = DOSchedule.objects.create(...)

# 2. System automatically updates behavioral concern
if schedule.report:
    schedule.report.status = 'under_review'  # ⚡ Magic happens here
    schedule.report.save()

# 3. Notifications sent automatically
Notification.objects.create(...)  # To reporter
Notification.objects.create(...)  # To student
Notification.objects.create(...)  # To adviser
```

### When Completing Schedule:

```python
# 1. DO marks schedule as complete
schedule.status = 'completed'
schedule.save()

# 2. System automatically updates behavioral concern
if schedule.report and new_status == 'completed':
    schedule.report.status = 'resolved'  # ⚡ Magic happens here
    schedule.report.save()

# 3. Completion notifications sent
Notification.objects.create(...)  # To reporter
Notification.objects.create(...)  # To student
```

## Benefits at a Glance

| Before (Manual) | After (Automatic) |
|----------------|-------------------|
| DO creates schedule | DO creates schedule |
| DO manually updates status | ✅ Status updates automatically |
| DO notifies parties manually | ✅ Notifications sent automatically |
| Risk of forgetting | ✅ Never miss an update |
| 5-10 minutes per case | ✅ Instant |

## Common Questions

**Q: What if I create a schedule without linking a report?**
A: The schedule will be created normally, but no automatic status sync will occur since there's no linked behavioral concern.

**Q: Can I manually change the status?**
A: Yes, you can still manually update statuses if needed. The automatic sync only happens when schedules are created or completed.

**Q: What if I cancel or reschedule?**
A: Currently, cancelled/rescheduled appointments don't trigger automatic status changes. The behavioral concern remains in its current status.

**Q: Can I see the sync history?**
A: Status changes are tracked through the `updated_at` timestamp on the IncidentReport model. Future versions may include detailed audit logs.

## Testing the Feature

1. Go to Behavioral Concerns page
2. Find a case with status "Classified"
3. Click "Schedule Appointment"
4. Fill in the form and submit
5. ✅ Check: Status should now be "Under Review"
6. Go to DO Schedule page
7. Find the schedule you just created
8. Click "Mark as Complete"
9. ✅ Check: Behavioral Concern status should now be "Resolved"

---

**Feature Status:** ✅ Implemented and Ready
**Last Updated:** December 4, 2025
