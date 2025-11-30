# Data Analytics Implementation Plan

## Backup Status
✅ **Backup Created**: `templates/dashboard_backup_working.html`

## Analytics Requirements

### DO Dashboard Analytics
1. **Trend Cases** (Wave/Line Graph) - Monthly trend of cases
2. **Grade Most Reported** (Bar Graph) - Which grade has most reports
3. **Month Most Reports** (Line Graph) - Which month has most reports
4. **Filter**: Yearly, Monthly, Quarterly

### Guidance Counselor Dashboard Analytics
1. **Trend Cases** (Wave/Line Graph) - Monthly trend of counseling cases
2. **Grade Most Reported** (Bar Graph) - Which grade needs most counseling
3. **Month Most Reports** (Line Graph) - Peak counseling months
4. **Filter**: Yearly, Monthly, Quarterly

### ESP Teacher Dashboard Analytics
1. **Status Distribution** (Donut Chart) - Completed, Pending, Ongoing VPF cases
2. **Most Incidents Referred** (Wave/Line Graph) - Trend of VPF referrals
3. **Filter**: Yearly, Monthly, Quarterly

## Implementation Steps

### Step 1: Backend Data Preparation (views.py)
- Add filter parameter handling (yearly/monthly/quarterly)
- Calculate trend data for each time period
- Calculate grade distribution
- Calculate monthly distribution
- Calculate VPF status counts

### Step 2: Frontend Chart Implementation
- Use Chart.js (already loaded)
- Create responsive chart containers
- Implement filter dropdown
- Connect filter to data refresh

### Step 3: Chart Specifications

#### Line/Wave Chart (Trend)
```javascript
{
  type: 'line',
  data: {
    labels: ['Jan', 'Feb', 'Mar', ...],
    datasets: [{
      label: 'Cases',
      data: [10, 15, 8, ...],
      borderColor: 'rgb(16, 185, 129)',
      backgroundColor: 'rgba(16, 185, 129, 0.1)',
      tension: 0.4,
      fill: true
    }]
  }
}
```

#### Bar Chart (Grade Distribution)
```javascript
{
  type: 'bar',
  data: {
    labels: ['Grade 7', 'Grade 8', ...],
    datasets: [{
      label: 'Reports',
      data: [5, 8, 3, ...],
      backgroundColor: 'rgba(16, 185, 129, 0.8)'
    }]
  }
}
```

#### Donut Chart (Status)
```javascript
{
  type: 'doughnut',
  data: {
    labels: ['Completed', 'Pending', 'Ongoing'],
    datasets: [{
      data: [45, 20, 15],
      backgroundColor: [
        'rgba(34, 197, 94, 0.8)',
        'rgba(251, 146, 60, 0.8)',
        'rgba(59, 130, 246, 0.8)'
      ]
    }]
  }
}
```

## Next Steps
1. Update views.py to provide chart data
2. Add chart containers to dashboard.html
3. Implement Chart.js rendering
4. Add filter functionality
5. Test with real data
