# Dashboard Chart Troubleshooting Guide

## Issue
The data analytics charts are not showing on the dashboard.

## Possible Causes

### 1. No Data in Database
The most common reason charts don't show is because there's no data to display.

**Check:**
- Are there any incident reports in the database?
- Do the incident types have the correct severity values?

**Run the test script:**
```bash
python test_dashboard_data.py
```

This will show you:
- How many prohibited acts exist
- How many OSP (Other School Policies) exist
- What severity values are in the database

### 2. Chart.js Not Loading
If Chart.js library fails to load, charts won't render.

**Check browser console for:**
- `Chart.js failed to load` error message
- `Chart is not defined` error

**Fix:**
- Verify `static/js/chart.js` file exists
- Check browser network tab to see if chart.js loads successfully
- Clear browser cache and reload

### 3. JavaScript Errors
Any JavaScript error before chart creation will prevent charts from showing.

**Check browser console for:**
- Red error messages
- Look for the line: `✅ Dashboard charts loaded successfully`
- If you see: `Chart error:` followed by an error message

### 4. Template Syntax Issues
Django template variables might not be rendering correctly.

**Check:**
- View page source in browser
- Search for `counselorReportTypeChart`
- Verify the JavaScript shows actual numbers, not `{{ total_prohibited_acts }}`

## Debugging Steps

### Step 1: Check Browser Console
1. Open browser (Chrome/Firefox/Edge)
2. Press F12 to open Developer Tools
3. Go to Console tab
4. Reload the dashboard page
5. Look for any error messages

### Step 2: Verify Data Exists
Run the test script:
```bash
cd sirms
python test_dashboard_data.py
```

Expected output:
```
Testing with counselor: counselor1
Total Prohibited Acts: 15
Total OSP: 8
```

If you see zeros, you need to add data to the database.

### Step 3: Check Chart Canvas Element
In browser console, type:
```javascript
document.getElementById('counselorReportTypeChart')
```

Should return: `<canvas id="counselorReportTypeChart"></canvas>`

If it returns `null`, the HTML template isn't rendering correctly.

### Step 4: Verify Chart.js is Loaded
In browser console, type:
```javascript
typeof Chart
```

Should return: `"function"`

If it returns `"undefined"`, Chart.js didn't load.

### Step 5: Check Data Values
In browser console, look for the log message:
```
Creating counselor pie chart: 15 8
```

This shows the actual data being passed to the chart.

## Common Fixes

### Fix 1: Add Sample Data
If no data exists, create some incident reports:
1. Log in as a teacher or student
2. Create incident reports
3. Log in as DO and classify them
4. Assign severity levels to incident types

### Fix 2: Clear Browser Cache
```
Ctrl + Shift + Delete (Windows/Linux)
Cmd + Shift + Delete (Mac)
```
Select "Cached images and files" and clear.

### Fix 3: Verify Incident Type Severities
Check that IncidentType records have severity field set to either:
- `'prohibited'` for Prohibited Acts
- `'school_policy'` for Other School Policies

### Fix 4: Check User Role
Verify you're logged in as a counselor:
```python
# In Django shell
from incidents.models import CustomUser
user = CustomUser.objects.get(username='your_username')
print(user.role)  # Should be 'counselor'
```

## Expected Behavior

When working correctly:

1. **Dashboard loads** → You see analytics cards at top
2. **Chart section appears** → White card with title "Report Type Distribution"
3. **Pie chart renders** → Doughnut chart with two colored segments
4. **Legend shows** → "Prohibited Acts" (red) and "Other School Policies" (blue)
5. **Hover works** → Tooltips show exact numbers when hovering over segments

## Chart Configuration

The counselor pie chart shows:
- **Red segment**: Prohibited Acts count
- **Blue segment**: Other School Policies count
- **Legend**: At bottom of chart
- **Title**: "Prohibited Acts vs Other School Policies"

## Files to Check

1. **sirms/templates/dashboard.html**
   - Line ~590: Chart HTML canvas element
   - Line ~793: createCounselorCharts() function

2. **sirms/incidents/views.py**
   - Line ~200: Counselor dashboard context data
   - Variables: `total_prohibited_acts`, `total_osp`

3. **sirms/static/js/chart.js**
   - Chart.js library file

## Still Not Working?

If charts still don't show after trying all fixes:

1. **Check Django logs** for any server errors
2. **Verify database connection** is working
3. **Test with different browser** (Chrome, Firefox, Edge)
4. **Check file permissions** on static files
5. **Run Django collectstatic** if using production setup:
   ```bash
   python manage.py collectstatic
   ```

## Contact Information

If you need further assistance, provide:
- Browser console error messages (screenshot)
- Output from test_dashboard_data.py script
- Django version and database type
- Any recent changes made to the system
