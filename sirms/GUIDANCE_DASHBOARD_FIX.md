# Guidance Dashboard Fix

## Overview
Fixed the Guidance Counselor dashboard to display accurate counts and proper navigation links based on the correct data sources.

## Implementation Date
November 28, 2025

## Issues Fixed

### 1. Total Prohibited Acts & Total OSP
**Problem**: Counts were not based on incident type severity

**Solution**: Updated to count based on `incident_type__severity`:
- **Prohibited Acts (PA)**: `incident_type__severity='prohibited'`
- **Other School Policies (OSP)**: `incident_type__severity='school_policy'`

```python
total_prohibited_acts = IncidentReport.objects.filter(
    incident_type__severity='prohibited'
).count()

total_osp = IncidentReport.objects.filter(
    incident_type__severity='school_policy'
).count()
```

### 2. Scheduled Sessions
**Problem**: Was using wrong model (CounselingSession instead of CounselingSchedule)

**Solution**: Changed to use `CounselingSchedule` model:
```python
scheduled_sessions_count = CounselingSchedule.objects.filter(
    counselor=user,
    status='scheduled'
).count()
```

**Link**: Now correctly goes to `counselor_schedule` (Counseling Schedule page)

### 3. Completed Sessions
**Problem**: 
- Count was from wrong source
- Link went to counseling_management instead of dedicated page
- No dedicated completed sessions page existed

**Solution**: 
- Created new `completed_sessions` view and template
- Count from `CounselingSchedule` with `status='completed'`
- Link now goes to dedicated completed sessions page

```python
completed_sessions_count = CounselingSchedule.objects.filter(
    counselor=user,
    status='completed'
).count()
```

**New Page**: `/completed-sessions/` - Shows all completed counseling sessions

### 4. Completed VPF
**Problem**: Count was correct but needed clarification

**Solution**: Confirmed counting from `VPFCase` with `status='completed'`:
```python
completed_vpf = VPFCase.objects.filter(status='completed').count()
```

**Note**: This counts ALL completed VPF cases (updated by ESP Teachers)

### 5. Total VPF Referrals
**Problem**: Was counting ALL VPF cases instead of only those assigned by this counselor

**Solution**: Changed to count only VPF cases assigned by the current counselor:
```python
total_vpf_referrals = VPFCase.objects.filter(assigned_by=user).count()
```

## Files Created/Modified

### New Files:
1. **sirms/incidents/completed_sessions_views.py** - New view for completed sessions
2. **sirms/templates/counselor/completed_sessions.html** - New template

### Modified Files:
1. **sirms/incidents/views.py** - Fixed counselor dashboard counts
2. **sirms/incidents/urls.py** - Added completed_sessions route
3. **sirms/templates/dashboard.html** - Updated counselor card links

## Dashboard Cards Summary

### Counselor Dashboard (6 cards):

1. **Total Prohibited Acts** (Red)
   - Count: All reports with PA incident types
   - Link: Major Case Review
   - Icon: Ban icon

2. **Total OSP** (Blue)
   - Count: All reports with OSP incident types
   - Link: Major Case Review
   - Icon: Clipboard list

3. **Scheduled Sessions** (Purple)
   - Count: CounselingSchedule with status='scheduled'
   - Link: Counselor Schedule (counselor_schedule)
   - Icon: Calendar

4. **Completed Sessions** (Green)
   - Count: CounselingSchedule with status='completed'
   - Link: Completed Sessions (completed_sessions) ← NEW
   - Icon: Check circle

5. **Completed VPF** (Orange)
   - Count: VPFCase with status='completed' (all)
   - Link: For VPF page
   - Icon: User shield

6. **Total VPF Referrals** (Teal)
   - Count: VPFCase assigned by this counselor
   - Link: For VPF page
   - Icon: User check

## Completed Sessions Page

### Features:
- Shows all completed counseling sessions for the counselor
- Displays in table format with columns:
  - Case ID (clickable link to report detail)
  - Student Name & Email
  - Grade/Section
  - Session Date & Time
  - Location
  - Notes (truncated)
  - Status badge (Completed)

### Access:
- URL: `/completed-sessions/`
- Role: Counselor only
- Navigation: Click "Completed Sessions" card on dashboard

### Empty State:
- Shows friendly message when no completed sessions exist
- Icon and helpful text

## Data Flow

### How Sessions Get Completed:

1. **Counselor evaluates case** → Creates CounselingSchedule
2. **Session is scheduled** → Status: 'scheduled'
3. **Counselor marks as complete** → Status: 'completed'
4. **Appears in Completed Sessions** → Count updates on dashboard

### How VPF Gets Completed:

1. **Counselor assigns to VPF** → Creates VPFCase (assigned_by=counselor)
2. **ESP Teacher works on case** → Status: 'ongoing'
3. **ESP Teacher completes** → Status: 'completed'
4. **Counts update** → Completed VPF increases

## Benefits

### Accurate Counts:
- ✅ PA and OSP counts reflect actual incident types
- ✅ Scheduled sessions from correct source
- ✅ Completed sessions properly tracked
- ✅ VPF referrals show counselor's assignments

### Better Navigation:
- ✅ Scheduled Sessions → Counseling Schedule
- ✅ Completed Sessions → Dedicated completed page
- ✅ Clear, intuitive links
- ✅ No confusion about where to go

### Improved Workflow:
- ✅ Easy to see completed work
- ✅ Track counseling progress
- ✅ Monitor VPF assignments
- ✅ Better oversight of cases

## Testing Checklist

- [x] Total PA counts correctly
- [x] Total OSP counts correctly
- [x] Scheduled Sessions counts from CounselingSchedule
- [x] Scheduled Sessions link goes to counselor_schedule
- [x] Completed Sessions counts from CounselingSchedule
- [x] Completed Sessions link goes to completed_sessions
- [x] Completed Sessions page displays correctly
- [x] Completed VPF counts all completed VPF cases
- [x] Total VPF Referrals counts counselor's assignments
- [x] All links work correctly
- [x] Dashboard loads without errors
- [x] Server reloaded successfully

## Database Queries

### Optimized Queries:
All queries use proper filtering and are efficient:

```python
# PA Count
IncidentReport.objects.filter(incident_type__severity='prohibited').count()

# OSP Count
IncidentReport.objects.filter(incident_type__severity='school_policy').count()

# Scheduled Sessions
CounselingSchedule.objects.filter(counselor=user, status='scheduled').count()

# Completed Sessions
CounselingSchedule.objects.filter(counselor=user, status='completed').count()

# Completed VPF
VPFCase.objects.filter(status='completed').count()

# VPF Referrals by Counselor
VPFCase.objects.filter(assigned_by=user).count()
```

## Future Enhancements (Optional)

### Analytics:
- Add completion rate percentage
- Show average session duration
- Track VPF success rates
- Generate monthly reports

### Filtering:
- Filter completed sessions by date range
- Filter by student grade level
- Search by student name
- Export to Excel

### Notifications:
- Alert when session is completed
- Remind about upcoming sessions
- Notify when VPF is completed

## Notes

- All counts are now accurate and based on correct data sources
- Navigation is intuitive and goes to the right pages
- Completed sessions have their own dedicated page
- VPF referrals show only what the counselor assigned
- Dashboard provides clear overview of counselor's work

## Support

For questions about the Guidance Dashboard:
- Check this documentation
- Refer to main SIRMS documentation
- Contact system administrator
