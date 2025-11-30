# Evidence Verification & Case Routing Feature

## Overview
Enhanced the DO fact-checking process with two key features:
1. **Evidence Verification**: DO can verify if evidence is sufficient before proceeding
2. **Case Routing**: DO decides whether to handle the case or send it to Guidance Counselor

## New Features

### 1. Evidence Status Options
When clicking "Verify & Classify" on a pending report, the DO first verifies evidence:

- **✅ Clear - Sufficient Evidence**: Evidence is complete and the report can proceed to routing
- **⚠️ Needs More Evidence**: Reporter will be notified to provide additional information

### 2. Case Routing Decision
After evidence is verified as clear, DO chooses the case destination:

- **🏢 Handle by Discipline Office (DO)**: Minor violations that DO can handle directly (warnings, sanctions, monitoring)
- **🧠 Send to Guidance Counselor**: Major violations requiring counseling intervention and behavioral assessment

### 3. Dynamic Form Behavior

#### When "Clear" is selected:
- Shows case routing options (DO or Counselor)
- Shows routing notes field
- Button text: "Verify & Classify"
- Proceeds with routing workflow

#### When "Needs More Evidence" is selected:
- Hides routing fields
- Shows "Reason for Requesting More Evidence" field (required)
- Button text: "Request More Evidence"
- Button color changes to orange
- Sends notification to reporter

### 4. Notifications System

#### When evidence is insufficient:
- Reporter receives notification: "Additional Evidence Required"
- Message includes case ID and specific reason from DO
- Report remains in "pending" status

#### When routed to DO:
- Other DO staff receive notification: "Case Assigned to DO"
- Student receives notification: "Case Under DO Review"
- Case status changes to "classified"

#### When routed to Counselor:
- All counselors receive notification: "Case Referred for Counseling"
- Student receives notification: "Counseling Session Required"
- Case status changes to "classified"

### 5. Database Changes
Added fields to `IncidentReport` model:
- `evidence_status`: Tracks if evidence is pending/clear/insufficient
- `evidence_notes`: Stores DO's notes about evidence status

Updated `Classification` model:
- `severity` field now represents routing decision (DO or Counselor)
- Added helper method `get_routing_destination()`

## User Flow

### DO Workflow:
1. Navigate to "Fact-Check Reports"
2. Click "Verify & Classify" on a pending report
3. **Step 1 - Verify Evidence:**
   - Select "Clear" or "Needs More Evidence"
   - If insufficient: Provide reason → Reporter notified → Done
4. **Step 2 - Route Case (if evidence clear):**
   - Choose "Handle by DO" or "Send to Guidance Counselor"
   - Add optional routing notes
   - Submit → Appropriate parties notified

### Reporter Experience:
- If evidence insufficient: Gets notification with specific requirements
- Can provide additional evidence/information
- Report stays in pending queue for re-review

### Student Experience:
- Receives notification about case status
- Knows whether case is with DO or Counselor
- Understands next steps

## Technical Implementation

### Models (`incidents/models.py`):
```python
evidence_status = models.CharField(max_length=20, choices=[
    ('pending', 'Pending Review'),
    ('clear', 'Clear - Sufficient Evidence'),
    ('insufficient', 'Needs More Evidence')
], default='pending', blank=True)
evidence_notes = models.TextField(blank=True)
```

### Views (`incidents/views.py`):
- Updated `fact_check_reports` view to handle evidence status
- Added logic to notify reporter when evidence is insufficient
- Prevents classification if evidence is marked as insufficient

### Template (`templates/do/fact_check_reports.html`):
- Enhanced modal with radio button options
- Dynamic form sections based on evidence status selection
- JavaScript to toggle form fields and button appearance

## Benefits

1. **Better Quality Control**: Ensures reports have sufficient evidence before proceeding
2. **Clear Communication**: Reporters know exactly what additional information is needed
3. **Efficient Workflow**: Prevents incomplete reports from moving forward
4. **Audit Trail**: Evidence status and notes are tracked in the database
5. **User-Friendly**: Intuitive interface with clear visual feedback

## Migrations Applied
1. `0013_incidentreport_evidence_notes_and_more.py` - Added evidence tracking fields
2. `0014_alter_classification_internal_notes_and_more.py` - Updated routing choices

## Related Documentation
See `CASE_ROUTING_SYSTEM.md` for detailed information about the routing decision framework.
