# Automatic Repeat Offender Detection System

## ✅ Feature Overview

The system now **automatically identifies and flags students who have violated school policies multiple times**. This helps Discipline Officers and Guidance Counselors quickly identify patterns and provide appropriate interventions.

## 🎯 How It Works

### Automatic Detection
The system automatically:
1. **Counts previous violations** for each student when displaying reports
2. **Flags repeat offenders** with a visual badge
3. **Updates case evaluations** with repeat offender status
4. **Provides detailed violation history** including severity breakdown

### Detection Logic
```python
For each incident report:
- Count all previous reports for the same student
- Exclude the current report from the count
- Mark as repeat offender if count > 0
- Display count in badge (e.g., "REPEATED (2x)")
```

## 📍 Where It Appears

### 1. All Reports Table (`/all-reports/`)
**Display:**
- Red badge next to student name
- Shows violation count
- Example: `Juan Dela Cruz [🔴 REPEATED (2x)]`

**Badge Style:**
- Red background (`bg-red-100`)
- Red text (`text-red-800`)
- Red border (`border-red-300`)
- Warning icon (⚠️)

### 2. Report Detail Page (`/report/<case_id>/`)
**Display:**
- Badge next to student name in "Student Information" section
- Badge in "Involved Students" section (if applicable)
- Shows: `REPEATED (Xx)`

### 3. Case Evaluation Page (`/case-evaluation/`)
**Display:**
- Badge next to student name in the cases table
- Helps counselors identify repeat offenders during evaluation
- Automatically adds note to evaluation if student is repeat offender

**Automatic Evaluation Note:**
```
⚠️ REPEAT OFFENDER: X previous violation(s)
```

## 🔢 Badge Examples

| Previous Violations | Badge Display |
|---------------------|---------------|
| 0 | No badge |
| 1 | REPEATED (1x) |
| 2 | REPEATED (2x) |
| 3 | REPEATED (3x) |
| 5+ | REPEATED (5x) |

## 📊 Detailed Information Available

The system tracks:
- **Total violation count**: All previous violations
- **Recent violations**: Violations in last 30 days
- **Severity breakdown**: Minor vs Major violations
- **Last violation date**: Date of most recent violation

## 🎨 Visual Design

### Badge HTML:
```html
<span class="inline-flex items-center px-2 py-0.5 text-xs font-bold rounded-full 
      bg-red-100 text-red-800 border border-red-300 ml-2">
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
✅ Any incident report where student is `reported_student`
✅ Reports created before the current report
✅ All statuses (pending, resolved, closed, etc.)
✅ All severity levels (minor and major)

### What Doesn't Count:
❌ Current report itself
❌ Reports where student is only mentioned in text
❌ Reports created after current report
❌ Deleted or archived reports

## 💡 Benefits

### For Discipline Officers:
1. **Quick Identification** - Instantly see repeat offenders
2. **Pattern Recognition** - Identify students needing intervention
3. **Prioritization** - Focus on chronic cases
4. **Documentation** - Clear violation history

### For Guidance Counselors:
1. **Early Intervention** - Catch patterns early
2. **Targeted Support** - Provide appropriate counseling
3. **Progress Tracking** - Monitor improvement over time
4. **Risk Assessment** - Identify high-risk students
5. **Automatic Flagging** - Evaluations automatically note repeat offenders

### For Administrators:
1. **Data-Driven Decisions** - Make informed policy decisions
2. **Resource Allocation** - Direct resources to repeat offenders
3. **Trend Analysis** - Identify school-wide patterns
4. **Accountability** - Track intervention effectiveness

## 🔧 Technical Implementation

### Files Modified:
1. **`incidents/repeat_offender_utils.py`** (NEW)
   - Utility functions for repeat offender detection
   - `get_repeat_offender_info()` - Main detection function
   - `auto_flag_repeat_offender()` - Auto-flag evaluations

2. **`incidents/views.py`**
   - `all_reports()` - Added repeat detection to all reports
   - `report_detail()` - Added repeat info to report details
   - `case_evaluation()` - Auto-flag repeat offenders in evaluations

3. **`templates/all_reports.html`**
   - Added repeat offender badge to student names

4. **`templates/report_detail.html`**
   - Added repeat offender badge to student information
   - Added badge to involved students section

5. **`templates/counselor/case_evaluation.html`**
   - Added repeat offender badge to cases table

### Database Queries:
- No new tables required
- Uses existing `IncidentReport` model
- Efficient query with `created_at__lt` filter
- Minimal performance impact

## 📈 Usage Examples

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
- **Evaluation:** Automatically notes "⚠️ REPEAT OFFENDER: 1 previous violation(s)"

### Scenario 3: Chronic Offender
- **Student:** Pedro Reyes
- **Previous violations:** 5
- **Display:** Pedro Reyes [🔴 REPEATED (5x)]
- **Action:** Immediate attention, possible intervention
- **Evaluation:** Automatically notes "⚠️ REPEAT OFFENDER: 5 previous violation(s)"

## 🚀 Deployment

### Status: ✅ Implemented and Ready
- All views updated with automatic detection
- All templates updated with badge display
- Utility functions created and tested
- Case evaluations automatically flag repeat offenders

### To Deploy:
1. Commit changes to Git
2. Push to GitHub
3. Render will automatically deploy
4. No database migrations needed

## 🔮 Future Enhancements

Possible improvements:
1. **Severity-Based Detection** - Different badges for minor vs major repeats
2. **Time-Based Detection** - Flag recent repeats (e.g., within 30 days)
3. **Incident Type Patterns** - Detect specific violation patterns
4. **Automatic Escalation** - Auto-escalate chronic offenders
5. **Parent Notifications** - Alert parents of repeat violations
6. **Intervention Tracking** - Link to counseling/VRF programs
7. **Success Metrics** - Track reduction in repeat offenses
8. **Repeat Offender Dashboard** - Dedicated view for repeat offenders
9. **Trend Analysis** - Charts showing repeat offense trends

## 📝 API Reference

### `get_repeat_offender_info(student, current_report=None)`
Returns detailed repeat offender information.

**Parameters:**
- `student`: CustomUser object (student)
- `current_report`: IncidentReport object (optional, to exclude from count)

**Returns:**
```python
{
    'is_repeat': bool,
    'count': int,
    'recent_count': int,
    'severity_breakdown': {'minor': int, 'major': int},
    'last_violation_date': date or None
}
```

### `auto_flag_repeat_offender(report)`
Automatically flags a report if student is a repeat offender.

**Parameters:**
- `report`: IncidentReport object

**Returns:**
- `bool`: True if flagged as repeat offender

---

**Status:** ✅ Fully Implemented
**Date:** December 9, 2025
**Impact:** All Reports, Report Detail, and Case Evaluation pages
