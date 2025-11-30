# Behavioral Concerns Template Fix

## Issue
The Behavioral Concerns page was not showing the updated design because the view was rendering the wrong template.

## Problem
```python
# BEFORE (Wrong template)
return render(request, 'do/classify_violations.html', {
    ...
})
```

The `behavior_concerns` view was rendering `'do/classify_violations.html'` instead of `'do/behavior_concerns.html'`.

## Solution
```python
# AFTER (Correct template)
return render(request, 'do/behavior_concerns.html', {
    ...
})
```

Changed the template path to point to the correct file where all the updates were made.

## What This Fixes
✅ Compact statistics now display
✅ Table format now shows
✅ Schedule button now appears
✅ All UI optimizations now visible

## Files Modified
- `incidents/views.py` - Changed template path in `behavior_concerns` view

## Status
✅ **FIXED** - The updated Behavioral Concerns page should now display correctly with:
- Compact statistics
- Table format
- Schedule button
- All new features

## Testing
1. Refresh the Behavioral Concerns page
2. You should now see the compact table layout
3. Schedule button (📅) should appear for each case
4. Statistics should be in small compact cards

The changes are now live!
