# Clickable Behavior Concerns Counter Cards Feature

## Overview
Enhanced the DO Behavior Concerns page with clickable counter cards that filter cases and Excel export functionality for completed counseling sessions.

## Features Implemented

### 1. Clickable Counter Cards
The three counter cards (Total, Pending, Completed) are now interactive buttons that filter the case list:

- **Total Card (Blue)**: Shows all behavior concerns
- **Pending Card (Yellow)**: Shows only pending cases (status: classified)
- **Completed Card (Green)**: Shows only completed cases (status: resolved)

#### Visual Feedback
- Cards have hover effects (scale and shadow)
- Active filter is highlighted with colored border and background
- Filter badge shows current selection and count
- Smooth transitions for better UX

### 2. Excel Export for Completed Cases
When viewing completed cases, an "Export to Excel" button appears that generates a comprehensive report.

#### Export Includes:
- **Basic Information**: Case ID, Student Name, Gender, Grade, Section
- **Incident Details**: Type, Category, Date, Time, Description
- **Reporter Information**: Name and Role
- **Classification**: Severity level
- **Timeline**: Reported Date, Completed Date, Days to Complete
- **Appointments**: Count and detailed schedule information
- **Notes**: Final notes from counseling sessions
- **Summary**: Total count, export date, and exported by information

#### File Format
- Excel (.xlsx) format
- Professional styling with green header
- Auto-sized columns for readability
- Frozen header row for easy scrolling
- Wrapped text for long descriptions
- Filename: `SIRMS_Completed_Behavior_Concerns_YYYYMMDD_HHMMSS.xlsx`

## Technical Implementation

### Files Modified

1. **sirms/templates/do/behavior_concerns.html**
   - Converted static counter cards to clickable buttons
   - Added data-status attribute to table rows for filtering
   - Added export button (hidden by default)
   - Implemented JavaScript filtering logic
   - Added visual feedback for active filters

2. **sirms/incidents/export_views.py**
   - Added `export_behavior_concerns_excel()` function
   - Imports DOSchedule model for appointment details
   - Comprehensive data extraction and formatting
   - Professional Excel styling

3. **sirms/incidents/urls.py**
   - Added route: `export-behavior-concerns-excel/`

## Usage

### For DO Users

1. **Navigate** to Behavior Concerns page
2. **Click** on any counter card to filter:
   - Click "Total" to see all cases
   - Click "Pending" to see only pending cases
   - Click "Completed" to see only completed cases

3. **Export Completed Cases**:
   - Click the "Completed" card
   - Click "Export to Excel" button (appears in header)
   - Excel file downloads automatically

### Filter Behavior
- Only one filter active at a time
- Empty state shown if no cases match filter
- Table automatically hides/shows based on results
- Export button only visible for completed cases

## Benefits

### For DO Staff
- **Quick Filtering**: Instantly view cases by status
- **Better Organization**: Focus on specific case types
- **Comprehensive Reports**: All data needed for documentation
- **Professional Output**: Ready for presentations and records

### For Administration
- **Data Analysis**: Complete case history with timelines
- **Accountability**: Track appointment schedules and completion times
- **Documentation**: Proper records for audits and reviews
- **Efficiency**: No manual data compilation needed

## Security
- Only DO role can access behavior concerns page
- Only DO role can export Excel reports
- Export includes user attribution (who exported)
- Timestamp on all exports for audit trail

## Future Enhancements
- Date range filtering for exports
- Additional export formats (PDF, CSV)
- Bulk actions on filtered cases
- Print-friendly view for filtered results
- Statistics dashboard for completed cases

## Testing Checklist
- [ ] Click Total card - shows all cases
- [ ] Click Pending card - shows only pending cases
- [ ] Click Completed card - shows only completed cases
- [ ] Export button appears only for completed filter
- [ ] Excel export downloads successfully
- [ ] Excel file contains all required data
- [ ] Excel formatting is professional
- [ ] Empty state shows when no cases match filter
- [ ] Visual feedback works (borders, backgrounds)
- [ ] Non-DO users cannot access export URL

## Notes
- Filter state persists during page session
- Page initializes with "All" filter active
- Export includes appointment details from DOSchedule
- Completed cases are locked and cannot be edited
