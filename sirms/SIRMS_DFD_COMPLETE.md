# SIRMS - Complete Data Flow Diagram (DFD)
## Student Incident Reporting Management System

---

## TABLE OF CONTENTS
1. [Context Diagram (Level 0)](#context-diagram-level-0)
2. [Level 1 DFD](#level-1-dfd)
3. [Level 2 DFD - Incident Reporting Process](#level-2-dfd---incident-reporting-process)
4. [Level 2 DFD - Case Management Process](#level-2-dfd---case-management-process)
5. [Data Dictionary](#data-dictionary)

---

## CONTEXT DIAGRAM (LEVEL 0)

### Overview
The Context Diagram shows the SIRMS system as a single process with all external entities that interact with it.

### External Entities
1. **Student** - Reports incidents, views their reports and schedules
2. **Teacher** - Reports behavioral concerns, views advisee records
3. **Discipline Officer (DO)** - Manages incident classification and routing
4. **Guidance Counselor** - Evaluates cases, schedules counseling sessions
5. **Principal** - Reviews evaluated cases, issues sanctions
6. **ESP Teacher/VPF Coordinator** - Manages Values Reflective Formation programs

### Context Diagram Representation

```
┌─────────────┐
│   Student   │
└──────┬──────┘
       │
       │ Incident Report
       │ Violation History Request
       ↓
       │ Report Status
       │ Counseling Schedule
       │ Notifications
       ↑
       │
┌──────────────────────────────────────────────────────────────┐
│                                                              │
│                    SIRMS SYSTEM                              │
│         (Student Incident Reporting                          │
│           Management System)                                 │
│                                                              │
└──────────────────────────────────────────────────────────────┘
       ↑                    ↑                    ↑
       │                    │                    │
       │ Behavioral         │ Case               │ Evaluated
       │ Concern            │ Classification     │ Cases
       │                    │                    │
       ↓                    ↓                    ↓
       │ Reports            │ Routing            │ Sanctions
       │ Analytics          │ Decisions          │ Final Verdicts
       │                    │                    │
┌──────┴──────┐      ┌─────┴──────┐      ┌─────┴──────┐
│   Teacher   │      │ Discipline │      │ Principal  │
│             │      │  Officer   │      │            │
└─────────────┘      └────────────┘      └────────────┘
       ↑                    ↑                    ↑
       │                    │                    │
       │ Case               │ VPF                │ Analytics
       │ Evaluation         │ Assignments        │ Reports
       │                    │                    │
       ↓                    ↓                    ↓
       │ Counseling         │ VPF                │ System
       │ Schedule           │ Schedule           │ Reports
       │ Recommendations    │ Progress           │
       │                    │                    │
┌──────┴──────┐      ┌─────┴──────┐
│  Guidance   │      │    ESP     │
│ Counselor   │      │  Teacher   │
└─────────────┘      └────────────┘
```

### Data Flows (Context Level)

**Incoming Data Flows:**
- Student → SIRMS: Incident Report, Violation History Request
- Teacher → SIRMS: Behavioral Concern, Advisee Records Request
- Discipline Officer → SIRMS: Classification Decision, Evidence Status
- Guidance Counselor → SIRMS: Case Evaluation, Counseling Schedule
- Principal → SIRMS: Sanction Decision, Final Verdict
- ESP Teacher → SIRMS: VPF Schedule, Progress Update

**Outgoing Data Flows:**
- SIRMS → Student: Report Status, Counseling Schedule, Notifications
- SIRMS → Teacher: Reports, Analytics, Advisee Records
- SIRMS → Discipline Officer: Pending Reports, Classification Queue
- SIRMS → Guidance Counselor: Major Cases, Evaluation Queue
- SIRMS → Principal: Evaluated Cases, Sanction Recommendations
- SIRMS → ESP Teacher: VPF Assignments, Student Progress

---

## LEVEL 1 DFD

### Overview
Level 1 breaks down the SIRMS system into 7 major processes.

### Major Processes

1. **1.0 User Authentication & Authorization**
2. **2.0 Incident Reporting**
3. **3.0 Case Classification & Routing**
4. **4.0 Case Evaluation & Counseling**
5. **5.0 Sanction Management**
6. **6.0 Schedule Management**
7. **7.0 Analytics & Reporting**

### Data Stores

- **D1: User Database** - Stores user accounts and roles
- **D2: Incident Database** - Stores all incident reports
- **D3: Classification Database** - Stores case classifications
- **D4: Evaluation Database** - Stores case evaluations
- **D5: Schedule Database** - Stores counseling and VPF schedules
- **D6: Notification Database** - Stores system notifications
- **D7: Analytics Database** - Stores analytics and reports

### Level 1 DFD Representation

```
[Student] ──Login Credentials──> (1.0 User Authentication) ──Access Token──> [Student]
                                         │
                                         ↓
                                    [D1: User DB]
                                         ↑
                                         │
                                    User Data
                                         │
                                         ↓

[Student] ──Incident Details──> (2.0 Incident Reporting) ──Confirmation──> [Student]
[Teacher] ──Behavioral Concern──>       │
                                        ↓
                                   Store Report
                                        │
                                        ↓
                                  [D2: Incident DB]
                                        │
                                        ↓
                                   Pending Reports
                                        │
                                        ↓
[DO] <──Pending Queue── (3.0 Case Classification) ──Classification──> [D3: Classification DB]
                                        │
                                        ↓
                                   Routing Decision
                                        │
                        ┌───────────────┴───────────────┐
                        │                               │
                   Minor Cases                     Major Cases
                        │                               │
                        ↓                               ↓
                   Handle by DO                  [Counselor]
                                                        │
                                                        ↓
                                            (4.0 Case Evaluation)
                                                        │
                                                        ↓
                                                  Evaluation
                                                        │
                                                        ↓
                                              [D4: Evaluation DB]
                                                        │
                                                        ↓
                                                Recommendation
                                                        │
                                                        ↓
[Principal] <──Evaluated Cases── (5.0 Sanction Management) ──Sanction──> [D2: Incident DB]
                                                        │
                                                        ↓
                                                  Final Verdict
                                                        │
                                                        ↓

[Counselor] ──Schedule Request──> (6.0 Schedule Management) ──Schedule Confirmation──> [Counselor]
[ESP Teacher] ──VPF Schedule──>           │
                                          ↓
                                    Store Schedule
                                          │
                                          ↓
                                   [D5: Schedule DB]
                                          │
                                          ↓
                                    Schedule Data
                                          │
                                          ↓
                                      [Student]

[All Users] ──Analytics Request──> (7.0 Analytics & Reporting) ──Reports/Charts──> [All Users]
                                          │
                                          ↑
                                    Read Data
                                          │
                                   [D2: Incident DB]
                                   [D3: Classification DB]
                                   [D4: Evaluation DB]
                                   [D5: Schedule DB]
                                          │
                                          ↓
                                    Store Analytics
                                          │
                                          ↓
                                   [D7: Analytics DB]
```

### Process Descriptions (Level 1)

#### 1.0 User Authentication & Authorization
**Purpose:** Manage user login, registration, and role-based access control

**Inputs:**
- Login Credentials (username, password)
- Registration Data (name, email, role, employee_id)
- OAuth Token (Google authentication)

**Outputs:**
- Access Token
- User Session
- Role Permissions

**Data Stores:**
- D1: User Database (Read/Write)

---

#### 2.0 Incident Reporting
**Purpose:** Allow students and teachers to submit incident reports

**Inputs:**
- Incident Details (reporter info, student info, incident type, date, time, description)
- Evidence Files (photos, documents)
- Behavioral Concerns (from teachers)

**Outputs:**
- Case ID
- Confirmation Message
- Notification to DO

**Data Stores:**
- D2: Incident Database (Write)
- D6: Notification Database (Write)

---

#### 3.0 Case Classification & Routing
**Purpose:** Discipline Officer classifies incidents and routes them appropriately

**Inputs:**
- Pending Reports
- Evidence Status
- Classification Decision (minor/major)

**Outputs:**
- Routing Decision (DO handles / Send to Counselor)
- Classification Record
- Notification to Counselor (if major)

**Data Stores:**
- D2: Incident Database (Read)
- D3: Classification Database (Write)
- D6: Notification Database (Write)

---

#### 4.0 Case Evaluation & Counseling
**Purpose:** Guidance Counselor evaluates major cases and provides recommendations

**Inputs:**
- Major Cases
- Evaluation Notes
- Verdict (guilty, not guilty, insufficient evidence)
- Recommendation (counseling, sanction, monitoring, resolved)

**Outputs:**
- Case Evaluation
- Counseling Recommendation
- VPF Assignment (if needed)
- Notification to Principal (if sanction recommended)

**Data Stores:**
- D2: Incident Database (Read)
- D4: Evaluation Database (Write)
- D6: Notification Database (Write)

---

#### 5.0 Sanction Management
**Purpose:** Principal reviews evaluated cases and issues sanctions

**Inputs:**
- Evaluated Cases
- Sanction Decision (warning, suspension, expulsion)
- Duration
- Reason

**Outputs:**
- Sanction Record
- Final Verdict
- Notification to Student
- Case Closure

**Data Stores:**
- D2: Incident Database (Update)
- D4: Evaluation Database (Read)
- D6: Notification Database (Write)

---

#### 6.0 Schedule Management
**Purpose:** Manage counseling sessions and VPF schedules

**Inputs:**
- Counseling Schedule Request
- VPF Schedule Request
- DO Schedule Request (parent conferences)
- Schedule Updates (completed, missed, rescheduled)

**Outputs:**
- Schedule Confirmation
- Schedule Reminders
- Notification to Students

**Data Stores:**
- D5: Schedule Database (Read/Write)
- D6: Notification Database (Write)

---

#### 7.0 Analytics & Reporting
**Purpose:** Generate reports, charts, and analytics for all users

**Inputs:**
- Analytics Request
- Date Range
- Filter Criteria (grade, violation type, status)

**Outputs:**
- Trend Charts
- Grade Distribution
- Violation Type Analysis
- Resolution Rate
- Excel Reports

**Data Stores:**
- D2: Incident Database (Read)
- D3: Classification Database (Read)
- D4: Evaluation Database (Read)
- D5: Schedule Database (Read)
- D7: Analytics Database (Write)

---

## LEVEL 2 DFD - INCIDENT REPORTING PROCESS

### Overview
This breaks down Process 2.0 (Incident Reporting) into sub-processes.

### Sub-Processes

- **2.1 Validate Reporter**
- **2.2 Collect Incident Details**
- **2.3 Upload Evidence**
- **2.4 Generate Case ID**
- **2.5 Store Incident**
- **2.6 Notify Stakeholders**

### Level 2 DFD Representation

```
[Student/Teacher] ──Reporter Info──> (2.1 Validate Reporter) ──Valid Reporter──> (2.2 Collect Details)
                                            │
                                            ↓
                                       Check User
                                            │
                                            ↓
                                      [D1: User DB]

(2.2 Collect Details) <──Incident Form Data── [Student/Teacher]
        │
        ↓
   Incident Data
        │
        ↓
(2.3 Upload Evidence) <──Evidence Files── [Student/Teacher]
        │
        ↓
   Complete Report
        │
        ↓
(2.4 Generate Case ID)
        │
        ↓
   Case ID (YYYY-####)
        │
        ↓
(2.5 Store Incident) ──Store──> [D2: Incident DB]
        │
        ↓
   Report Stored
        │
        ↓
(2.6 Notify Stakeholders) ──Create Notifications──> [D6: Notification DB]
        │
        ├──> [DO] (New Report Notification)
        ├──> [Reporter] (Confirmation)
        └──> [Student] (If reported student exists)
```

### Sub-Process Descriptions

#### 2.1 Validate Reporter
**Input:** Reporter credentials, role
**Process:** Verify user is logged in and has permission to report
**Output:** Valid reporter confirmation
**Data Store:** D1: User Database (Read)

#### 2.2 Collect Incident Details
**Input:** 
- Reporter name (first, middle, last)
- Involved students
- Student gender
- Curriculum, grade level, section, teacher
- Incident date and time
- Incident type
- Description
- Bullying type (if applicable)

**Process:** Validate all required fields, format data
**Output:** Complete incident data

#### 2.3 Upload Evidence
**Input:** Evidence files (photos, documents, videos)
**Process:** Validate file type and size, store in file system
**Output:** Evidence file path

#### 2.4 Generate Case ID
**Input:** Current year, incident count
**Process:** Generate unique case ID in format YYYY-####
**Output:** Case ID (e.g., 2025-0001)

#### 2.5 Store Incident
**Input:** Complete report with case ID
**Process:** Save to database with status='pending'
**Output:** Stored report
**Data Store:** D2: Incident Database (Write)

#### 2.6 Notify Stakeholders
**Input:** Stored report
**Process:** Create notifications for relevant users
**Output:** Notifications sent
**Data Store:** D6: Notification Database (Write)

**Notifications Created:**
- All Discipline Officers: "New incident report requires fact-checking"
- Reporter: "Your report has been submitted successfully"
- Reported Student (if exists): "You have been mentioned in an incident report"

---

## LEVEL 2 DFD - CASE MANAGEMENT PROCESS

### Overview
This breaks down Process 3.0 (Case Classification) and Process 4.0 (Case Evaluation).

### Sub-Processes for 3.0 Case Classification

- **3.1 Fact-Check Report**
- **3.2 Review Evidence**
- **3.3 Classify Severity**
- **3.4 Route Case**
- **3.5 Update Status**

### Level 2 DFD Representation (Classification)

```
[DO] ──View Request──> (3.1 Fact-Check Report) <──Pending Reports── [D2: Incident DB]
                              │
                              ↓
                         Fact-Checked
                              │
                              ↓
[DO] ──Evidence Review──> (3.2 Review Evidence) <──Evidence Files── [File System]
                              │
                              ↓
                         Evidence Status
                         (clear/insufficient)
                              │
                              ↓
[DO] ──Classification──> (3.3 Classify Severity)
                              │
                              ↓
                         Severity Decision
                         (minor/major)
                              │
                              ↓
                         Store Classification
                              │
                              ↓
                      [D3: Classification DB]
                              │
                              ↓
(3.4 Route Case)
        │
        ├──Minor──> [DO] (Handle directly)
        │
        └──Major──> (3.5 Update Status) ──Notify──> [Counselor]
                              │
                              ↓
                      [D6: Notification DB]
```

### Sub-Processes for 4.0 Case Evaluation

- **4.1 Review Major Case**
- **4.2 Check Violation History**
- **4.3 Evaluate Evidence**
- **4.4 Determine Verdict**
- **4.5 Provide Recommendation**
- **4.6 Assign Intervention**

### Level 2 DFD Representation (Evaluation)

```
[Counselor] ──View Request──> (4.1 Review Major Case) <──Major Cases── [D2: Incident DB]
                                      │
                                      ↓
                                 Case Details
                                      │
                                      ↓
(4.2 Check Violation History) <──Student History── [D2: Incident DB]
                                      │
                                      ↓
                              Repeat Offender Status
                                      │
                                      ↓
[Counselor] ──Evaluation──> (4.3 Evaluate Evidence)
                                      │
                                      ↓
                              Evidence Assessment
                                      │
                                      ↓
(4.4 Determine Verdict)
        │
        ├──> Guilty
        ├──> Not Guilty
        ├──> Insufficient Evidence
        └──> Pending Investigation
                │
                ↓
(4.5 Provide Recommendation)
        │
        ├──> Counseling Only
        ├──> Recommend Sanction
        ├──> Monitoring Required
        └──> Case Resolved
                │
                ↓
         Store Evaluation
                │
                ↓
      [D4: Evaluation DB]
                │
                ↓
(4.6 Assign Intervention)
        │
        ├──> Schedule Counseling ──> [D5: Schedule DB]
        ├──> Assign VPF ──> [ESP Teacher]
        └──> Refer to Principal ──> [Principal]
                │
                ↓
         Create Notifications
                │
                ↓
      [D6: Notification DB]
```

### Sub-Process Descriptions (Classification)

#### 3.1 Fact-Check Report
**Input:** Pending incident reports
**Process:** DO reviews report details for accuracy and completeness
**Output:** Fact-checked report
**Data Store:** D2: Incident Database (Read)

#### 3.2 Review Evidence
**Input:** Evidence files attached to report
**Process:** DO reviews evidence quality and sufficiency
**Output:** Evidence status (clear, insufficient, pending)
**Data Store:** D2: Incident Database (Update)

#### 3.3 Classify Severity
**Input:** Fact-checked report, evidence status
**Process:** DO determines if case is minor or major based on incident type and severity
**Output:** Classification (minor/major)
**Data Store:** D3: Classification Database (Write)

#### 3.4 Route Case
**Input:** Classification decision
**Process:** Route case to appropriate handler
**Output:** 
- Minor cases: Handled by DO directly
- Major cases: Sent to Guidance Counselor

#### 3.5 Update Status
**Input:** Routing decision
**Process:** Update report status and notify relevant parties
**Output:** Status update, notifications
**Data Stores:** 
- D2: Incident Database (Update)
- D6: Notification Database (Write)

### Sub-Process Descriptions (Evaluation)

#### 4.1 Review Major Case
**Input:** Major cases from classification
**Process:** Counselor reviews case details, incident type, and context
**Output:** Case understanding
**Data Store:** D2: Incident Database (Read)

#### 4.2 Check Violation History
**Input:** Student ID from report
**Process:** Query past violations for pattern detection
**Output:** Repeat offender status, related cases
**Data Store:** D2: Incident Database (Read - violation history)

#### 4.3 Evaluate Evidence
**Input:** Evidence files, witness statements, investigation notes
**Process:** Counselor assesses evidence quality and credibility
**Output:** Evidence assessment

#### 4.4 Determine Verdict
**Input:** Evidence assessment, violation history
**Process:** Counselor makes determination of guilt
**Output:** Verdict (guilty, not guilty, insufficient evidence, pending)

#### 4.5 Provide Recommendation
**Input:** Verdict, severity, student history
**Process:** Counselor recommends appropriate intervention
**Output:** Recommendation (counseling, sanction, monitoring, resolved)
**Data Store:** D4: Evaluation Database (Write)

#### 4.6 Assign Intervention
**Input:** Recommendation
**Process:** Create appropriate intervention based on recommendation
**Output:** 
- Counseling schedule
- VPF assignment
- Sanction referral to Principal
**Data Stores:**
- D5: Schedule Database (Write)
- D6: Notification Database (Write)

---

## DATA DICTIONARY

### Data Stores

#### D1: User Database (CustomUser)
**Description:** Stores all user accounts and authentication information

**Fields:**
- user_id (PK)
- username
- password (hashed)
- email
- first_name
- last_name
- role (student, teacher, do, counselor, principal, esp_teacher)
- employee_id
- grade_level (for students)
- section (for students)
- is_active
- date_joined

---

#### D2: Incident Database (IncidentReport)
**Description:** Stores all incident reports and their details

**Fields:**
- report_id (PK)
- case_id (unique, format: YYYY-####)
- reporter_id (FK to User)
- reporter_first_name
- reporter_middle_name
- reporter_last_name
- involved_students (text)
- student_gender
- reported_student_id (FK to User)
- curriculum_id (FK to Curriculum)
- grade_level
- section_name
- teacher_name
- incident_date
- incident_time
- incident_type_id (FK to IncidentType)
- description
- evidence (file path)
- status (pending, under_review, classified, evaluated, sanctioned, resolved, closed)
- evidence_status (pending, clear, insufficient)
- evidence_notes
- created_at
- updated_at

---

#### D3: Classification Database (Classification)
**Description:** Stores case classifications made by Discipline Officers

**Fields:**
- classification_id (PK)
- report_id (FK to IncidentReport)
- classified_by_id (FK to User - DO)
- severity (minor, major)
- internal_notes
- classified_at

---

#### D4: Evaluation Database (CaseEvaluation)
**Description:** Stores case evaluations made by Guidance Counselors

**Fields:**
- evaluation_id (PK)
- report_id (FK to IncidentReport)
- evaluated_by_id (FK to User - Counselor)
- evaluation_notes
- recommendation (counseling, sanction, monitoring, resolved)
- verdict (pending, guilty, not_guilty, insufficient_evidence)
- verdict_notes
- is_repeat_offender
- evaluated_at

---

#### D5: Schedule Database
**Description:** Stores counseling sessions, VPF schedules, and DO schedules

**Tables:**
- CounselingSchedule
- VPFSchedule
- DOSchedule

**CounselingSchedule Fields:**
- schedule_id (PK)
- evaluation_id (FK to CaseEvaluation)
- counselor_id (FK to User)
- student_id (FK to User)
- scheduled_date
- location
- notes
- status (scheduled, completed, missed, rescheduled)
- created_at
- updated_at

**VPFSchedule Fields:**
- schedule_id (PK)
- vpf_case_id (FK to VPFCase)
- esp_teacher_id (FK to User)
- counselor_assigned_id (FK to Counselor)
- scheduled_date
- location
- notes
- status (scheduled, completed, missed, rescheduled)
- created_at
- updated_at

**DOSchedule Fields:**
- schedule_id (PK)
- report_id (FK to IncidentReport)
- discipline_officer_id (FK to User)
- student_id (FK to User)
- schedule_type (parent_conference, interview, follow_up)
- scheduled_date
- location
- attendees
- purpose
- notes
- status (scheduled, completed, cancelled, rescheduled, no_show)
- created_at
- updated_at

---

#### D6: Notification Database (Notification)
**Description:** Stores system notifications for users

**Fields:**
- notification_id (PK)
- user_id (FK to User)
- title
- message
- report_id (FK to IncidentReport, optional)
- is_read
- created_at

---

#### D7: Analytics Database (ReportAnalytics)
**Description:** Stores pre-computed analytics data

**Fields:**
- analytics_id (PK)
- date_range_start
- date_range_end
- total_reports
- minor_violations
- major_violations
- resolved_cases
- pending_cases
- most_common_violation
- grade_with_most_violations
- generated_by_id (FK to User)
- generated_at

---

### Data Flows

#### Incident Report Data Flow
**Source:** Student/Teacher
**Destination:** Incident Database
**Data Elements:**
- Reporter information (name, role)
- Student information (name, gender, grade, section)
- Incident details (type, date, time, description)
- Evidence files
- Academic context (curriculum, teacher)

#### Classification Data Flow
**Source:** Discipline Officer
**Destination:** Classification Database
**Data Elements:**
- Report ID
- Severity classification (minor/major)
- Routing decision
- Internal notes
- Evidence status

#### Evaluation Data Flow
**Source:** Guidance Counselor
**Destination:** Evaluation Database
**Data Elements:**
- Report ID
- Evaluation notes
- Verdict (guilty, not guilty, etc.)
- Recommendation (counseling, sanction, etc.)
- Repeat offender flag
- Related cases

#### Schedule Data Flow
**Source:** Counselor/ESP Teacher/DO
**Destination:** Schedule Database
**Data Elements:**
- Student ID
- Counselor/Teacher ID
- Scheduled date and time
- Location
- Purpose/Notes
- Status

#### Notification Data Flow
**Source:** System (triggered by various processes)
**Destination:** Notification Database
**Data Elements:**
- User ID (recipient)
- Title
- Message
- Related report ID
- Timestamp

---

## SUMMARY

This complete DFD documentation provides:

1. **Context Diagram** - High-level view of SIRMS with all external entities
2. **Level 1 DFD** - 7 major processes with data stores
3. **Level 2 DFD** - Detailed breakdown of Incident Reporting and Case Management
4. **Data Dictionary** - Complete description of all data stores and flows

The SIRMS system manages the complete lifecycle of student incident reports from submission through classification, evaluation, intervention, and resolution, with comprehensive tracking and analytics capabilities.

---

**Document Version:** 1.0  
**Last Updated:** November 30, 2025  
**Created By:** Kiro AI Assistant
