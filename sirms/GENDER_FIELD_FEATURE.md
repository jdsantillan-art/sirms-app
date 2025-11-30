# Gender Field Feature

## Overview
Added a gender dropdown field to incident reporting forms to record the gender of involved students.

## Implementation Date
November 28, 2025

## Changes Made

### 1. Database Model
**File**: `sirms/incidents/models.py`
- Added `student_gender` field to `IncidentReport` model
- Field type: CharField with choices (Male/Female)
- Optional field (blank=True)

```python
student_gender = models.CharField(max_length=10, choices=[
    ('male', 'Male'),
    ('female', 'Female')
], blank=True, help_text="Gender of the involved student")
```

### 2. Form
**File**: `sirms/incidents/forms.py`
- Added `student_gender` field to `IncidentReportForm`
- Dropdown with options: Select Gender, Male, Female
- Styled with green theme matching SIRMS design

### 3. Views
**Files**: 
- `sirms/incidents/views.py` - Updated `report_incident` view
- `sirms/incidents/direct_report_views.py` - Updated `direct_report` view

Both views now save the gender field:
```python
report.student_gender = form.cleaned_data.get('student_gender', '')
```

### 4. Templates
**Files**:
- `sirms/templates/report_incident.html`
- `sirms/templates/direct_report.html`

**Field Position**: 
- Located under "Middle Name" field
- Above "Involved Students" section
- In the Reporter Information column (left side)

### 5. Database Migration
**File**: `sirms/incidents/migrations/0022_incidentreport_student_gender.py`
- Migration created and applied successfully
- Adds `student_gender` column to `incidents_incidentreport` table

## Field Location in Form

```
Reporter Info Section:
├── First Name (required)
├── Last Name (required)
├── Middle Name (optional)
└── Gender (optional) ← NEW FIELD
    ├── Select Gender
    ├── Male
    └── Female

Involved Students Section:
└── Names or IDs
```

## Usage

### For Students and Teachers
When reporting an incident:
1. Fill in reporter information (first name, last name, middle name)
2. Select the gender of the involved student from the dropdown
3. Continue with the rest of the form

### For DO and Guidance (Direct Report)
When manually encoding a report:
1. Enter the reporter's information
2. Select the gender of the involved student
3. The gender will be recorded along with all other incident details

## Data Storage
- Gender is stored in the `student_gender` field of the `IncidentReport` model
- Appears in all reports views and detail pages
- Can be filtered and used for analytics

## Benefits
- ✅ Better demographic tracking
- ✅ Improved incident analytics
- ✅ Gender-specific reporting capabilities
- ✅ Compliance with data collection requirements
- ✅ Optional field - doesn't block report submission

## Display in Reports
The gender field will be visible in:
- All Reports view
- Report Detail page
- My Reports view
- Analytics and statistics
- Export functionality

## Technical Details

### Form Field Configuration
```python
student_gender = forms.ChoiceField(
    choices=[('', 'Select Gender'), ('male', 'Male'), ('female', 'Female')],
    required=False,
    widget=forms.Select(attrs={
        'class': 'w-full px-2.5 py-1.5 text-sm border-2 border-gray-200 rounded-xl focus:border-emerald-500 focus:ring-2 focus:ring-emerald-100 transition-all outline-none',
        'id': 'id_student_gender'
    })
)
```

### Styling
- Matches SIRMS green theme
- Rounded corners (rounded-xl)
- Focus states with emerald color
- Responsive design
- Consistent with other form fields

## Future Enhancements (Optional)
- Add "Prefer not to say" option
- Add "Other" option with text input
- Use gender data for analytics dashboards
- Generate gender-based incident reports
- Track gender patterns in violations

## Testing Checklist
- [x] Field appears in Report Incident form
- [x] Field appears in Direct Report form
- [x] Field is optional (form submits without it)
- [x] Gender value is saved to database
- [x] Gender appears in report details
- [x] Migration applied successfully
- [x] No errors on form submission
- [x] Dropdown styling matches theme

## Notes
- Field is optional to maintain flexibility
- Position chosen for logical flow (after personal info, before involved students)
- Uses simple Male/Female options as requested
- Can be expanded in the future if needed

## Support
For questions about this feature, refer to the main SIRMS documentation or contact the system administrator.
