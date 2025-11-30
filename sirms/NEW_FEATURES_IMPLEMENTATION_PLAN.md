# New Features Implementation Plan

## Feature 1: ESP Teacher VPF Status Updates
**What**: ESP Teachers can update VPF case status (pending → ongoing → complete) with notes
**Notifications**: Guidance counselor receives notification on each status change

### Implementation:
1. Add status update modal in `vpf_cases.html`
2. Create view endpoint: `update_vpf_status()`
3. Add notification to guidance counselor
4. Update VPFCase model if needed

## Feature 2: DO Behavioral Concerns Evaluation
**What**: DO can evaluate behavioral concerns with actions and notes
**Actions**: Intake Interview, Investigate, Parent Conference
**Notifications**: Violator (student) receives notification

### Implementation:
1. Add evaluation modal in `behavior_concerns.html`
2. Create view endpoint: `evaluate_behavior_concern()`
3. Add notification to student
4. Store evaluation data

## Feature 3: Bullying Type Dropdown
**What**: When "Bullying" is selected, show dropdown with types
**Types**: Physical, Psychological, Sexual, Emotional, Cyber, Social, Gender-based

### Implementation:
1. Update `report_incident.html` with conditional dropdown
2. Add JavaScript to show/hide bullying types
3. Update form handling to capture bullying type
4. Store in incident_type or description field

## Feature 4: Terminology Change: Case → Referral
**What**: Change all instances of "Case" to "Referral" throughout system
**Scope**: Templates, models (display), views (messages), documentation

### Implementation:
1. Update all templates (case_id → referral_id display)
2. Update model __str__ methods and verbose names
3. Update view messages
4. Keep database field names as-is (case_id) for compatibility
5. Update documentation

## Priority Order:
1. Feature 3 (Bullying dropdown) - Quick, affects data entry
2. Feature 4 (Terminology) - Wide impact, better to do early
3. Feature 1 (ESP Status) - Important for workflow
4. Feature 2 (DO Evaluation) - Similar to Feature 1

## Files to Modify:
- `incidents/views.py` - Add new endpoints
- `incidents/models.py` - Add verbose names, update __str__
- `templates/esp/vpf_cases.html` - Status update modal
- `templates/do/behavior_concerns.html` - Evaluation modal
- `templates/report_incident.html` - Bullying dropdown
- `incidents/urls.py` - New URL routes
- Multiple templates - Terminology changes
