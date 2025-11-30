# Dynamic Dashboard Analytics Feature

## Date: November 30, 2025

## Overview
Implemented dynamic time filter functionality for the main dashboard analytics, allowing users to switch between Monthly, Quarterly, and Yearly views with real-time chart updates.

## Features Implemented

### 1. Time Filter Dropdown
- **Location:** Top right of dashboard (DO, Counselor, ESP Teacher views)
- **Options:**
  - Monthly View (Last 12 months)
  - Quarterly View (Last 8 quarters)
  - Yearly View (Last 5 years)

### 2. Dynamic Data Loading
- **API Endpoint:** `/api/dashboard-analytics/`
- **Method:** GET
- **Parameters:** `filter` (monthly, quarterly, yearly)
- **Response:** JSON with updated chart data and metrics

### 3. Real-Time Chart Updates
- Charts update without page reload
- Smooth transition with loading state (opacity fade)
- Maintains chart styling and configuration
- Updates all relevant charts based on user role

## Technical Implementation

### Backend (views.py)

#### New API Endpoint: `get_dashboard_analytics()`
```python
@login_required
def get_dashboard_analytics(request):
    """API endpoint for dynamic dashboard analytics based on time filter"""
    time_filter = request.GET.get('filter', 'monthly')
    
    # Calculate date ranges
    - Monthly: Last 12 months (30-day periods)
    - Quarterly: Last 8 quarters (90-day periods)
    - Yearly: Last 5 years (365-day periods)
    
    # Returns:
    - trend_data: Time-series incident reports
    - grade_data: Reports by grade level
    - stacked_data: Major vs Minor offenses
    - metrics: Role-specific statistics
```

**Data Calculation:**
- Dynamically calculates periods based on filter
- Formats labels appropriately (Jan, Q1 2025, 2025)
- Filters data by date range
- Calculates role-specific metrics

### Frontend (dashboard.html)

#### JavaScript Functions

**1. initCharts()**
- Initializes Chart.js
- Creates initial charts
- Attaches event listener to time filter

**2. updateDashboardData(filter)**
- Fetches new data from API
- Shows loading state
- Updates charts with new data
- Updates metrics if provided

**3. updateCharts(data)**
- Updates existing chart instances
- Preserves chart configuration
- Smooth data transition

**4. createDashboardCharts()**
- Creates initial chart instances
- Stores global references
- Handles data parsing errors

#### Chart Instances (Global)
```javascript
let trendChartInstance = null;
let gradeChartInstance = null;
let monthChartInstance = null;
let statusChartInstance = null;
let referralChartInstance = null;
```

## Data Flow

```
User selects time filter
        ↓
JavaScript event listener triggered
        ↓
Fetch API call to /api/dashboard-analytics/?filter=X
        ↓
Backend calculates data for selected period
        ↓
JSON response with updated data
        ↓
JavaScript updates chart instances
        ↓
Charts re-render with new data
```

## Role-Specific Behavior

### Discipline Officer (DO)
**Charts Updated:**
- Case Trend Analysis
- Reports by Grade Level
- Monthly Distribution (Major vs Minor)

**Metrics Updated:**
- Total Reports
- Pending Classification
- Minor Cases Count
- Major Cases Count

### Guidance Counselor
**Charts Updated:**
- Case Trend Analysis
- Reports by Grade Level
- Monthly Distribution (Major vs Minor)

**Metrics Updated:**
- Prohibited Acts
- OSP Cases
- Scheduled Sessions
- Completed Sessions
- Resolution Data (if applicable)

### ESP Teacher
**Charts Updated:**
- VPF Status Distribution (Donut)
- Referral Trend Over Time

**Metrics Updated:**
- Total VPF Referrals
- Completed VPF
- Pending VPF
- Ongoing VPF

## Time Period Calculations

### Monthly View
- **Period:** Last 12 months
- **Interval:** 30 days
- **Label Format:** "Jan", "Feb", "Mar"
- **Use Case:** Recent trends and patterns

### Quarterly View
- **Period:** Last 8 quarters (2 years)
- **Interval:** 90 days
- **Label Format:** "Q1 2025", "Q2 2025"
- **Use Case:** Seasonal analysis

### Yearly View
- **Period:** Last 5 years
- **Interval:** 365 days
- **Label Format:** "2021", "2022", "2023"
- **Use Case:** Long-term trends

## API Response Format

```json
{
    "trend_data": [
        {"month": "Jan", "reports": 15},
        {"month": "Feb", "reports": 12}
    ],
    "grade_data": [
        {"grade": "Grade 7", "count": 5},
        {"grade": "Grade 8", "count": 8}
    ],
    "stacked_data": [
        {"month": "Jan", "major": 5, "minor": 10},
        {"month": "Feb", "major": 3, "minor": 9}
    ],
    "metrics": {
        "total_reports": 150,
        "pending": 25,
        "minor_cases_count": 80,
        "major_cases_count": 70
    }
}
```

## User Experience

### Before
- ❌ Static charts showing only one time period
- ❌ No way to view historical trends
- ❌ Limited analytical capabilities

### After
- ✅ Dynamic time filter with 3 options
- ✅ Real-time chart updates
- ✅ Smooth loading transitions
- ✅ Comprehensive historical analysis
- ✅ No page reload required

## Performance Optimizations

1. **Efficient Queries:** Date range filtering at database level
2. **Chart Reuse:** Updates existing instances instead of recreating
3. **Loading States:** Visual feedback during data fetch
4. **Error Handling:** Graceful fallback to sample data
5. **Caching:** Browser caches Chart.js library

## Browser Compatibility
- ✅ Chrome/Edge (Latest)
- ✅ Firefox (Latest)
- ✅ Safari (Latest)
- ✅ Mobile browsers

## Testing Checklist
- [x] Time filter dropdown displays correctly
- [x] Monthly view loads and displays data
- [x] Quarterly view loads and displays data
- [x] Yearly view loads and displays data
- [x] Charts update without page reload
- [x] Loading state shows during fetch
- [x] Error handling works properly
- [x] All role-specific views work
- [x] API endpoint returns correct data
- [x] Date calculations are accurate
- [x] Labels format correctly

## Files Modified
1. `sirms/incidents/views.py` - Added `get_dashboard_analytics()` function
2. `sirms/incidents/urls.py` - Added API route
3. `sirms/templates/dashboard.html` - Added dynamic update functionality

## Future Enhancements
- Add custom date range picker
- Export filtered data to Excel/PDF
- Add comparison between periods
- Include predictive analytics
- Add drill-down functionality
- Cache frequently accessed data
- Add real-time updates via WebSocket
- Include more granular filters (weekly, daily)

## Usage Instructions

### For Users
1. Navigate to dashboard (`/dashboard/`)
2. Locate the time filter dropdown (top right)
3. Select desired view:
   - **Monthly:** See last 12 months
   - **Quarterly:** See last 8 quarters
   - **Yearly:** See last 5 years
4. Charts update automatically
5. Analyze trends and patterns

### For Developers
```python
# To add new metrics to API response
def get_dashboard_analytics(request):
    # Add your metric calculation
    new_metric = YourModel.objects.filter(...).count()
    
    # Include in response
    metrics['new_metric'] = new_metric
```

```javascript
// To update charts with new data
function updateCharts(data) {
    if (yourChartInstance) {
        yourChartInstance.data.labels = data.your_data.map(d => d.label);
        yourChartInstance.data.datasets[0].data = data.your_data.map(d => d.value);
        yourChartInstance.update();
    }
}
```

---

**Status:** ✅ Complete and Functional
**Type:** Descriptive Analytics with Dynamic Time Filtering
**Impact:** Enhanced data analysis capabilities for all staff roles
