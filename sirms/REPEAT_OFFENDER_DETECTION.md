# Automatic Repeat Offender Detection

## ✅ What Was Added

### Feature: Automatic Detection of Repeat Offenders
The system now automatically detects and displays when a student has violated school policies multiple times, showing:
- **"REPEATED" badge** - Red warning badge
- **Violation count** - Number of previous violations (e.g., "2x", "3x")

## 🎯 How It Works

### Detection Logic:
For each incident report, the system:
1. Checks if the student has a previous violation history
2. Counts all previous reports for that student
3. Displays a warning badge if count > 0

### Formula:
```python
repeat_count = Previous reports for this student
is_repeat_offender = repeat_count > 0
```

## 📍 Where It Appears

### 1. All Reports Table
**Location:** `/all-reports/`

**Display:**
```
Student Name                    | Reporter Role | Incident
Juan Dela Cruz [🔴 REPEATED (2x)] | 🎓 Student   | Bullying
```

**Badge Style:**
- Red background (`bg-red-100`)
- Red text (`text-red-800`)
- Red border (`border-red-300`)
- Warning icon (⚠️)
- Shows count: "REPEATED (2x)"

### 2. Report Detail Page
**Location:** `/report/<case_id>/`

**Display:**
```
Involved Students:
Juan Dela Cruz, Maria Santos
[🔴 REPEATED OFFENDER (2x previous)]
```

**Badge Style:**
- Same red styling as All Reports
- Shows "REPEATED OFFENDER (Xx previous)"
- Positioned next to student names

## 🔢 Count Examples

| Previous Violations | Badge Display |
|---------------------|---------------|
| 0 | No badge |
| 1 | REPEATED (1x) |
| 2 | REPEATED (2x) |
| 3 | REPEATED (3x) |
| 5+ | REPEATED (5x) |

## 📊 Use Cases

### Scenario 1: First-Time Offender
- **Student:** Juan Cruz
- **Previous violations:** 0
- **Display:** Juan Cruz (no badge)
- **Action:** Normal processing

### Scenario 2: Second Offense
- **Student:** Maria Santos
- **Previous violations:** 1
- **Display:** Maria Santos [🔴 REPEATED (1x)]
- **Action:** DO/Counselor alerted to pattern

### Scenario 3: Chronic Offender
- **Student:** Pedro Reyes
- **Previous violations:** 5
- **Display:** Pedro Reyes [🔴 REPEATED (5x)]
- **Action:** Immediate attention, possible intervention

## 🎨 Visual Design

### Badge Components:
```html
<span class="inline-flex items-center px-2 py-0.5 text-xs font-bold rounded-full 
      bg-red-100 text-red-800 border border-red-300">
    <i class="fas fa-exclamation-triangle mr-1"></i>
    REPEATED (2x)
</span>
```

### Colors:
- **Background:** Light red (`#FEE2E2`)
- **Text:** Dark red (`#991B1B`)
- **Border:** Medium red (`#FCA5A5`)
- **Icon:** Warning triangle (⚠️)

## 🔍 Detection Details

### What Counts as a Previous Violation:
- ✅ Any incident report where student is `reported_student`
- ✅ Reports created before the current report
- ✅ All statuses (pending, resolved, closed, etc.)
- ✅ All severity levels (minor and major)

### What Doesn't Count:
- ❌ Current report itself
- ❌ Reports where student is only mentioned in text
- ❌ Reports created after current report
- ❌ Deleted or archived reports

### Query Logic:
```python
repeat_count = IncidentReport.objects.filter(
    reported_student=report.reported_student,
    created_at__lt=report.created_at  # Only previous reports
).count()
```

## 💡 Benefits

### For Discipline Officers:
1. **Quick Identification** - Instantly see repeat offenders
2. **Pattern Recognition** - Identify students needing intervention
3. **Prioritization** - Focus on chronic cases
4. **Documentation** - Clear violation history

### For Counselors:
1. **Early Intervention** - Catch patterns early
2. **Targeted Support** - Provide appropriate counseling
3. **Progress Tracking** - Monitor improvement over time
4. **Risk Assessment** - Identify high-risk students

### For Administrators:
1. **Data-Driven Decisions** - Make informed policy decisions
2. **Resource Allocation** - Direct resources to repeat offenders
3. **Trend Analysis** - Identify school-wide patterns
4. **Accountability** - Track intervention effectiveness

## 📈 Statistics Impact

### Dashboard Metrics (Future Enhancement):
- Total repeat offenders
- Average violations per student
- Repeat offense rate
- Intervention success rate

### Reporting (Future Enhancement):
- Monthly repeat offender report
- Student-specific violation history
- Grade-level repeat offense trends
- Incident type recurrence patterns

## 🚀 Deployment

Changes pushed to GitHub and deploying to Render:
- Build time: ~4-6 minutes
- Deploy time: ~4-6 minutes
- Total: ~10-15 minutes

## 📝 Technical Details

**Modified Files:**
- `incidents/views.py` - Added repeat detection logic
- `templates/all_reports.html` - Added badge display
- `templates/report_detail.html` - Added badge display

**Database Queries:**
- No new tables required
- Uses existing `IncidentReport` model
- Efficient query with `created_at__lt` filter

**Performance:**
- Minimal impact (simple count query)
- Cached per report in view
- No N+1 query issues

## 🔮 Future Enhancements

Possible improvements:
1. **Severity-Based Detection** - Different badges for minor vs major repeats
2. **Time-Based Detection** - Flag recent repeats (e.g., within 30 days)
3. **Incident Type Patterns** - Detect specific violation patterns
4. **Automatic Escalation** - Auto-escalate chronic offenders
5. **Parent Notifications** - Alert parents of repeat violations
6. **Intervention Tracking** - Link to counseling/VPF programs
7. **Success Metrics** - Track reduction in repeat offenses

---

**Status:** ✅ Deployed
**Date:** December 2, 2025
**Impact:** All Reports & Report Detail pages
