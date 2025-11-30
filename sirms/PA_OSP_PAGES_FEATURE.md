# Prohibited Acts & Other School Policies Pages

## Overview
Created dedicated pages for Prohibited Acts (PA) and Other School Policies (OSP) that show only incidents of each specific type. The dashboard cards now link to these filtered pages instead of the general major case review.

## Implementation Date
November 28, 2025

## Features

### 1. Prohibited Acts Page
**URL**: `/prohibited-acts/`

**Shows**:
- All incidents with `incident_type__severity='prohibited'`
- Only Prohibited Acts violations
- Filtered list of PA reports

**Statistics**:
- Total PA count
- Pending PA
- Classified PA
- Resolved PA

**Access**: Counselor, DO, Principal

### 2. Other School Policies Page
**URL**: `/other-school-policies/`

**Shows**:
- All incidents with `incident_type__severity='school_policy'`
- Only Other School Policies violations
- Filtered list of OSP reports

**Statistics**:
- Total OSP count
- Pending OSP
- Classified OSP
- Resolved OSP

**Access**: Counselor, DO, Principal

## Dashboard Integration

### Counselor Dashboard Cards

**Before**:
- Total Prohibited Acts → Went to Major Case Review
- Total OSP → Went to Major Case Review

**After**:
- Total Prohibited Acts → Goes to Prohibited Acts page ✅
- Total OSP → Goes to Other School Policies page ✅

### Updated Links:
```html
<!-- Prohibited Acts Card -->
<a href="{% url 'prohibited_acts' %}">
    Total Prohibited Acts: {{ total_prohibited_acts }}
    Click to view PA reports
</a>

<!-- OSP Card -->
<a href="{% url 'other_school_policies' %}">
    Total OSP: {{ total_osp }}
    Click to view OSP reports
</a>
```

## Page Features

### Reports Table
Displays:
- Case ID (clickable to report detail)
- Student Name
- Incident Type (specific violation)
- Grade/Section
- Status (with color badges)
- Date
- View button

### Search & Filters
- **Search**: By case ID or student name
- **Status Filter**: All, Pending, Under Review, Classified, Evaluated, Sanctioned, Resolved, Closed
- **Grade Filter**: All grades, 7-12

### Statistics Cards
Four cards showing:
1. Total count (Red for PA, Blue for OSP)
2. Pending count (Yellow)
3. Classified count (Purple)
4. Resolved count (Green)

### Navigation
- Back button to return to dashboard
- Breadcrumb-style navigation
- Clear page title indicating PA or OSP

## Files Created/Modified

### New Files:
1. **sirms/incidents/incident_type_views.py**
   - `prohibited_acts()` view
   - `other_school_policies()` view

2. **sirms/templates/counselor/incident_type_list.html**
   - Shared template for both PA and OSP
   - Dynamic content based on page_type

3. **sirms/PA_OSP_PAGES_FEATURE.md**
   - This documentation

### Modified Files:
1. **sirms/incidents/urls.py**
   - Added `prohibited-acts/` route
   - Added `other-school-policies/` route

2. **sirms/templates/dashboard.html**
   - Updated PA card link
   - Updated OSP card link
   - Changed button text to clarify destination

## Technical Implementation

### View Logic
```python
@login_required
def prohibited_acts(request):
    # Permission check
    if request.user.role not in ['counselor', 'do', 'principal']:
        return redirect('dashboard')
    
    # Get PA reports only
    reports = IncidentReport.objects.filter(
        incident_type__severity='prohibited'
    ).select_related(
        'incident_type', 'reported_student', 'reporter', 'classification'
    ).order_by('-created_at')
    
    # Calculate statistics
    # Render template
```

### Template Reusability
Single template handles both PA and OSP:
- `page_title`: "Prohibited Acts" or "Other School Policies"
- `page_type`: "PA" or "OSP"
- Dynamic colors based on type
- Dynamic icons based on type

### Query Optimization
Uses `select_related()` for efficient database queries:
- Fetches related incident_type
- Fetches related reported_student
- Fetches related reporter
- Fetches related classification
- Single query instead of N+1

## Benefits

### Clear Separation
- ✅ PA and OSP are now separate
- ✅ Easy to see only what you need
- ✅ No confusion with mixed reports
- ✅ Focused view for each type

### Better Navigation
- ✅ Direct access from dashboard
- ✅ Clear indication of destination
- ✅ Intuitive user flow
- ✅ Back button to return

### Improved Workflow
- ✅ Counselors can focus on specific types
- ✅ Easier to track PA vs OSP
- ✅ Better reporting and analysis
- ✅ Clearer statistics

### Consistent Design
- ✅ Matches SIRMS theme
- ✅ Same layout as other list pages
- ✅ Familiar interface
- ✅ Professional appearance

## Use Cases

### For Counselors:
1. Click "Total Prohibited Acts" on dashboard
2. See all PA incidents
3. Filter by status or grade
4. Click to view specific report
5. Take appropriate action

### For Analysis:
1. View PA trends separately from OSP
2. Compare PA vs OSP counts
3. Track resolution rates by type
4. Generate type-specific reports

### For Compliance:
1. Separate tracking of serious violations (PA)
2. Monitor policy violations (OSP)
3. Report to administration
4. Document incident patterns

## Color Coding

### Prohibited Acts (PA):
- **Primary Color**: Red (#DC2626)
- **Background**: Red gradient (from-red-50 to-red-100)
- **Border**: Red (border-red-500)
- **Icon**: Ban icon (fa-ban)

### Other School Policies (OSP):
- **Primary Color**: Blue (#2563EB)
- **Background**: Blue gradient (from-blue-50 to-blue-100)
- **Border**: Blue (border-blue-500)
- **Icon**: Clipboard list (fa-clipboard-list)

## Status Badges

Consistent across both pages:
- **Pending**: Yellow
- **Under Review**: Orange
- **Classified**: Purple
- **Evaluated**: Blue
- **Sanctioned**: Red
- **Resolved**: Green
- **Closed**: Gray

## Empty States

### No PA Reports:
- Ban icon in gray
- "No Prohibited Acts Reports"
- "No prohibited acts incidents have been reported yet."

### No OSP Reports:
- Clipboard icon in gray
- "No Other School Policies Reports"
- "No other school policies incidents have been reported yet."

## Future Enhancements (Optional)

### Export:
- Export PA reports to Excel
- Export OSP reports to Excel
- Separate exports for each type

### Analytics:
- PA vs OSP comparison charts
- Trend analysis by type
- Grade-level breakdown
- Monthly statistics

### Filtering:
- Date range filter
- Incident type sub-categories
- Reporter role filter
- Classification filter

## Testing Checklist

- [x] PA page loads correctly
- [x] OSP page loads correctly
- [x] PA card links to PA page
- [x] OSP card links to OSP page
- [x] Counts are accurate
- [x] Search works
- [x] Filters work
- [x] View button works
- [x] Back button works
- [x] Statistics display correctly
- [x] Empty states show properly
- [x] Permission checks work
- [x] Server running without errors

## URLs Summary

| Page | URL | Access |
|------|-----|--------|
| Prohibited Acts | `/prohibited-acts/` | Counselor, DO, Principal |
| Other School Policies | `/other-school-policies/` | Counselor, DO, Principal |

## Navigation Flow

```
Dashboard
    ↓
Click "Total Prohibited Acts"
    ↓
Prohibited Acts Page
    ↓
View specific report
    ↓
Report Detail

Dashboard
    ↓
Click "Total OSP"
    ↓
Other School Policies Page
    ↓
View specific report
    ↓
Report Detail
```

## Notes

- Both pages use the same template for consistency
- Filtering is done at the database level for performance
- Statistics are calculated in real-time
- No caching implemented (can be added if needed)
- Pages are mobile responsive

## Support

For questions about PA/OSP pages:
- Check this documentation
- Refer to main SIRMS documentation
- Contact system administrator
