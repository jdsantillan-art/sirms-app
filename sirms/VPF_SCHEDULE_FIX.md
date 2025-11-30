# VPF Schedule Error Fix

## Error Description
```
AttributeError at /vpf-schedule/
'str' object has no attribute 'strftime'
Exception Location: incidents/views.py, line 3474, in vpf_schedule
```

## Root Cause
The `scheduled_date` variable was being retrieved as a string from POST data:
```python
scheduled_date = request.POST.get('scheduled_date')
```

When creating the notification message, the code tried to call `.strftime()` on this string:
```python
message=f'...on {schedule.scheduled_date.strftime("%B %d, %Y at %I:%M %p")}...'
```

However, `schedule.scheduled_date` was still a string at this point, not a datetime object.

## Solution
Parse the datetime string explicitly before using it:

```python
from datetime import datetime

# Get the string from POST
scheduled_date_str = request.POST.get('scheduled_date')

# Parse it into a datetime object
try:
    scheduled_date = datetime.strptime(scheduled_date_str, '%Y-%m-%dT%H:%M')
except ValueError:
    # Try alternative format
    scheduled_date = datetime.strptime(scheduled_date_str, '%Y-%m-%d %H:%M:%S')

# Now use the datetime object
schedule = VPFSchedule.objects.create(
    scheduled_date=scheduled_date,
    ...
)

# And in the notification
message=f'...on {scheduled_date.strftime("%B %d, %Y at %I:%M %p")}...'
```

## Why This Works
1. **Explicit parsing** - We convert the string to a datetime object before using it
2. **Format handling** - We handle both HTML5 datetime-local format (`%Y-%m-%dT%H:%M`) and standard format
3. **Direct usage** - We use the parsed `scheduled_date` variable instead of relying on Django's auto-conversion

## Files Modified
- `sirms/incidents/views.py` (lines 3447-3476)

## Testing
After this fix:
1. ESP teachers can schedule VPF sessions without errors
2. The notification message displays the date correctly formatted
3. The schedule is saved properly to the database

## Status
✅ **Fixed** - Error resolved, datetime parsing now explicit and reliable
