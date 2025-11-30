# Counseling Schedule Validation Guide

## Visual Flow of Validations

```
┌─────────────────────────────────────────────────────────────┐
│              USER SELECTS DATE & TIME                       │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │  VALIDATION CHECK 1  │
              │   Is it a weekend?   │
              └──────────┬───────────┘
                         │
         ┌───────────────┴───────────────┐
         │                               │
         ▼ YES                           ▼ NO
┌────────────────────┐         ┌────────────────────┐
│  ⚠️ SHOW WARNING   │         │  VALIDATION CHECK 2│
│                    │         │  Is it in past?    │
│ "Weekend not       │         └────────┬───────────┘
│  allowed"          │                  │
│                    │         ┌────────┴────────┐
│ 🔴 DISABLE SUBMIT  │         │                 │
└────────────────────┘         ▼ YES             ▼ NO
                      ┌────────────────┐  ┌────────────────────┐
                      │ ⚠️ SHOW WARNING│  │  VALIDATION CHECK 3│
                      │                │  │  Schedule conflict?│
                      │ "Cannot        │  └────────┬───────────┘
                      │  schedule in   │           │
                      │  past"         │  ┌────────┴────────┐
                      │                │  │                 │
                      │ 🔴 DISABLE     │  ▼ YES             ▼ NO
                      │    SUBMIT      │  ┌──────────┐  ┌──────────┐
                      └────────────────┘  │⚠️ WARNING│  │✅ VALID  │
                                          │          │  │          │
                                          │"Conflict"│  │Enable    │
                                          │          │  │Submit    │
                                          │🔴 DISABLE│  │          │
                                          │  SUBMIT  │  │🟢 ALLOW  │
                                          └──────────┘  └────┬─────┘
                                                             │
                                                             ▼
                                                  ┌──────────────────┐
                                                  │ USER CLICKS      │
                                                  │ "SCHEDULE"       │
                                                  └────────┬─────────┘
                                                           │
                                                           ▼
                                                  ┌──────────────────┐
                                                  │ SERVER-SIDE      │
                                                  │ VALIDATION       │
                                                  │ (Double Check)   │
                                                  └────────┬─────────┘
                                                           │
                                         ┌─────────────────┴─────────────────┐
                                         │                                   │
                                         ▼ PASS                              ▼ FAIL
                                  ┌──────────────┐                  ┌──────────────┐
                                  │ ✅ CREATE    │                  │ ❌ ERROR     │
                                  │    SCHEDULE  │                  │    MESSAGE   │
                                  │              │                  │              │
                                  │ 📧 SEND      │                  │ 🔙 REDIRECT  │
                                  │    NOTIFS    │                  │    BACK      │
                                  └──────────────┘                  └──────────────┘
```

## Validation Examples

### Example 1: Weekend Selection ❌

```
User Action:
  Selects: Saturday, December 7, 2024 at 10:00 AM

System Response:
  ⚠️ Warning Box Appears:
  ┌─────────────────────────────────────────────────┐
  │ ⚠️ Weekend scheduling is not allowed.           │
  │    Please select a weekday.                     │
  └─────────────────────────────────────────────────┘
  
  🔴 Submit Button: DISABLED (grayed out)
  
User Must:
  Select a weekday (Monday-Friday)
```

### Example 2: Past Date Selection ❌

```
User Action:
  Selects: November 20, 2024 at 2:00 PM (past date)

System Response:
  ⚠️ Warning Box Appears:
  ┌─────────────────────────────────────────────────┐
  │ ⚠️ Cannot schedule in the past.                 │
  │    Please select a future date and time.        │
  └─────────────────────────────────────────────────┘
  
  🔴 Submit Button: DISABLED (grayed out)
  
User Must:
  Select a future date and time
```

### Example 3: Schedule Conflict ❌

```
Existing Schedule:
  Student: John Doe
  Date: December 5, 2024 at 10:00 AM
  Status: Scheduled

User Action:
  Tries to schedule same student:
  Date: December 5, 2024 at 10:30 AM (within 1 hour)

System Response:
  ⚠️ Warning Box Appears:
  ┌─────────────────────────────────────────────────┐
  │ ⚠️ This student already has a session scheduled │
  │    at this time. Please choose a different time.│
  └─────────────────────────────────────────────────┘
  
  🔴 Submit Button: DISABLED (grayed out)
  
User Must:
  Select a time at least 1 hour away from existing schedule
```

### Example 4: Valid Selection ✅

```
User Action:
  Selects: December 5, 2024 (Thursday) at 2:00 PM
  No existing schedules for this student at this time

System Response:
  ✅ No warnings shown
  🟢 Submit Button: ENABLED (green, clickable)
  
User Can:
  Click "Schedule & Notify" to create the session
```

## View Toggle Behavior

### Before Update ❌
```
┌─────────────────────────────────────────────────┐
│  Pending Cases                                  │
├─────────────────────────────────────────────────┤
│  Calendar View (Always Visible)                 │
│  [Calendar displayed here]                      │
├─────────────────────────────────────────────────┤
│  List View (Always Visible)                     │
│  [Table displayed here]                         │
└─────────────────────────────────────────────────┘
Problem: Both views shown, cluttered interface
```

### After Update ✅
```
Default (List View):
┌─────────────────────────────────────────────────┐
│  Pending Cases                                  │
├─────────────────────────────────────────────────┤
│  List View (Visible)                            │
│  [Table displayed here]                         │
└─────────────────────────────────────────────────┘

Click "Calendar View":
┌─────────────────────────────────────────────────┐
│  Pending Cases                                  │
├─────────────────────────────────────────────────┤
│  Calendar View (Visible)                        │
│  [Calendar displayed here]                      │
└─────────────────────────────────────────────────┘

Result: Clean, focused interface
```

## Conflict Detection Logic

### Time Window Check
```
Existing Schedule: 10:00 AM
Time Window: 9:00 AM - 11:00 AM (±1 hour)

❌ BLOCKED:
  - 9:00 AM (within window)
  - 9:30 AM (within window)
  - 10:00 AM (exact match)
  - 10:30 AM (within window)
  - 11:00 AM (within window)

✅ ALLOWED:
  - 8:59 AM (outside window)
  - 11:01 AM (outside window)
  - 2:00 PM (outside window)
```

### Status Check
```
Only checks schedules with status:
  ✅ "scheduled" - Active, blocks new schedules
  ✅ "rescheduled" - Active, blocks new schedules
  
Ignores schedules with status:
  ⏭️ "completed" - Past, doesn't block
  ⏭️ "missed" - Past, doesn't block
```

## Error Messages Reference

| Scenario | Message | Action |
|----------|---------|--------|
| Weekend selected | "Weekend scheduling is not allowed. Please select a weekday." | Disable submit, show warning |
| Past date | "Cannot schedule in the past. Please select a future date and time." | Disable submit, show warning |
| Conflict detected | "This student already has a session scheduled at this time. Please choose a different time." | Disable submit, show warning |
| Server validation fails | "Schedule conflict: [Student Name] already has a session scheduled within this time window." | Redirect back with error |

## Best Practices for Counselors

### ✅ DO:
- Schedule during weekdays (Monday-Friday)
- Check calendar for existing appointments
- Allow at least 1 hour between sessions for same student
- Schedule during business hours (8 AM - 5 PM recommended)

### ❌ DON'T:
- Try to schedule on weekends
- Schedule in the past
- Book overlapping sessions for same student
- Ignore warning messages

## Quick Troubleshooting

**Q: Submit button is disabled, why?**
A: Check for red warning box above the date field. Fix the issue mentioned.

**Q: I selected a valid date but still see warning?**
A: Check if the student already has a session within 1 hour of selected time.

**Q: Can I schedule two different students at the same time?**
A: Yes! Conflict check is per-student, not per-counselor.

**Q: What if I need to schedule on weekend for emergency?**
A: Contact system administrator to manually create the schedule.

**Q: How do I see existing schedules?**
A: Use Calendar View to see all scheduled sessions visually.
