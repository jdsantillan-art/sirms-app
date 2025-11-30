# Counseling Schedule Updates

## Changes Made

### 1. View Toggle Behavior
**Before**: Both calendar and list views were visible at the same time
**After**: Only one view is shown at a time
- Default view: **List View**
- Click "Calendar View" button → Shows only calendar
- Click "List View" button → Shows only list

### 2. Schedule Conflict Prevention
Added validation to prevent duplicate/conflicting schedules:

#### Client-Side Validation (JavaScript)
- Real-time conflict checking as user selects date/time
- Shows warning message if conflict detected
- Disables submit button when conflict exists
- Checks for schedules within 1-hour window for the same student

#### Server-Side Validation (Python)
- Double-checks all validations on form submission
- Prevents duplicate schedules for the same student
- Returns error message and redirects back to form

### 3. Weekend Blocking
**No scheduling allowed on weekends (Saturday & Sunday)**

#### Client-Side Validation
- Checks if selected date is weekend
- Shows warning: "Weekend scheduling is not allowed"
- Disables submit button
- Prevents form submission

#### Server-Side Validation
- Validates day of week (Monday-Friday only)
- Returns error message if weekend selected
- Redirects back to form with evaluation pre-selected

### 4. Additional Validations

#### Past Date Prevention
- Cannot schedule sessions in the past
- Minimum date/time set to current date/time
- Both client and server-side validation

#### Time Window Conflict Check
- Checks for existing schedules within ±1 hour
- Prevents scheduling conflicts
- Only checks active schedules (not completed/missed)

## Validation Rules Summary

| Validation | Client-Side | Server-Side | Error Message |
|------------|-------------|-------------|---------------|
| **Weekend** | ✅ Yes | ✅ Yes | "Weekend scheduling is not allowed. Please select a weekday." |
| **Past Date** | ✅ Yes | ✅ Yes | "Cannot schedule in the past. Please select a future date and time." |
| **Duplicate Schedule** | ✅ Yes | ✅ Yes | "Schedule conflict: [Student] already has a session scheduled within this time window." |
| **Time Window (±1 hour)** | ✅ Yes | ✅ Yes | Same as duplicate |

## User Experience Flow

### Scheduling a Session

1. **Select Date/Time**
   - Date picker opens
   - User selects date and time
   - System automatically checks:
     - ❌ Is it a weekend? → Show warning
     - ❌ Is it in the past? → Show warning
     - ❌ Does student have another session nearby? → Show warning

2. **Warning Display**
   - Red warning box appears below date field
   - Submit button becomes disabled and grayed out
   - User must select different date/time

3. **Valid Selection**
   - No warnings shown
   - Submit button enabled
   - User can proceed with scheduling

4. **Form Submission**
   - Server validates again (double-check)
   - If valid: Creates schedule, sends notifications
   - If invalid: Shows error message, redirects back

### View Switching

1. **Default View (List)**
   - Page loads with list view
   - Shows table of all sessions
   - "List View" button is blue (active)

2. **Switch to Calendar**
   - Click "Calendar View" button
   - List view hides
   - Calendar view shows
   - Button turns blue (active)

3. **Switch Back to List**
   - Click "List View" button
   - Calendar view hides
   - List view shows
   - Button turns blue (active)

## Technical Implementation

### JavaScript Functions Added

```javascript
checkScheduleConflict()
- Called when date/time changes
- Checks weekend, past date, and conflicts
- Shows/hides warning message
- Enables/disables submit button

validateSchedule(event)
- Called on form submission
- Final validation before sending to server
- Prevents submission if invalid
- Shows alert messages

showView(view)
- Updated to show only one view at a time
- Toggles visibility of calendar/list
- Updates button styles
```

### Python View Updates

```python
counselor_schedule(request)
- Added weekend validation (weekday >= 5)
- Added past date validation
- Added conflict checking (±1 hour window)
- Returns error messages with redirect
```

### Data Structure Updates

```javascript
schedules array now includes:
- studentId: For accurate conflict checking
- All other fields remain the same
```

## Testing Checklist

- [x] View toggle works (only one view at a time)
- [x] Default view is list
- [x] Weekend blocking (client-side)
- [x] Weekend blocking (server-side)
- [x] Past date blocking (client-side)
- [x] Past date blocking (server-side)
- [x] Conflict detection (client-side)
- [x] Conflict detection (server-side)
- [ ] Test with actual data
- [ ] Test error messages display correctly
- [ ] Test notifications still work
- [ ] Test calendar rendering with conflicts

## Benefits

1. **Prevents Double-Booking**: Students can't have overlapping sessions
2. **Professional Scheduling**: No weekend sessions
3. **Better UX**: Real-time validation feedback
4. **Data Integrity**: Server-side validation ensures no bypassing
5. **Cleaner Interface**: One view at a time reduces clutter

## Notes

- Conflict window is set to ±1 hour (can be adjusted if needed)
- Only checks active schedules (scheduled/rescheduled status)
- Completed and missed sessions don't block new schedules
- Weekend check uses JavaScript `getDay()` (0=Sunday, 6=Saturday)
- Server-side uses Python `weekday()` (5=Saturday, 6=Sunday)
