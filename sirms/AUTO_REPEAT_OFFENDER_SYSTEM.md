# Automatic Repeat Offender Detection System

## Overview
The system now automatically identifies and marks repeat offenders without manual intervention.

## How It Works

### Signal-Based Detection
1. **When Report Created** - Creates violation history automatically
2. **When Evaluation Created** - Detects previous violations and marks repeat offender
3. **After Evaluation Saved** - Links related cases automatically
4. **When Any Report Created** - Updates all existing evaluations for that student

## Detection Logic
```python
previous_violations = IncidentReport.objects.filter(
    reported_student=student,
    created_at__lt=current_report.created_at
).count()

is_repeat_offender = previous_violations > 0
```

## Management Command
```bash
# Preview changes
python manage.py detect_repeat_offenders --dry-run

# Apply changes to existing data
python manage.py detect_repeat_offenders
```

## New Files
1. `incidents/signals.py` - Automatic detection signals
2. `incidents/repeat_offender_utils.py` - Utility functions
3. `incidents/management/commands/detect_repeat_offenders.py` - Retroactive detection

## Benefits
- No manual tracking needed
- Instant alerts for repeat offenders
- Complete violation history automatically linked
- Real-time statistics

## Deployment
1. Push changes to GitHub
2. Wait for Render deployment
3. Run: `python manage.py detect_repeat_offenders`
4. Verify badges appear on All Reports page

---
**Status:** Ready for Deployment
**Date:** December 9, 2025
