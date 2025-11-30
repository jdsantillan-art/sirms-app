# SIRMS - Visual DFD Guide
## Step-by-Step Process with Detailed Scenarios

---

## HOW TO READ THIS DOCUMENT

This guide provides:
1. **Visual diagrams** for each DFD level
2. **Real-world scenarios** showing how data flows
3. **Step-by-step walkthroughs** of each process
4. **Color-coded elements** for easy understanding

### Legend
- 🟦 **External Entity** (Square) - Users/Systems outside SIRMS
- 🟢 **Process** (Circle) - Actions that transform data
- 🟡 **Data Store** (Rectangle) - Databases/Files
- ➡️ **Data Flow** (Arrow) - Movement of information

---

## SCENARIO 1: Student Reports a Bullying Incident

### Step-by-Step Walkthrough

**Context:** Maria, a Grade 10 student, wants to report a bullying incident that happened in the cafeteria.

### CONTEXT DIAGRAM VIEW

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  🟦 Maria (Student)                                             │
│                                                                 │
│  What she does:                                                 │
│  1. Logs into SIRMS                                             │
│  2. Fills out incident report form                              │
│  3. Uploads photo evidence                                      │
│  4. Submits report                                              │
│                                                                 │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     │ ➡️ Incident Report Data:
                     │    - Reporter: Maria Santos
                     │    - Involved Student: John Doe
                     │    - Type: Bullying (Verbal)
                     │    - Date: Nov 30, 2025
                     │    - Time: 12:30 PM
                     │    - Location: Cafeteria
                     │    - Description: "John called me names..."
                     │    - Evidence: photo.jpg
                     │
                     ↓
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│                    🟢 SIRMS SYSTEM                              │
│                                                                 │
│  What it does:                                                  │
│  1. Validates Maria's login                                     │
│  2. Generates Case ID: 2025-0042                                │
│  3. Stores report in database                                   │
│  4. Sends notifications                                         │
│                                                                 │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     │ ➡️ Outputs:
                     │    - Confirmation to Maria
                     │    - Notification to Discipline Officer
                     │    - Case ID: 2025-0042
                     │
                     ↓
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  🟦 Mr. Cruz (Discipline Officer)                               │
│                                                                 │
│  What he receives:                                              │
│  - Notification: "New incident report 2025-0042"                │
│  - Action needed: Fact-check and classify                       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## SCENARIO 2: Discipline Officer Classifies the Case

### LEVEL 1 DFD VIEW

```
┌─────────────────────────────────────────────────────────────────┐
│  🟦 Mr. Cruz (DO)                                               │
│                                                                 │
│  Actions:                                                       │
│  1. Reviews Maria's report                                      │
│  2. Checks evidence photo                                       │
│  3. Interviews witnesses                                        │
│  4. Determines severity                                         │
│                                                                 │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     │ ➡️ Classification Request
                     │
                     ↓
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  🟢 3.0 CASE CLASSIFICATION & ROUTING                           │
│                                                                 │
│  Sub-processes:                                                 │
│  3.1 Fact-Check Report ✓                                        │
│  3.2 Review Evidence ✓ (Photo is clear)                        │
│  3.3 Classify Severity → MAJOR (Bullying is serious)           │
│  3.4 Route Case → Send to Guidance Counselor                    │
│  3.5 Update Status → "Classified"                               │
│                                                                 │
└────┬────────────────────────────────────┬─────────────────────┘
     │                                    │
     │ ➡️ Store Classification            │ ➡️ Read Report
     │                                    │
     ↓                                    ↓
┌─────────────────┐              ┌─────────────────┐
│                 │              │                 │
│  🟡 D3:         │              │  🟡 D2:         │
│  Classification │              │  Incident       │
│  Database       │              │  Database       │
│                 │              │                 │
│  Stores:        │              │  Contains:      │
│  - Case 2025-   │              │  - Full report  │
│    0042         │              │  - Evidence     │
│  - Severity:    │              │  - Status       │
│    MAJOR        │              │                 │
│  - Routed to:   │              │                 │
│    Counselor    │              │                 │
│                 │              │                 │
└─────────────────┘              └─────────────────┘
     │
     │ ➡️ Notification
     │
     ↓
┌─────────────────────────────────────────────────────────────────┐
│  🟦 Ms. Reyes (Guidance Counselor)                              │
│                                                                 │
│  Receives:                                                      │
│  - Notification: "Major case 2025-0042 assigned to you"        │
│  - Action needed: Evaluate and provide recommendation           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## SCENARIO 3: Counselor Evaluates the Case

### LEVEL 2 DFD VIEW (Case Evaluation Process)

```
┌─────────────────────────────────────────────────────────────────┐
│  🟦 Ms. Reyes (Counselor)                                       │
│                                                                 │
│  Actions:                                                       │
│  1. Opens case 2025-0042                                        │
│  2. Reviews incident details                                    │
│  3. Checks John's violation history                             │
│  4. Interviews Maria and John separately                        │
│  5. Makes determination                                         │
│                                                                 │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     │ ➡️ Evaluation Request
                     │
                     ↓
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  🟢 4.1 REVIEW MAJOR CASE                                       │
│                                                                 │
│  Reads from D2: Incident Database                               │
│  - Case ID: 2025-0042                                           │
│  - Type: Bullying (Verbal)                                      │
│  - Evidence: Photo showing incident                             │
│                                                                 │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     │ ➡️ Case Details
                     │
                     ↓
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  🟢 4.2 CHECK VIOLATION HISTORY                                 │
│                                                                 │
│  Queries D2 for John's past incidents:                          │
│  - 2025-0015: Fighting (Resolved)                               │
│  - 2024-0234: Disrespect to teacher (Counseling completed)      │
│  - 2024-0189: Bullying (Warning issued)                         │
│                                                                 │
│  ⚠️ FINDING: John is a REPEAT OFFENDER                          │
│                                                                 │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     │ ➡️ Repeat Offender Status
                     │
                     ↓
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  🟢 4.3 EVALUATE EVIDENCE                                       │
│                                                                 │
│  Assessment:                                                    │
│  ✓ Photo evidence is clear                                     │
│  ✓ Witness statements corroborate                              │
│  ✓ Both parties interviewed                                    │
│  ✓ Pattern of behavior established                             │
│                                                                 │
│  Conclusion: Evidence is SUFFICIENT                             │
│                                                                 │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     │ ➡️ Evidence Assessment
                     │
                     ↓
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  🟢 4.4 DETERMINE VERDICT                                       │
│                                                                 │
│  Based on:                                                      │
│  - Clear evidence                                               │
│  - Repeat offender status                                       │
│  - Severity of bullying                                         │
│                                                                 │
│  VERDICT: GUILTY                                                │
│                                                                 │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     │ ➡️ Verdict
                     │
                     ↓
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  🟢 4.5 PROVIDE RECOMMENDATION                                  │
│                                                                 │
│  Considering:                                                   │
│  - Repeat offender (3rd bullying incident)                      │
│  - Escalating behavior pattern                                  │
│  - Need for serious intervention                                │
│                                                                 │
│  RECOMMENDATION: RECOMMEND SANCTION                             │
│  (Suggest suspension + mandatory counseling)                    │
│                                                                 │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     │ ➡️ Store Evaluation
                     │
                     ↓
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  🟡 D4: EVALUATION DATABASE                                     │
│                                                                 │
│  Stores:                                                        │
│  - Case ID: 2025-0042                                           │
│  - Evaluated by: Ms. Reyes                                      │
│  - Verdict: GUILTY                                              │
│  - Recommendation: RECOMMEND SANCTION                           │
│  - Is Repeat Offender: YES                                      │
│  - Notes: "Third bullying incident. Pattern of escalating       │
│            behavior. Recommend 3-day suspension with            │
│            mandatory counseling sessions."                      │
│  - Evaluated at: Nov 30, 2025 3:45 PM                           │
│                                                                 │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     │ ➡️ Notification
                     │
                     ↓
┌─────────────────────────────────────────────────────────────────┐
│  🟦 Dr. Santos (Principal)                                      │
│                                                                 │
│  Receives:                                                      │
│  - Notification: "Case 2025-0042 evaluated - Sanction           │
│    recommended"                                                 │
│  - Action needed: Review and issue sanction                     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## SCENARIO 4: Complete System Flow (All Levels)

### FULL DATA FLOW DIAGRAM

```
═══════════════════════════════════════════════════════════════════
                        CONTEXT LEVEL
═══════════════════════════════════════════════════════════════════

🟦 Student ──Report──> 🟢 SIRMS ──Status──> 🟦 Student
🟦 Teacher ──Concern──> 🟢 SIRMS ──Analytics──> 🟦 Teacher
🟦 DO ──Classification──> 🟢 SIRMS ──Queue──> 🟦 DO
🟦 Counselor ──Evaluation──> 🟢 SIRMS ──Cases──> 🟦 Counselor
🟦 Principal ──Sanction──> 🟢 SIRMS ──Reports──> 🟦 Principal

═══════════════════════════════════════════════════════════════════
                         LEVEL 1
═══════════════════════════════════════════════════════════════════

🟦 Student
    │
    │ Login Credentials
    ↓
🟢 1.0 User Authentication ←──→ 🟡 D1: User DB
    │
    │ Access Token
    ↓
🟦 Student
    │
    │ Incident Details
    ↓
🟢 2.0 Incident Reporting ──→ 🟡 D2: Incident DB
    │                          ↓
    │ Confirmation             │ Pending Reports
    ↓                          ↓
🟦 Student              🟦 DO
                              │
                              │ Classification
                              ↓
                        🟢 3.0 Case Classification ──→ 🟡 D3: Classification DB
                              │
                              ├─ Minor ──→ 🟦 DO (Handle)
                              │
                              └─ Major ──→ 🟦 Counselor
                                          │
                                          │ Evaluation
                                          ↓
                                    🟢 4.0 Case Evaluation ──→ 🟡 D4: Evaluation DB
                                          │
                                          │ Recommendation
                                          ↓
                                    🟦 Principal
                                          │
                                          │ Sanction Decision
                                          ↓
                                    🟢 5.0 Sanction Management
                                          │
                                          │ Final Verdict
                                          ↓
                                    🟡 D2: Incident DB (Update)

═══════════════════════════════════════════════════════════════════
                         LEVEL 2 (Incident Reporting)
═══════════════════════════════════════════════════════════════════

🟦 Student
    │
    │ Reporter Info
    ↓
🟢 2.1 Validate Reporter ←──→ 🟡 D1: User DB
    │
    │ Valid Reporter
    ↓
🟢 2.2 Collect Incident Details
    │
    │ Incident Data
    ↓
🟢 2.3 Upload Evidence
    │
    │ Complete Report
    ↓
🟢 2.4 Generate Case ID
    │
    │ Case ID (2025-0042)
    ↓
🟢 2.5 Store Incident ──→ 🟡 D2: Incident DB
    │
    │ Report Stored
    ↓
🟢 2.6 Notify Stakeholders ──→ 🟡 D6: Notification DB
    │
    ├──→ 🟦 DO (New report notification)
    ├──→ 🟦 Student (Confirmation)
    └──→ 🟦 Reported Student (Notification)

═══════════════════════════════════════════════════════════════════
                         LEVEL 2 (Case Classification)
═══════════════════════════════════════════════════════════════════

🟦 DO
    │
    │ View Request
    ↓
🟢 3.1 Fact-Check Report ←──→ 🟡 D2: Incident DB
    │
    │ Fact-Checked
    ↓
🟢 3.2 Review Evidence
    │
    │ Evidence Status
    ↓
🟢 3.3 Classify Severity
    │
    │ Classification (Minor/Major)
    ↓
🟡 D3: Classification DB
    │
    ↓
🟢 3.4 Route Case
    │
    ├─ Minor ──→ 🟦 DO
    │
    └─ Major ──→ 🟢 3.5 Update Status ──→ 🟡 D6: Notification DB
                      │
                      └──→ 🟦 Counselor

═══════════════════════════════════════════════════════════════════
                         LEVEL 2 (Case Evaluation)
═══════════════════════════════════════════════════════════════════

🟦 Counselor
    │
    │ View Request
    ↓
🟢 4.1 Review Major Case ←──→ 🟡 D2: Incident DB
    │
    │ Case Details
    ↓
🟢 4.2 Check Violation History ←──→ 🟡 D2: Incident DB
    │
    │ Repeat Offender Status
    ↓
🟢 4.3 Evaluate Evidence
    │
    │ Evidence Assessment
    ↓
🟢 4.4 Determine Verdict
    │
    │ Verdict (Guilty/Not Guilty/etc.)
    ↓
🟢 4.5 Provide Recommendation
    │
    │ Recommendation
    ↓
🟡 D4: Evaluation DB
    │
    ↓
🟢 4.6 Assign Intervention
    │
    ├──→ Schedule Counseling ──→ 🟡 D5: Schedule DB
    ├──→ Assign VPF ──→ 🟦 ESP Teacher
    └──→ Refer to Principal ──→ 🟦 Principal
```

---

## REAL-WORLD SCENARIOS

### Scenario A: Minor Incident (Handled by DO)

**Case:** Student late to class 3 times

```
Student Reports → DO Reviews → Classifies as MINOR
                                    ↓
                            DO Handles Directly
                                    ↓
                            Issues Warning
                                    ↓
                            Case Resolved
```

**Data Flow:**
1. Student submits report
2. DO fact-checks (confirms tardiness)
3. DO classifies as "minor"
4. DO issues verbal warning
5. Status updated to "resolved"
6. Student notified

---

### Scenario B: Major Incident (Requires Counseling)

**Case:** First-time physical altercation

```
Teacher Reports → DO Reviews → Classifies as MAJOR
                                    ↓
                            Routes to Counselor
                                    ↓
                    Counselor Evaluates → Verdict: GUILTY
                                    ↓
                    Recommendation: COUNSELING ONLY
                                    ↓
                            Schedules 3 Sessions
                                    ↓
                            Case Monitored
```

**Data Flow:**
1. Teacher submits behavioral concern
2. DO fact-checks and classifies as "major"
3. Counselor receives notification
4. Counselor evaluates (first offense)
5. Recommends counseling intervention
6. Schedules counseling sessions
7. Monitors progress

---

### Scenario C: Serious Incident (Requires Sanction)

**Case:** Repeat offender - Bullying (3rd time)

```
Student Reports → DO Reviews → Classifies as MAJOR
                                    ↓
                            Routes to Counselor
                                    ↓
                    Counselor Evaluates → Checks History
                                    ↓
                            Repeat Offender Found
                                    ↓
                    Verdict: GUILTY
                    Recommendation: SANCTION
                                    ↓
                            Routes to Principal
                                    ↓
                    Principal Reviews → Issues Suspension
                                    ↓
                            Parents Notified
                                    ↓
                            Case Closed
```

**Data Flow:**
1. Student submits report with evidence
2. DO fact-checks and classifies as "major"
3. Counselor receives case
4. Counselor checks violation history (finds 2 prior incidents)
5. Counselor determines verdict: GUILTY
6. Counselor recommends: SANCTION
7. Principal receives notification
8. Principal reviews and issues 3-day suspension
9. Parents notified via DO schedule (parent conference)
10. Case status updated to "closed"

---

### Scenario D: VPF Intervention

**Case:** Student needs values formation

```
Counselor Evaluates → Recommends VPF
                            ↓
                    Assigns to ESP Teacher
                            ↓
                    ESP Teacher Creates Schedule
                            ↓
                    Student Attends VPF Sessions
                            ↓
                    Progress Monitored
                            ↓
                    VPF Completed
                            ↓
                    Case Resolved
```

**Data Flow:**
1. Counselor evaluates case
2. Recommends VPF intervention
3. Creates VPF case assignment
4. ESP Teacher receives notification
5. ESP Teacher schedules VPF sessions
6. Student attends sessions
7. ESP Teacher updates progress
8. VPF marked as completed
9. Case status updated to "resolved"

---

## DATA FLOW TIMING

### Timeline Example: From Report to Resolution

```
Day 1 (Monday 9:00 AM)
├─ Student submits report
├─ System generates Case ID: 2025-0042
└─ DO receives notification

Day 1 (Monday 2:00 PM)
├─ DO reviews and fact-checks
├─ DO classifies as MAJOR
└─ Counselor receives notification

Day 2 (Tuesday 10:00 AM)
├─ Counselor reviews case
├─ Counselor checks violation history
└─ Counselor schedules interview

Day 3 (Wednesday 1:00 PM)
├─ Counselor interviews student
├─ Counselor evaluates evidence
├─ Counselor determines verdict: GUILTY
├─ Counselor recommends: SANCTION
└─ Principal receives notification

Day 4 (Thursday 9:00 AM)
├─ Principal reviews evaluation
├─ Principal issues 3-day suspension
├─ DO schedules parent conference
└─ All parties notified

Day 5 (Friday 2:00 PM)
├─ Parent conference held
├─ Suspension begins Monday
└─ Case status: SANCTIONED

Day 10 (Next Friday)
├─ Suspension completed
├─ Follow-up counseling scheduled
└─ Case status: RESOLVED
```

---

## SUMMARY

This visual guide demonstrates:

1. **Context Diagram** - Shows SIRMS interacting with all external users
2. **Level 1 DFD** - Shows 7 major processes and data stores
3. **Level 2 DFD** - Shows detailed sub-processes for reporting, classification, and evaluation
4. **Real Scenarios** - Shows actual data flows with realistic examples
5. **Timeline** - Shows how data moves through the system over time

Each level provides more detail while maintaining consistency with the higher levels.

---

**Created By:** Kiro AI Assistant  
**Date:** November 30, 2025  
**Purpose:** Educational guide for understanding SIRMS data flows
