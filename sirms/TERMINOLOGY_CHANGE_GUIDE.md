# Terminology Change: "Case" → "Referral"

## Overview
Change all user-facing instances of "Case" to "Referral" throughout the system while maintaining database field names for compatibility.

## Scope

### What Changes:
- ✅ Display text in templates
- ✅ User messages in views
- ✅ Model verbose_names
- ✅ Form labels
- ✅ Documentation

### What DOES NOT Change:
- ❌ Database field names (case_id stays as case_id)
- ❌ Python variable names in code
- ❌ URL patterns
- ❌ Function/method names

## Search and Replace Patterns

### Templates (HTML files)
```
"Case ID" → "Referral ID"
"case ID" → "referral ID"
"Case" → "Referral" (context-dependent)
"case" → "referral" (context-dependent)
"Cases" → "Referrals"
"cases" → "referrals"
```

### Views (Python messages)
```python
# BEFORE
messages.success(request, f'Case {report.case_id} updated')

# AFTER
messages.success(request, f'Referral {report.case_id} updated')
```

### Models (verbose_name)
```python
# BEFORE
case_id = models.CharField(max_length=50, unique=True)

# AFTER
case_id = models.CharField(max_length=50, unique=True, verbose_name="Referral ID")
```

## Files to Update

### High Priority Templates (User-Facing):
1. `templates/do/behavior_concerns.html`
2. `templates/do/fact_check_reports.html`
3. `templates/counselor/case_evaluation.html`
4. `templates/counselor/major_case_review.html`
5. `templates/esp/vpf_cases.html`
6. `templates/report_detail.html`
7. `templates/my_reports.html`
8. `templates/all_reports.html`
9. `templates/dashboard.html`

### Medium Priority:
10. `templates/counselor/counselor_schedule.html`
11. `templates/counselor/counseling_management_clean.html`
12. `templates/do/classify_violations.html`
13. `templates/shared/case_history.html`

### Views (Messages):
- `incidents/views.py` - Update all user-facing messages

### Models:
- `incidents/models.py` - Add verbose_name to case_id field

## Implementation Strategy

### Phase 1: Critical Templates (Do First)
Update the most visible pages:
- Behavioral Concerns
- Case Evaluation
- VPF Cases
- Report Detail
- My Reports

### Phase 2: Supporting Templates
Update remaining templates:
- Dashboard
- All Reports
- Case History
- Counseling pages

### Phase 3: Backend Messages
Update view messages and notifications

### Phase 4: Models
Add verbose_name attributes

## Example Changes

### Template Example:
```html
<!-- BEFORE -->
<th>Case ID</th>
<td>{{ report.case_id }}</td>
<h2>Case Details</h2>
<p>This case was reported on...</p>

<!-- AFTER -->
<th>Referral ID</th>
<td>{{ report.case_id }}</td>
<h2>Referral Details</h2>
<p>This referral was reported on...</p>
```

### View Example:
```python
# BEFORE
messages.success(request, f'Case {report.case_id} has been evaluated')
Notification.objects.create(
    title='Case Status Updated',
    message=f'Your case {report.case_id} has been updated'
)

# AFTER
messages.success(request, f'Referral {report.case_id} has been evaluated')
Notification.objects.create(
    title='Referral Status Updated',
    message=f'Your referral {report.case_id} has been updated'
)
```

### Model Example:
```python
# BEFORE
class IncidentReport(models.Model):
    case_id = models.CharField(max_length=50, unique=True)

# AFTER
class IncidentReport(models.Model):
    case_id = models.CharField(
        max_length=50, 
        unique=True,
        verbose_name="Referral ID",
        help_text="Unique identifier for this referral"
    )
```

## Context-Sensitive Changes

### Keep "Case" in these contexts:
- "Use case" (technical term)
- "In case of" (conditional phrase)
- "Case-sensitive" (technical term)
- Variable names in code
- Database field names

### Change "Case" in these contexts:
- "Case ID" → "Referral ID"
- "Case details" → "Referral details"
- "Case status" → "Referral status"
- "Case evaluation" → "Referral evaluation"
- "Case history" → "Referral history"
- "VPF case" → "VPF referral"
- "Major case" → "Major referral"
- "Minor case" → "Minor referral"

## Testing Checklist

After making changes:
- [ ] All pages load without errors
- [ ] "Referral ID" displays correctly
- [ ] Database queries still work
- [ ] Forms submit successfully
- [ ] Notifications use "Referral"
- [ ] Reports generate correctly
- [ ] Search/filter functions work
- [ ] No broken links
- [ ] No JavaScript errors
- [ ] Mobile view displays correctly

## Estimated Impact

### Files Affected: ~30-40 files
- Templates: ~20 files
- Views: 1 file (many changes)
- Models: 1 file (few changes)
- Forms: 1 file (label changes)

### Time Estimate: 2-3 hours
- Phase 1: 45 minutes
- Phase 2: 45 minutes
- Phase 3: 30 minutes
- Phase 4: 15 minutes
- Testing: 30 minutes

## Risks & Mitigation

### Risks:
1. Breaking existing functionality
2. Inconsistent terminology
3. Missing some instances
4. Database issues

### Mitigation:
1. Keep database field names unchanged
2. Test thoroughly after each phase
3. Use search to find all instances
4. Create backup before starting
5. Update in phases, not all at once

## Rollback Plan

If issues occur:
1. Revert template changes
2. Revert view message changes
3. Keep model verbose_name changes (safe)
4. Test system functionality
5. Fix issues and retry

## Post-Implementation

After completion:
- [ ] Update user documentation
- [ ] Update training materials
- [ ] Notify users of terminology change
- [ ] Update help text
- [ ] Update tooltips
- [ ] Update error messages

## Notes

- This is a cosmetic change for users
- Backend functionality remains unchanged
- Database structure is not affected
- No migration needed
- Can be done incrementally
- Low risk if done carefully

## Recommendation

Given the scope (30-40 files), I recommend:

**Option A: Incremental Approach**
- Do Phase 1 now (critical templates)
- Test thoroughly
- Do Phase 2 tomorrow
- Continue until complete

**Option B: Complete Implementation**
- Do all phases in one session
- Requires 2-3 hours
- More efficient but higher risk
- Needs thorough testing

**Option C: Automated Script**
- Create Python script to do replacements
- Review changes before committing
- Fastest but needs careful review

Which approach would you prefer?
