# 🎓 SIRMS Defense Presentation Script
## School Incident Reporting and Management System

---

## 📋 TABLE OF CONTENTS
1. [Overall System Process Flow](#a-overall-system-process-flow)
2. [Incident Reporting Process](#b-incident-reporting-process)
3. [Classification & Routing Process](#c-classification--routing-process)
4. [Guidance Counseling Process](#d-guidance-counseling-process)
5. [Status Management Process](#e-status-management-process)
6. [Approval & Record Handling](#f-approval--record-handling)
7. [Notification Process](#g-notification-process)
8. [User Access Process](#h-user-access-process)
9. [Reporting & Analytics Process](#i-reporting--analytics-process)

---

## 🔵 A. OVERALL SYSTEM PROCESS FLOW

### Q1: Can you explain the entire process flow from reporting to resolution?

**ANSWER:**
"Our SIRMS follows a structured 7-stage workflow:

**Stage 1: Incident Reporting**
- Students or teachers submit incident reports through the web portal
- System validates all required fields and generates a unique Case ID (format: YYYY-####)
- Evidence files can be uploaded (photos, documents)

**Stage 2: Initial Review (DO)**
- All Discipline Officers receive notifications of new reports
- DO performs fact-checking and evidence review
- Status changes from 'pending' to 'under_review'

**Stage 3: Classification**
- DO classifies the incident severity based on violation type
- Minor violations: Handled directly by DO
- Major violations: Routed to Guidance Office

**Stage 4: Case Evaluation (for Major Cases)**
- Guidance Counselor reviews the case
- Checks student's violation history for repeat offenses
- Determines verdict: Guilty, Not Guilty, or Insufficient Evidence
- Provides recommendation based on commission level (1st, 2nd, 3rd)


**Stage 5: Intervention Assignment**
- VPF (Values Reflective Formation): Routed to ESP Teacher
- Other interventions: Managed by Counselor via Counseling Schedule
- Parent conferences scheduled through DO Schedule

**Stage 6: Intervention Execution**
- ESP Teachers manage VPF sessions independently
- Counselors conduct counseling sessions
- DO coordinates parent conferences
- All updates trigger automatic notifications

**Stage 7: Case Resolution**
- Status progresses: Pending → Ongoing → Completed
- Final status: Resolved or Closed
- All records archived in the database
- Analytics updated automatically"

---

### Q2: What happens immediately after submission?

**ANSWER:**
"The moment a report is submitted, our system executes 5 automatic processes:

1. **Case ID Generation**: Creates unique identifier (e.g., 2025-0001)
2. **Database Storage**: Saves report with status='pending'
3. **File Upload**: Stores evidence files securely in the file system
4. **Automatic Notifications**: Sends to:
   - All Discipline Officers: 'New incident requires fact-checking'
   - Reporter: 'Report submitted successfully'
   - Reported Student (if exists): 'You've been mentioned in a report'
5. **Dashboard Update**: Report appears in DO's pending queue immediately

The entire process takes less than 2 seconds."

---

### Q3: How does the system validate incident details?

**ANSWER:**
"We have 3 layers of validation:

**Frontend Validation (Real-time):**
- Required fields marked with asterisks
- Date cannot be in the future
- File size limits (max 10MB per file)
- File type restrictions (images, PDFs, documents only)

**Backend Validation (Server-side):**
- Checks if reporter is authenticated
- Validates student exists in database
- Ensures incident type is valid
- Verifies curriculum → grade → section relationship
- Prevents duplicate submissions within 5 minutes

**Business Logic Validation:**
- Incident date must be within current school year
- Student must belong to selected section
- Teacher must be assigned to that section
- Incident type must match severity classification

If any validation fails, the system shows specific error messages and prevents submission."

---

### Q4: How does the system notify the Discipline Officer?

**ANSWER:**
"We use a multi-channel notification system:

**1. Dashboard Notification Badge:**
- Red badge appears on DO's notification icon
- Shows count of unread notifications
- Updates in real-time

**2. Notification Center:**
- Detailed notification with:
  - Case ID
  - Student name
  - Incident type
  - Timestamp
- Click to view full report

**3. Pending Queue:**
- Report appears in 'All Reports' with status 'Pending'
- Filterable by status, type, grade level
- Search by Case ID or student name

**4. Email Notification (Optional):**
- Can be configured in settings
- Sends summary to DO's registered email

All DOs receive the notification simultaneously, and any DO can claim the case for review."

---

### Q5: How does DO classify reports?

**ANSWER:**
"The DO follows a structured classification process:

**Step 1: Fact-Checking**
- Reviews report details for accuracy
- Verifies student information
- Checks if incident type matches description

**Step 2: Evidence Review**
- Examines uploaded evidence files
- Marks evidence status as:
  - Clear: Evidence is sufficient
  - Insufficient: Needs more evidence
  - Pending: Awaiting additional files

**Step 3: Severity Classification**
- Based on incident type:
  - **Prohibited Acts (PA)**: Major violations (bullying, violence, drugs)
  - **Other School Policies (OSP)**: Minor violations (uniform, tardiness)

**Step 4: Routing Decision**
- **Minor (OSP)**: DO handles directly
  - Can schedule parent conference
  - Issues warning or minor sanction
  - Updates status to 'resolved'
  
- **Major (PA)**: Routes to Guidance
  - Creates classification record
  - Updates status to 'classified'
  - Notifies all Guidance Counselors
  - Case appears in Counselor's queue

The classification is stored in the Classification database with timestamp and DO's notes."

---

### Q6: What happens when DO forwards to Guidance?

**ANSWER:**
"When a case is forwarded to Guidance, the system executes this workflow:

**Internal System Actions:**
1. Updates report status: 'under_review' → 'classified'
2. Creates Classification record with:
   - Severity: 'major'
   - DO's internal notes
   - Classification timestamp
3. Links report to Classification database

**Notification Process:**
- All Guidance Counselors notified: 'New major case requires evaluation'
- Reporter notified: 'Your case has been forwarded to Guidance Office'
- Student notified: 'Your case is being reviewed by Guidance'
- Adviser notified (if student has one): 'Your advisee has a major case'

**Dashboard Updates:**
- Case appears in Counselor's 'Case Evaluation' queue
- DO can still view case in 'All Reports' (read-only)
- Case shows status badge: 'Classified'

**Data Access:**
- Counselor can see:
  - Full report details
  - Evidence files
  - DO's classification notes
  - Student's violation history
  - Related cases (if repeat offender)

The handoff is seamless - no data is lost, and all stakeholders are informed."

---

### Q7: How does Guidance manage the incident?

**ANSWER:**
"Guidance follows a comprehensive evaluation process:

**Step 1: Case Review**
- Access case from 'Case Evaluation' queue
- Review all report details and evidence
- Check student's violation history
- System automatically flags repeat offenders with badge

**Step 2: Evaluation Form**
- Select Commission Level:
  - 1st Commission: First offense
  - 2nd Commission: Second offense
  - 3rd Commission: Third or more offenses
  
- Choose Intervention (auto-updates based on commission):
  - **1st Commission Options:**
    - Parent Conference with Adviser/Subject Teacher
    - Counseling/Follow-up/Supervised Intervention
  - **2nd Commission Options:**
    - Parent Conference
    - Values Reflective Formation (VPF)
  - **3rd Commission Options:**
    - Recommendation for Sanction


- Set Status:
  - Pending: Awaiting action
  - Ongoing: Currently being addressed
  - Complete: Intervention finished

- Add Evaluation Notes

**Step 3: System Routes Based on Intervention**

**If VPF Selected:**
- Creates VPFCase record
- Routes to ESP Teacher dashboard
- Notifies all ESP Teachers
- Appears in Guidance 'For VRF' (monitoring only)
- ESP Teacher manages independently

**If Other Intervention:**
- Creates CounselingSchedule record
- Appears in Guidance 'Counseling Schedule'
- Counselor sets date/time/location
- Notifies student and adviser

**Step 4: Progress Tracking**
- Counselor can update status anytime
- Add session notes
- Mark as completed/missed/rescheduled
- All updates trigger notifications

**Step 5: Case Closure**
- When intervention is complete
- Final status: 'Resolved'
- Case archived but accessible for history
- Analytics updated automatically"

---

### Q8: How are status updates handled?

**ANSWER:**
"Status management follows a strict workflow with 7 defined statuses:

**Status Progression:**
```
Pending → Under Review → Classified → Evaluated → Sanctioned → Resolved → Closed
```

**Who Can Update:**
- **Pending → Under Review**: Any DO (when they start fact-checking)
- **Under Review → Classified**: DO (after classification)
- **Classified → Evaluated**: Counselor (after evaluation)
- **Evaluated → Sanctioned**: Principal (if sanction needed)
- **Sanctioned → Resolved**: DO/Counselor (after sanction served)
- **Resolved → Closed**: Admin (for archiving)

**What Happens on Status Change:**
1. Database updated with new status
2. Timestamp recorded
3. Internal note created (audit trail)
4. Notifications sent to:
   - Reporter
   - Student
   - Adviser (if exists)
   - Next handler in workflow

**Status Indicators:**
- Color-coded badges in all views
- Dashboard widgets show counts per status
- Filters allow viewing by status
- Analytics track status distribution

The system prevents skipping statuses - must follow the workflow sequence."

---

## 🔵 B. INCIDENT REPORTING PROCESS

### Q1: What fields are required for creating a report?

**ANSWER:**
"Our incident report form has 3 sections with specific required fields:

**Section 1: Reporter Information** (Auto-filled for logged-in users)
- First Name *
- Middle Name (optional)
- Last Name *
- Role (auto-detected: student/teacher)

**Section 2: Student Information**
- Involved Students * (text field for multiple students)
- Student Gender * (Male/Female/Other)
- Curriculum * (dropdown: K-12, STEM, ABM, HUMSS, etc.)
- Grade Level * (auto-updates based on curriculum)
- Section * (auto-updates based on grade)
- Teacher Name * (auto-updates based on section)

**Section 3: Incident Details**
- Incident Date * (cannot be future date)
- Incident Time * (24-hour format)
- Incident Type * (dropdown: linked to legal documents)
- Description * (minimum 20 characters)
- Bullying Type (conditional: only if incident type is bullying)
- Evidence Files (optional: images, PDFs, documents)

**Dynamic Dropdowns:**
- Curriculum selection filters grade levels
- Grade level selection filters sections
- Section selection auto-fills teacher name

**Validation Rules:**
- All fields marked with * are required
- Date must be within current school year
- Time must be valid 24-hour format
- Description must be detailed (min 20 chars)
- File size max 10MB per file
- Max 5 files per report

If any required field is missing, the submit button is disabled and error messages appear."

---

### Q2: How does the system handle evidence uploads?

**ANSWER:**
"We have a secure file upload system with multiple safeguards:

**Upload Process:**
1. **File Selection**: User clicks 'Choose Files' or drags files
2. **Client-side Validation**:
   - Checks file type (jpg, png, pdf, doc, docx)
   - Checks file size (max 10MB per file)
   - Max 5 files per report
   - Shows preview thumbnails

3. **Server-side Processing**:
   - Generates unique filename (timestamp + random string)
   - Stores in `/media/evidence/` directory
   - Saves file path in database
   - Creates backup reference

4. **Security Measures**:
   - Sanitizes filenames (removes special characters)
   - Scans for malicious content
   - Restricts file types (no executables)
   - Access control (only authorized users can view)


**Storage Structure:**
```
/media/evidence/
  ├── 2025-0001_evidence1_20250102_143022.jpg
  ├── 2025-0001_evidence2_20250102_143025.pdf
  └── 2025-0002_evidence1_20250102_150033.png
```

**Viewing Evidence:**
- DO, Counselor, Principal can view all evidence
- Reporter can view their own evidence
- Student can view evidence related to their case
- Evidence displayed in lightbox/modal
- Download option available for authorized users

**Evidence Status Tracking:**
- DO marks evidence as: Clear, Insufficient, or Pending
- Status visible to all stakeholders
- Can request additional evidence if insufficient"

---

### Q3: How does the system map incident types to legal documents?

**ANSWER:**
"We have a comprehensive incident type database linked to legal references:

**Database Structure:**
- Each incident type has:
  - Name (e.g., 'Bullying', 'Theft', 'Vandalism')
  - Severity (Prohibited Acts or Other School Policies)
  - Legal Reference (RA 10627, DepEd Order, School Handbook)
  - Description
  - Recommended Actions

**Automatic Mapping:**
1. **During Report Creation**:
   - User selects incident type from dropdown
   - System retrieves legal reference
   - Displays reference below dropdown
   - Stores incident_type_id in report

2. **During Classification**:
   - DO sees incident type with legal reference
   - Severity auto-determined (PA or OSP)
   - Classification decision pre-filled based on severity

3. **During Evaluation**:
   - Counselor sees full legal context
   - Recommended interventions based on incident type
   - Commission level determines available options

**Example Mappings:**
- **Bullying** → RA 10627 (Anti-Bullying Act) → Prohibited Act → Major
- **Uniform Violation** → School Handbook Section 3.2 → OSP → Minor
- **Physical Violence** → RA 7610 (Child Protection) → Prohibited Act → Major
- **Tardiness** → School Policy → OSP → Minor

**Benefits:**
- Ensures legal compliance
- Consistent classification
- Proper documentation
- Audit trail for legal purposes"

---

### Q4: How does the system ensure correct student/section linking?

**ANSWER:**
"We use a cascading dropdown system with database relationships:

**Database Relationships:**
```
Curriculum → Grade Level → Section → Teacher Assignment
```

**Step-by-Step Process:**

**Step 1: Curriculum Selection**
- User selects curriculum (K-12, STEM, ABM, etc.)
- System queries database for valid grade levels
- Only grades 7-12 shown for Senior High curricula
- Only grades 1-10 shown for K-12


**Step 2: Grade Level Selection**
- User selects grade level
- System queries sections for that grade
- Sections filtered by curriculum and grade
- Only active sections shown

**Step 3: Section Selection**
- User selects section (e.g., 'Rizal', 'Bonifacio')
- System queries TeacherAssignment table
- Finds adviser for that section
- Auto-fills teacher name field

**Step 4: Validation**
- System verifies:
  - Section exists in database
  - Section belongs to selected grade
  - Grade belongs to selected curriculum
  - Teacher is assigned to section
  - Student (if registered) belongs to section

**Data Integrity:**
- Foreign key constraints prevent invalid combinations
- Dropdown options dynamically filtered
- Cannot select non-existent combinations
- Real-time validation on form submission

**Example Flow:**
```
User selects: STEM → Grade 11 → Rizal
System auto-fills: Teacher: Ms. Maria Santos (Adviser)
Validation: ✓ STEM has Grade 11 ✓ Grade 11 has Rizal ✓ Ms. Santos is adviser
```

This ensures 100% data accuracy and prevents mismatched records."

---

### Q5: How do dynamic dropdowns work?

**ANSWER:**
"We use AJAX-based dynamic dropdowns with real-time updates:

**Technical Implementation:**

**Frontend (JavaScript):**
```javascript
// When curriculum changes
$('#curriculum').change(function() {
    let curriculum_id = $(this).val();
    // AJAX call to get grade levels
    $.get('/api/get-grades/', {curriculum: curriculum_id}, function(data) {
        // Update grade dropdown
        $('#grade').html(data.options);
    });
});
```

**Backend (Django Views):**
```python
def get_grades(request):
    curriculum_id = request.GET.get('curriculum')
    grades = GradeLevel.objects.filter(curriculum_id=curriculum_id)
    return JsonResponse({'options': grades})
```

**User Experience:**
1. User selects Curriculum
   - Grade dropdown updates instantly
   - Section dropdown clears
   - Teacher field clears

2. User selects Grade
   - Section dropdown updates instantly
   - Teacher field clears

3. User selects Section
   - Teacher field auto-fills
   - Shows adviser name

**Performance:**
- Responses in < 100ms
- Cached database queries
- Minimal data transfer
- No page reload needed

**Error Handling:**
- If no grades found: Shows 'No grades available'
- If no sections found: Shows 'No sections for this grade'
- If no teacher assigned: Shows 'No adviser assigned'
- Network error: Shows retry button

This creates a smooth, intuitive user experience while maintaining data integrity."

---

## 🔵 C. CLASSIFICATION & ROUTING PROCESS

### Q1: How does the system determine Minor vs Major?

**ANSWER:**
"Classification is based on incident type severity with both automatic and manual components:

**Automatic Classification (System-Assisted):**
- Each incident type has pre-defined severity in database:
  - **Prohibited Acts (PA)**: Automatically flagged as Major
    - Bullying, Physical Violence, Drugs, Weapons, Theft
  - **Other School Policies (OSP)**: Automatically flagged as Minor
    - Uniform violations, Tardiness, Minor disruptions

**Manual Override (DO Decision):**
- DO can override automatic classification based on:
  - Severity of incident (e.g., minor bullying vs severe bullying)
  - Evidence quality
  - Student's violation history
  - Context and circumstances

**Classification Criteria:**

**Minor (DO Handles):**
- First-time minor offenses
- Clear evidence
- No physical harm
- Can be resolved with warning/parent conference
- Examples: Uniform violation, tardiness, minor disruption

**Major (Guidance Handles):**
- Serious violations (PA)
- Repeat offenses
- Physical/emotional harm
- Requires counseling/intervention
- Examples: Bullying, violence, drugs, weapons

**System Logic:**
```python
if incident_type.severity == 'prohibited':
    suggested_classification = 'major'
elif student.violation_count >= 3:
    suggested_classification = 'major'  # Repeat offender
else:
    suggested_classification = 'minor'
```

**DO's Final Decision:**
- Reviews suggested classification
- Can accept or override
- Must provide justification if overriding
- Classification stored with timestamp and notes

This hybrid approach ensures consistency while allowing professional judgment."

---

### Q2: Is classification automatic, manual, or both?

**ANSWER:**
"It's a hybrid system combining automatic suggestions with manual approval:

**Automatic Components:**
1. **Severity Detection**:
   - System reads incident_type.severity
   - Flags PA as major, OSP as minor
   - Shows suggestion to DO

2. **Repeat Offender Detection**:
   - System queries student's violation history
   - Counts previous incidents
   - Displays badge if ≥ 2 previous violations
   - Auto-suggests major classification for repeat offenders

3. **Evidence Assessment**:
   - System checks if evidence files exist
   - Marks evidence_status as 'pending' initially
   - Alerts DO if no evidence uploaded

**Manual Components:**
1. **DO Review**:
   - DO reads full report
   - Reviews evidence files
   - Considers context and circumstances
   - Makes final classification decision

2. **Evidence Status**:
   - DO manually marks evidence as:
     - Clear: Sufficient evidence
     - Insufficient: Needs more evidence
     - Pending: Awaiting additional files

3. **Routing Decision**:
   - DO decides: Handle personally or forward to Guidance
   - Can add internal notes
   - Confirms classification before routing


**Workflow:**
```
1. System suggests classification (automatic)
2. DO reviews suggestion (manual)
3. DO can accept or override (manual)
4. System validates decision (automatic)
5. System routes based on decision (automatic)
6. System sends notifications (automatic)
```

**Benefits:**
- Speed: Automatic suggestions save time
- Accuracy: Manual review ensures correctness
- Consistency: System enforces rules
- Flexibility: DO can use professional judgment
- Accountability: All decisions logged with justification"

---

### Q3: How did you design the DO → Guidance flow?

**ANSWER:**
"The DO to Guidance handoff is designed for seamless data transfer and clear accountability:

**Design Principles:**
1. **No Data Loss**: All information transfers completely
2. **Clear Ownership**: One person responsible at a time
3. **Audit Trail**: Every action logged
4. **Stakeholder Awareness**: All parties notified

**Technical Implementation:**

**Step 1: DO Classification**
```python
# DO classifies case
classification = Classification.objects.create(
    report=report,
    classified_by=do_user,
    severity='major',
    internal_notes='Serious bullying case, needs counseling'
)
report.status = 'classified'
report.save()
```

**Step 2: Database Linking**
- Classification record links to IncidentReport
- Foreign key relationship maintained
- DO's notes stored in Classification table
- Original report unchanged (data integrity)

**Step 3: Access Control**
- DO: Read-only access after forwarding
- Counselor: Full access to case
- Both can see classification notes
- Prevents conflicting updates

**Step 4: Notification Chain**
```python
# Notify all counselors
for counselor in User.objects.filter(role='counselor'):
    Notification.objects.create(
        user=counselor,
        title='New Major Case',
        message=f'Case {report.case_id} requires evaluation',
        report=report
    )
```

**Step 5: Dashboard Updates**
- Case removed from DO's pending queue
- Case appears in Counselor's evaluation queue
- Status badge changes to 'Classified'
- Both can track case progress

**Data Flow Diagram:**
```
DO Dashboard → Classification Form → Database Update → Notification Service
                                            ↓
                                    Counselor Dashboard
```

**Rollback Capability:**
- If Counselor finds issue, can return to DO
- Return creates new notification
- Status reverts to 'under_review'
- DO can reclassify

This design ensures smooth handoff with full traceability."

---

### Q4: What happens if report doesn't need counseling?

**ANSWER:**
"For minor cases that don't require counseling, DO has direct resolution options:

**DO's Resolution Path:**

**Option 1: Direct Warning**
- DO issues verbal/written warning
- Updates report status to 'resolved'
- Adds resolution notes
- Notifies student and parent
- Case closed

**Option 2: Parent Conference**
- DO schedules parent conference using DO Schedule
- Sets date, time, location
- Invites: Parent, Student, Adviser (optional)
- Documents conference outcome
- Updates status to 'resolved' after conference

**Option 3: Minor Sanction**
- DO issues minor sanction (e.g., detention, community service)
- Records sanction details
- Sets duration
- Monitors completion
- Updates status to 'resolved' when served

**System Process:**
```python
# DO resolves minor case
report.status = 'resolved'
report.resolution_notes = 'Parent conference held, student warned'
report.resolved_by = do_user
report.resolved_at = timezone.now()
report.save()

# Notify stakeholders
notify_student(report)
notify_parent(report)
notify_reporter(report)
```

**DO Schedule Feature:**
- DO can create schedule for:
  - Parent conferences
  - Student interviews
  - Follow-up meetings
- Schedule stored in DOSchedule table
- Notifications sent to all attendees
- Status tracking: Scheduled → Completed → Closed

**Benefits:**
- Fast resolution for minor cases
- Reduces Guidance workload
- Appropriate response to severity
- Still maintains documentation
- Analytics track resolution methods

**Statistics:**
- Approximately 60% of cases resolved by DO
- Average resolution time: 3-5 days
- 40% forwarded to Guidance for major cases"

---

## 🔵 D. GUIDANCE COUNSELING PROCESS

### Q1: How does Guidance create a counseling schedule?

**ANSWER:**
"Counseling schedule creation follows a structured workflow:

**Method 1: After Case Evaluation (Automatic)**

**Step 1: Counselor Evaluates Case**
- Selects case from 'Case Evaluation' queue
- Fills evaluation form:
  - Commission level (1st, 2nd, 3rd)
  - Intervention type
  - Status (Pending/Ongoing/Complete)
  - Evaluation notes

**Step 2: System Routes Based on Intervention**

**If Non-VPF Intervention:**
```python
# System automatically creates counseling schedule
schedule = CounselingSchedule.objects.create(
    evaluation=evaluation,
    counselor=counselor_user,
    student=report.reported_student,
    status='pending'
)
```

**Step 3: Counselor Sets Schedule Details**
- Access from 'Counseling Schedule' sidebar
- Set date and time
- Set location (Guidance Office, etc.)
- Add session notes
- Click 'Schedule'

**Method 2: Direct Schedule Creation (Manual)**
- Counselor can create schedule without evaluation
- For follow-up sessions
- For proactive counseling
- For student requests

**Schedule Form Fields:**
- Student Name * (searchable dropdown)
- Scheduled Date * (date picker)
- Scheduled Time * (time picker)
- Location * (text field)
- Session Type (Individual/Group/Family)
- Purpose/Notes (textarea)
- Status (Scheduled/Completed/Missed/Rescheduled)

**Validation:**
- Date cannot be in the past
- Time must be during school hours (7 AM - 5 PM)
- Cannot double-book counselor
- Student must exist in database

**After Scheduling:**
- Student notified with date/time/location
- Adviser notified
- Calendar reminder created
- Appears in Counselor's schedule view

**Schedule Management:**
- View all schedules in calendar format
- Filter by date, student, status
- Update status after session
- Add session notes
- Reschedule if needed"

---

### Q2: What details are stored when scheduling?

**ANSWER:**
"Our CounselingSchedule database stores comprehensive information:

**Core Schedule Information:**
- schedule_id (Primary Key)
- evaluation_id (Foreign Key to CaseEvaluation)
- counselor_id (Foreign Key to User)
- student_id (Foreign Key to User)
- scheduled_date (Date field)
- scheduled_time (Time field)
- location (Text: 'Guidance Office', 'Counseling Room', etc.)

**Session Details:**
- session_type ('individual', 'group', 'family')
- purpose (Text: reason for counseling)
- notes (Textarea: session notes, observations)
- duration (Integer: minutes, default 60)

**Status Tracking:**
- status ('scheduled', 'completed', 'missed', 'rescheduled', 'cancelled')
- status_updated_at (Timestamp)
- status_updated_by (Foreign Key to User)

