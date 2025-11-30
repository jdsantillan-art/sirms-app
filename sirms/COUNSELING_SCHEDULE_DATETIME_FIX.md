# Counseling Schedule DateTime Fix

## Issue
**Error**: `TypeError: can't compare offset-naive and offset-aware datetimes`

**Location**: `incidents/views.py`, line 2001, in `counselor_schedule` view

**Cause**: The scheduled date from the HTML datetime-local input was being parsed as a timezone-naive datetime, but Django's `timezone.now()` returns a timezone-aware datetime. Python cannot compare these two types directly.

## Solution

Added timezone awareness to the parsed datetime before any comparisons:

```python
# Parse the scheduled date and make it timezone-aware
from datetime import datetime
scheduled_date = datetime.fromisoformat(scheduled_date_str)

# Make the datetime timezone-aware if it's naive
if scheduled_date.tzinfo is None:
    scheduled_date = timezone.make_aware(scheduled_date)
```

## What This Does

1. **Parses the datetime string** from the form input
2. **Checks if it's timezone-naive** (no timezone info)
3. **Converts to timezone-aware** using Django's `timezone.make_aware()`
4. **Uses the project's default timezone** (from settings.py)

## Why This Works

- Django's `timezone.now()` returns an aware datetime in the project's timezone
- `timezone.make_aware()` converts naive datetime to aware using the same timezone
- Now both datetimes are aware and can be compared safely

## Affected Validations

This fix enables these validations to work correctly:

1. **Weekend Check**: Validates if the selected date is a weekend
2. **Past Date Check**: Ensures the scheduled date is in the future
3. **Conflict Check**: Checks for scheduling conflicts within a 1-hour window

## Testing

To verify the fix works:

1. Go to Counseling Schedule page
2. Try to schedule a session
3. The form should submit successfully without the TypeError
4. Validations should work:
   - Try scheduling in the past → Should show error
   - Try scheduling on weekend → Should show error
   - Try scheduling conflicting times → Should show error

## Related Files

- `incidents/views.py` - Fixed the `counselor_schedule` view
- No template changes needed
- No model changes needed

## Django Timezone Best Practices

For future reference:

1. **Always use timezone-aware datetimes** in Django
2. **Use `timezone.now()`** instead of `datetime.now()`
3. **Use `timezone.make_aware()`** when parsing user input
4. **Enable timezone support** in settings.py: `USE_TZ = True`

## Status

✅ **Fixed** - The counseling schedule feature now works correctly with proper timezone handling.
