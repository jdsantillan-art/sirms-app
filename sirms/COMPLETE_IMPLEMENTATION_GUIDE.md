# Complete Implementation Guide - All 4 Features

## Overview
This document outlines the complete implementation of all 4 requested features with code examples and file changes.

## Feature 1: Bullying Type Dropdown

### Files to Modify:
1. `templates/report_incident.html` - Add bullying type dropdown
2. `incidents/forms.py` - Add bullying_type field (optional)

### Implementation:
Add after incident_type field in report_incident.html:
```html
<!-- Bullying Type (conditional) -->
<div id="bullyingTypeDiv" style="display: none;">
    <label>Bullying Type <span class="text-red-500">*</span></label>
    <select name="bullying_type" id="bullyingType">
        <option value="">Select Bullying Type</option>
        <option value="Physical">Physical</option>
        <option value="Psychological">Psychological</option>
        <option value="Sexual">Sexual</option>
        <option value="Emotional">Emotional</option>
        <option value="Cyber">Cyber</option>
        <option value="Social">Social</option>
        <option value="Gender-based">Gender-based</option>
    </select>
</div>
```

Add JavaScript:
```javascript
incidentTypeSelect.addEventListener('change', function() {
    const selectedText = this.options[this.selectedIndex].text;
    if (selectedText.toLowerCase().includes('bullying')) {
        document.getElementById('bullyingTypeDiv').style.display = 'block';
    } else {
        document.getElementById('bullyingTypeDiv').style.display = 'none';
    }
});
```

## Feature 2: ESP Teacher VPF Status Updates

### Files to Create/Modify:
1. `templates/esp/vpf_cases.html` - Add status update button
2. `incidents/views.py` - Add update_vpf_status view
3. `incidents/urls.py` - Add URL route

### Code to Add:

**In vpf_cases.html** - Add button in table:
```html
<button onclick="showStatusModal({{ vpf.id }}, '{{ vpf.status }}')" 
        class="text-blue-600 hover:underline">
    Update Status
</button>
```

**New View in views.py**:
```python
@login_required
def update_vpf_status(request, vpf_id):
    if request.user.role != 'esp_teacher':
        return JsonResponse({'success': False}, status=403)
    
    vpf_case = get_object_or_404(VPFCase, id=vpf_id)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        notes = request.POST.get('notes', '')
        
        vpf_case.status = new_status
        vpf_case.notes = f"{vpf_case.notes}\n\n[{timezone.now().strftime('%Y-%m-%d %H:%M')}] Status updated to {new_status}: {notes}"
        vpf_case.save()
        
        # Notify guidance counselor
        if vpf_case.assigned_by:
            Notification.objects.create(
                user=vpf_case.assigned_by,
                title=f'VPF Status Updated - {vpf_case.report.case_id}',
                message=f'ESP Teacher updated VPF case status to "{new_status}" for {vpf_case.student.get_full_name()}. Notes: {notes}',
                report=vpf_case.report
            )
        
        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False}, status=400)
```

## Feature 3: DO Behavioral Concerns Evaluation

### Files to Modify:
1. `templates/do/behavior_concerns.html` - Add evaluation button
2. `incidents/views.py` - Add evaluate_behavior_concern view
3. `incidents/urls.py` - Add URL route

### Code to Add:

**New View**:
```python
@login_required
def evaluate_behavior_concern(request, report_id):
    if request.user.role != 'do':
        return JsonResponse({'success': False}, status=403)
    
    report = get_object_or_404(IncidentReport, id=report_id)
    
    if request.method == 'POST':
        action = request.POST.get('action')  # Intake Interview, Investigate, Parent Conference
        notes = request.POST.get('notes', '')
        
        # Create internal note
        InternalNote.objects.create(
            report=report,
            author=request.user,
            note=f"DO Evaluation - {action}: {notes}",
            is_private=False
        )
        
        # Notify student
        if report.reported_student:
            Notification.objects.create(
                user=report.reported_student,
                title=f'Behavioral Concern Evaluation - {report.case_id}',
                message=f'The Discipline Office has evaluated your case. Action: {action}. Please check with the DO for more information.',
                report=report
            )
        
        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False}, status=400)
```

## Feature 4: Terminology Change (Case → Referral)

### Scope: 30+ files need updates

### Database Fields: NO CHANGE
- Keep `case_id` field name in database
- Only change display text

### Changes Needed:

**Models (verbose_name only)**:
```python
case_id = models.CharField(verbose_name="Referral ID", ...)
```

**Templates** - Replace in all files:
- "Case ID" → "Referral ID"
- "case" → "referral" (context-dependent)
- "Case" → "Referral"

**Files to Update** (partial list):
- templates/report_detail.html
- templates/my_reports.html
- templates/all_reports.html
- templates/counselor/*.html
- templates/do/*.html
- templates/esp/*.html
- incidents/models.py (verbose_name)
- incidents/views.py (messages)

## Implementation Order

1. Feature 1: Bullying Dropdown (Quick)
2. Feature 2: ESP Status Updates
3. Feature 3: DO Evaluation
4. Feature 4: Terminology Change (Most extensive)

## Testing Checklist

After implementation:
- [ ] Bullying dropdown appears when bullying selected
- [ ] ESP can update VPF status
- [ ] Guidance receives notification on VPF status change
- [ ] DO can evaluate behavioral concerns
- [ ] Student receives notification on evaluation
- [ ] All "Case" references changed to "Referral"
- [ ] Existing data still displays correctly

## Estimated Time: 2-3 hours total

Ready to proceed with full implementation?
