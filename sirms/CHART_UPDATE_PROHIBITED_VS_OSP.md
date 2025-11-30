# Chart Update: Prohibited Acts vs. Other School Policies

## Date: November 30, 2025

## Overview
Updated the Monthly Distribution chart to show "Prohibited Acts vs. Other School Policies" instead of "Major vs. Minor" offenses, providing more meaningful categorization based on incident type severity.

## Changes Made

### 1. Backend Changes (views.py)

#### Dashboard Function
**Before:**
```python
major_count = IncidentReport.objects.filter(
    created_at__range=[month_start, month_end],
    classification__severity='major'
).count()

minor_count = IncidentReport.objects.filter(
    created_at__range=[month_start, month_end],
    classification__severity='minor'
).count()

stacked_data.append({
    'month': month_start.strftime('%b'),
    'major': major_count,
    'minor': minor_count
})
```

**After:**
```python
prohibited_count = IncidentReport.objects.filter(
    created_at__range=[month_start, month_end],
    incident_type__severity='prohibited'
).count()

school_policy_count = IncidentReport.objects.filter(
    created_at__range=[month_start, month_end],
    incident_type__severity='school_policy'
).count()

stacked_data.append({
    'month': month_start.strftime('%b'),
    'prohibited': prohibited_count,
    'school_policy': school_policy_count
})
```

#### API Endpoint (get_dashboard_analytics)
Same changes applied to the dynamic API endpoint for time filter functionality.

### 2. Frontend Changes (dashboard.html)

#### Chart Title
**Before:** "Monthly Distribution"
**After:** "Prohibited Acts vs. Other School Policies"

#### Chart Labels
**Before:**
- "Minor" (Yellow)
- "Major" (Purple)

**After:**
- "Other School Policies" (Yellow/Amber)
- "Prohibited Acts" (Red)

#### Chart Colors
- **Other School Policies:** `rgba(251, 191, 36, 0.8)` (Amber)
- **Prohibited Acts:** `rgba(239, 68, 68, 0.8)` (Red)

#### JavaScript Updates
```javascript
// Update function
monthChartInstance.data.datasets[0].data = data.stacked_data.map(d => d.school_policy);
monthChartInstance.data.datasets[1].data = data.stacked_data.map(d => d.prohibited);

// Initial chart creation
datasets: [{
    label: 'Other School Policies',
    data: stackedData.map(d => d.school_policy),
    backgroundColor: 'rgba(251, 191, 36, 0.8)',
    borderRadius: 4
}, {
    label: 'Prohibited Acts',
    data: stackedData.map(d => d.prohibited),
    backgroundColor: 'rgba(239, 68, 68, 0.8)',
    borderRadius: 4
}]
```

## Data Source Comparison

### Old Approach (Classification-based)
- **Source:** `classification__severity` field
- **Categories:** 
  - Major: Cases classified as major by DO
  - Minor: Cases classified as minor by DO
- **Issue:** Depends on manual classification by DO

### New Approach (Incident Type-based)
- **Source:** `incident_type__severity` field
- **Categories:**
  - Prohibited Acts: Violations of prohibited acts (RA 10533, DepEd Orders)
  - Other School Policies: Other school policy violations
- **Benefit:** Automatic categorization based on incident type definition

## Benefits

### 1. More Accurate Categorization
- Based on predefined incident type severity
- Consistent across all reports
- No dependency on manual classification

### 2. Better Alignment with Policy
- Directly reflects DepEd guidelines
- Clear distinction between prohibited acts and other policies
- Easier to track compliance

### 3. Improved Analytics
- More meaningful insights for administrators
- Better trend analysis
- Clearer reporting for stakeholders

### 4. Consistent with System Design
- Aligns with IncidentType model structure
- Matches PA/OSP categorization used elsewhere
- Consistent terminology across the system

## Visual Changes

### Chart Appearance
```
Before:
┌─────────────────────────────────┐
│  Monthly Distribution           │
├─────────────────────────────────┤
│  [Yellow] Minor                 │
│  [Purple] Major                 │
└─────────────────────────────────┘

After:
┌─────────────────────────────────┐
│  Prohibited Acts vs. OSP        │
├─────────────────────────────────┤
│  [Amber] Other School Policies  │
│  [Red] Prohibited Acts          │
└─────────────────────────────────┘
```

### Color Psychology
- **Red (Prohibited Acts):** Indicates serious violations requiring immediate attention
- **Amber (Other School Policies):** Indicates policy violations that need monitoring

## Database Query Changes

### Old Query
```python
IncidentReport.objects.filter(
    created_at__range=[start, end],
    classification__severity='major'  # Requires Classification model
)
```

### New Query
```python
IncidentReport.objects.filter(
    created_at__range=[start, end],
    incident_type__severity='prohibited'  # Uses IncidentType model
)
```

## Impact on Existing Data

### Data Migration
- No database migration required
- Existing data automatically categorized based on incident_type
- Historical data remains intact

### Backward Compatibility
- Classification model still exists for other purposes
- No breaking changes to other features
- API response structure updated but compatible

## Testing Checklist
- [x] Chart displays correct title
- [x] Chart shows correct data
- [x] Colors match new scheme
- [x] Legend labels are correct
- [x] Time filter updates work
- [x] API returns correct data structure
- [x] Sample data uses new structure
- [x] No console errors
- [x] Stacked chart displays properly

## Files Modified
1. `sirms/incidents/views.py` - Updated dashboard() and get_dashboard_analytics()
2. `sirms/templates/dashboard.html` - Updated chart title, labels, colors, and JavaScript

## Related Features
- Incident Type Management
- PA/OSP Classification
- Analytics Dashboard
- Time Filter Functionality

## Future Enhancements
- Add drill-down to see specific incident types
- Include percentage breakdown
- Add trend indicators (increasing/decreasing)
- Export chart data with new categories
- Add comparison with previous periods

---

**Status:** ✅ Complete and Functional
**Type:** Chart Enhancement
**Impact:** Improved data categorization and visualization
**Alignment:** Better compliance with DepEd guidelines
