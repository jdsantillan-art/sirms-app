# Automatic Repeat Offender Detection - Quick Guide

## What It Does
Automatically identifies students with multiple violations and displays warning badges.

## How It Works
1. Report created → Violation history created automatically
2. Evaluation created → Checks previous violations automatically
3. If violations exist → Marks as repeat offender automatically
4. Related cases linked automatically

## Visual Display
Red badge: `Juan Dela Cruz [REPEATED (3x)]`

## Deployment
```bash
deploy_auto_repeat_detection.bat
```

After Render deployment:
```bash
python manage.py detect_repeat_offenders
```

## Files Created
- `incidents/signals.py` - Auto-detection signals
- `incidents/repeat_offender_utils.py` - Utility functions
- `incidents/management/commands/detect_repeat_offenders.py` - Command

Status: Ready to Deploy
