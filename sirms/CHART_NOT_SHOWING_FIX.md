# Chart Not Showing - Quick Fix Guide

## The Problem
The data analytics charts on the dashboard are not displaying.

## Most Likely Cause
**No data in the database** - The charts need data to display. If there are zero prohibited acts and zero OSP reports, the chart will appear empty or not render.

## Quick Test

### Step 1: Open Browser Console
1. Press **F12** on your keyboard
2. Click the **Console** tab
3. Reload the dashboard page
4. Look for these messages:

**Good signs:**
```
Creating counselor pie chart: 15 8
✅ Dashboard charts loaded successfully
```

**Bad signs:**
```
Creating counselor pie chart: 0 0
❌ Chart.js failed to load
Chart error: ...
```

### Step 2: Check if Data Exists
Run this command in your terminal:
```bash
cd sirms
python test_dashboard_data.py
```

**If you see zeros:**
```
Total Prohibited Acts: 0
Total OSP: 0
⚠️  WARNING: Both counts are 0!
```

This means you need to add data to the database first.

## Solution: Add Sample Data

### Option 1: Create Incident Reports Manually
1. Log in as a **Teacher** or **Student**
2. Go to "Report Incident"
3. Create several incident reports
4. Log in as **Discipline Officer (DO)**
5. Classify the reports
6. Make sure incident types have severity set to:
   - `prohibited` for Prohibited Acts
   - `school_policy` for Other School Policies

### Option 2: Use Django Shell to Add Data
```python
python manage.py shell

from incidents.models import IncidentReport, IncidentType, CustomUser

# Create or get incident types
prohibited_type, _ = IncidentType.objects.get_or_create(
    name="Fighting",
    defaults={'severity': 'prohibited', 'description': 'Physical altercation'}
)

osp_type, _ = IncidentType.objects.get_or_create(
    name="Dress Code Violation",
    defaults={'severity': 'school_policy', 'description': 'Uniform violation'}
)

# Get a reporter (teacher/student)
reporter = CustomUser.objects.filter(role='teacher').first()

# Create sample reports
if reporter:
    IncidentReport.objects.create(
        reporter=reporter,
        incident_type=prohibited_type,
        description="Sample prohibited act",
        incident_date="2024-01-15",
        incident_time="10:00:00"
    )
    
    IncidentReport.objects.create(
        reporter=reporter,
        incident_type=osp_type,
        description="Sample OSP violation",
        incident_date="2024-01-16",
        incident_time="11:00:00"
    )

print("Sample data created!")
```

### Option 3: Check Existing Data Severity
If you have incident reports but charts still don't show, check the severity values:

```python
python manage.py shell

from incidents.models import IncidentType

# Check what severities exist
for it in IncidentType.objects.all():
    print(f"{it.name}: severity='{it.severity}'")

# Update severities if needed
IncidentType.objects.filter(name="Fighting").update(severity='prohibited')
IncidentType.objects.filter(name="Uniform Violation").update(severity='school_policy')
```

## Verify the Fix

After adding data:

1. **Reload the dashboard** (Ctrl+F5 or Cmd+Shift+R)
2. **Check browser console** - should see:
   ```
   Creating counselor pie chart: 5 3
   ✅ Dashboard charts loaded successfully
   ```
3. **See the chart** - A doughnut chart with red and blue segments should appear

## Chart Should Look Like This

```
┌─────────────────────────────────────┐
│  Prohibited Acts vs OSP             │
│                                     │
│         ╭─────╮                     │
│       ╱         ╲                   │
│      │    🔴     │                  │
│      │  ⚪  🔵   │                  │
│       ╲         ╱                   │
│         ╰─────╯                     │
│                                     │
│  🔴 Prohibited Acts                 │
│  🔵 Other School Policies           │
└─────────────────────────────────────┘
```

## Still Not Working?

### Check 1: Chart.js Library
Verify the file exists:
```bash
ls sirms/static/js/chart.js
```

If missing, download Chart.js from https://www.chartjs.org/

### Check 2: User Role
Make sure you're logged in as a **Counselor**:
```python
python manage.py shell

from incidents.models import CustomUser
user = CustomUser.objects.get(username='YOUR_USERNAME')
print(f"Role: {user.role}")  # Should be 'counselor'
```

### Check 3: Template Rendering
View page source (Ctrl+U) and search for `counselorReportTypeChart`. You should see:
```javascript
const prohibitedActs = 15;  // Actual number, not {{ template_var }}
const otherSchoolPolicies = 8;
```

## Summary

**90% of the time**, charts don't show because there's no data in the database. 

**Quick fix:**
1. Add some incident reports
2. Make sure incident types have correct severity values
3. Reload the dashboard
4. Charts should appear!

## Need More Help?

See the full troubleshooting guide: `DASHBOARD_CHART_TROUBLESHOOTING.md`
