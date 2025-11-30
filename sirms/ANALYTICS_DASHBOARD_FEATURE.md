# Analytics Dashboard Feature

## Overview
A comprehensive analytics dashboard has been implemented for DO, Counselor, and Principal roles with interactive charts and data visualization.

## Access
- **URL**: `/analytics/` or click "Analytics Dashboard" in the sidebar
- **Available for**: Discipline Officers, Guidance Counselors, and Principals

## Features

### 1. Role-Specific Metrics Cards

#### Discipline Officer (DO)
- Total Reports
- Pending Classification
- Classified Today
- Major Cases

#### Guidance Counselor
- Major Cases
- Scheduled Sessions
- Counseling Success Rate
- Pending Evaluations

#### Principal
- Total Cases This Year
- Resolution Rate
- Active Sanctions
- Repeat Offenders

### 2. Interactive Charts

#### For All Roles:
1. **Violation Trend Over Time** (Line Chart)
   - Shows monthly trend of incident reports over the past year
   - Smooth wave animation with gradient fill

2. **Violation Type Distribution** (Doughnut Chart)
   - Displays breakdown of different violation types
   - Color-coded for easy identification

3. **Grade Level Reports** (Bar Chart)
   - Shows which grade levels have the most reports
   - Grades 7-12 comparison

4. **Major vs Minor Offenses** (Stacked Bar Chart)
   - Monthly comparison of major and minor offenses
   - Stacked visualization for easy comparison

#### For Counselor & Principal Only:
5. **Resolution Progress** (Area Chart)
   - Tracks resolved vs pending cases over time
   - Dual-line area chart showing trends

### 3. Export Functionality
- Export reports in multiple formats:
  - PDF
  - Excel
  - CSV
- Click "Export Report" button in the top right

### 4. Auto-Refresh
- Dashboard data automatically refreshes every 60 seconds
- Ensures real-time data accuracy

## Technical Implementation

### Files Created/Modified:
1. **Template**: `sirms/templates/analytics_dashboard.html`
   - Full-featured analytics dashboard with Chart.js integration
   - Responsive design with Tailwind CSS
   - Role-based content rendering

2. **View**: `sirms/incidents/views.py`
   - Added `analytics_dashboard()` function
   - Generates chart data from database
   - Role-specific data aggregation

3. **URL**: `sirms/incidents/urls.py`
   - Added route: `path('analytics/', views.analytics_dashboard, name='analytics_dashboard')`

4. **Navigation**: `sirms/templates/base.html`
   - Added "Analytics Dashboard" link to sidebar for DO, Counselor, and Principal

### Data Sources:
- **IncidentReport** model for violation trends
- **Classification** model for severity breakdown
- **CounselingSession** model for counseling metrics
- **CounselingSchedule** model for scheduled sessions
- **Sanction** model for active sanctions
- **CaseEvaluation** model for repeat offenders

### Chart Library:
- **Chart.js** (v4.x) via CDN
- Responsive and interactive charts
- Smooth animations and transitions

## Usage Instructions

### For Discipline Officers:
1. Navigate to Dashboard → Analytics Dashboard
2. View total reports and pending classifications
3. Monitor major vs minor case trends
4. Track grade-level violation patterns
5. Export data for reporting

### For Guidance Counselors:
1. Access Analytics Dashboard from sidebar
2. Monitor major cases requiring attention
3. Track counseling session success rates
4. View resolution progress over time
5. Identify trends for intervention planning

### For Principals:
1. Open Analytics Dashboard for school-wide overview
2. Review resolution rates and active sanctions
3. Monitor repeat offenders
4. Track overall incident trends
5. Export comprehensive reports for stakeholders

## Data Visualization Details

### Color Scheme:
- Primary Green: `#2E8B57` (SeaGreen)
- Light Green: `#3CB371` (MediumSeaGreen)
- Accent Colors: Teal, Lime, DarkGreen variations

### Chart Configurations:
- All charts are responsive and maintain aspect ratio
- Smooth animations on load (0.6s fade-in)
- Interactive tooltips on hover
- Legend positioning optimized for readability

### Performance:
- Efficient database queries with date range filtering
- JSON serialization for chart data
- Minimal page load time
- Optimized for 12 months of historical data

## Future Enhancements (Potential):
- [ ] Custom date range selection
- [ ] Drill-down functionality for detailed views
- [ ] Comparison between time periods
- [ ] Predictive analytics using ML
- [ ] Real-time notifications for anomalies
- [ ] Dashboard customization per user
- [ ] Mobile-optimized charts

## Testing Checklist:
- [x] DO can access analytics dashboard
- [x] Counselor can access analytics dashboard
- [x] Principal can access analytics dashboard
- [x] Charts render correctly with real data
- [x] Export modal opens and closes
- [x] Responsive design works on different screen sizes
- [x] Role-specific metrics display correctly
- [x] Navigation link appears in sidebar

## Notes:
- The dashboard uses the same data aggregation logic as the main dashboard
- Charts are generated client-side using Chart.js for better performance
- All data is filtered based on user role and permissions
- Export functionality requires backend API endpoints (already implemented)

## Support:
For issues or questions about the analytics dashboard, check:
1. Browser console for JavaScript errors
2. Django server logs for backend errors
3. Ensure Chart.js CDN is accessible
4. Verify user has appropriate role permissions
