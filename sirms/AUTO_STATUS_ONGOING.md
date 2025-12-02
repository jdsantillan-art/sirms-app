# ✅ Auto Status Update to "Ongoing" - DEPLOYED

## Status Changes to "Under Review" (Ongoing) When Scheduled

When DO or Guidance schedules a counseling session or meeting, the incident report status now automatically updates to **"under_review"** (displayed as "Under Review" or "Ongoing"), indicating active work on the case.

### What Changed:

**Previous Behavior:**
- Status changed to "pending" when scheduled
- Didn't clearly indicate active work

**New Behavior:**
- Status changes to "under_review" when scheduled
- Clearly shows case is actively being handled
- Indicates ongoing intervention

### Updated Logic:

#### DO Schedule (Parent Conference/Interview):
```python
# When DO creates schedule
if schedule.report:
    schedule.report.status = 'under_review'  # Changed from 'pending'
    schedule.report.save()
```

#### Counseling Schedule (Guidance):
```python
# When Counselor schedules counseling
report.status = 'under_review'  # Changed from 'pending'
report.save()
```

### Status Flow:

**Before:**
```
New Report → Pending → [Schedule Created] → Pending (no change)
```

**After:**
```
New Report → Pending → [Schedule Created] → Under Review (Ongoing)
```

### Display in System:

**All Reports Table:**
- Badge: "Under Review" (blue background)
- Indicates: Case is actively being worked on

**Report Detail:**
- Status: "Under Review"
- Meaning: Counseling/meeting scheduled and in progress

### Use Cases:

**1. DO Schedules Parent Conference:**
```
Status: Pending → Under Review
Meaning: Meeting scheduled, case actively being handled
```

**2. Counselor Schedules Counseling Session:**
```
Status: Pending → Under Review
Meaning: Counseling scheduled, intervention in progress
```

**3. Multiple Schedules:**
```
Status: Under Review (maintained)
Meaning: Ongoing intervention continues
```

### Benefits:

✅ **Clear Status** - Shows case is actively being worked on  
✅ **Better Tracking** - Distinguishes between pending and ongoing cases  
✅ **Accurate Reporting** - Reflects actual case status  
✅ **Workflow Clarity** - Staff knows case is in progress  
✅ **Automatic** - No manual status update needed

### Status Definitions:

| Status | Meaning | When Set |
|--------|---------|----------|
| **Pending** | Awaiting action | Initial report submission |
| **Under Review** | Actively being handled | Schedule created by DO/Guidance |
| **Classified** | Categorized by severity | DO classifies the case |
| **Evaluated** | Assessment complete | Guidance completes evaluation |
| **Sanctioned** | Consequences applied | Sanctions assigned |
| **Resolved** | Case closed successfully | Issue resolved |

### Updated Files:

1. **incidents/do_schedule_views.py**
   - Changed status update from 'pending' to 'under_review'
   - Applies when DO creates schedule

2. **incidents/views.py** (2 locations)
   - Changed status update from 'pending' to 'under_review'
   - Applies when Counselor schedules counseling

### Manual Override:

**Staff can still manually change status:**
- DO can update status in report detail
- Counselor can update status in case evaluation
- Status dropdown remains fully functional

### Testing:

**Test Scenario 1: DO Schedule**
1. Create incident report (Status: Pending)
2. DO schedules parent conference
3. Verify status changes to "Under Review"

**Test Scenario 2: Counseling Schedule**
1. Create incident report (Status: Pending)
2. Counselor schedules counseling session
3. Verify status changes to "Under Review"

**Test Scenario 3: Already Ongoing**
1. Report already has status "Under Review"
2. Create another schedule
3. Status remains "Under Review" (no change)

---

**Deployed**: December 2, 2025 - 11:00 PM  
**Commit**: `e082a43`  
**Status**: ✅ Live on Render

Reports now automatically show "Under Review" (Ongoing) status when scheduled!
