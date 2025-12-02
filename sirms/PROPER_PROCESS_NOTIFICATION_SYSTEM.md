# 🎯 SIRMS - Proper Process & Notification System Specification

## Overview
This document outlines the complete incident reporting process with proper notifications for both **student** and **teacher** involved parties.

---

## 📋 CURRENT SYSTEM vs PROPER SYSTEM

### Current System Limitations:
- ❌ Only handles students as involved parties
- ❌ No teacher-as-involved-party support
- ❌ Limited notification logic
- ❌ No confidential report handling
- ❌ No "reporter is victim" checkbox
- ❌ No party type distinction

### Proper System Requirements:
- ✅ Handle both students AND teachers as involved parties
- ✅ Support multiple involved parties
- ✅ Reporter can be victim (auto-add as involved party)
- ✅ Confidential reports for teacher incidents
- ✅ Smart notification routing based on party type
- ✅ Unknown involved parties (notify after DO confirmation)
- ✅ Web + Email notifications

---

## 🔄 COMPLETE WORKFLOW

### Phase 1: Report Submission

#### Form Fields:

**1. Reporter Information**
```
- First Name * (required)
- Middle Name (optional)
- Last Name * (required)
- Gender (optional)
- Role * (Student / Teacher / Staff)
- [✓] Reporter is Victim (checkbox)
```

**2. Involved Party(ies)**
```
- Party Type * (Student / Teacher)
- Name / ID / Email (optional if unknown)
- [If Student]:
  - Curriculum (optional)
  - Grade Level (optional)
  - Section (optional)
  - Adviser (auto-filled)
- [If Teacher]:
  - Department (optional)
  - Grade Level Taught (optional)
- [✓] Confidential (checkbox - recommended for teacher incidents)
```

**3. Incident Details**
```
- Date of Incident * (required)
- Time of Incident * (required)
- Violation Type * (required)
- Description * (required, min 20 chars)
- Evidence (optional, photos/documents)
```

#### Submission Logic:
```python
1. Save report to database
2. Generate Case ID (YYYY-####)
3. Store evidence files
4. Trigger notifications:
   
   ALWAYS NOTIFY:
   - All DOs (Web + Email): "New incident report requires fact-checking"
   
   IF reporter is student:
   - Reporter's adviser (Web + Email): "Your advisee reported an incident"
   
   IF "Reporter is Victim" checked:
   - Add reporter as involved party automatically
   
   IF involved party is known AND is student:
   - Student (Web + Email): "You've been mentioned in an incident report"
   - Student's adviser (Web + Email): "Your advisee is involved in an incident"
   
   IF involved party is known AND is teacher:
   - DO only (confidential)
   - Guidance (Web + Email): "Teacher involved in incident report"
   
   IF involved party is unknown:
   - No notification yet (wait for DO confirmation)
```

---

### Phase 2: DO Fact-Check & Classification

#### DO Actions:
1. **Review Report** - Check validity and evidence
2. **Confirm/Add Involved Parties** - If unknown, add them now
3. **Classify Severity**:
   - **DO Only** (Minor) - Handle internally
   - **Refer to Guidance** (Major) - Forward for evaluation

#### Notification Logic:

**When DO confirms involved party:**
```python
IF involved party is student:
  NOTIFY:
  - Student (Web + Email): "You've been confirmed as involved in case {case_id}"
  - Student's adviser (Web + Email): "Your advisee {student_name} is involved in case {case_id}"

IF involved party is teacher:
  NOTIFY:
  - DO (internal note)
  - Guidance (Web + Email): "Teacher {teacher_name} confirmed in case {case_id}"
  - NO notification to teacher yet (confidential until investigation)
```

**When DO classifies as "DO Only":**
```python
IF involved party is student:
  NOTIFY:
  - Student (Web + Email): "Your case is being handled by the Discipline Office"
  - Student's adviser (Web + Email): "Case {case_id} for {student_name} is being handled by DO"

IF involved party is teacher:
  NOTIFY:
  - Teacher (Web + Email): "You're involved in case {case_id} - DO handling"
  - DO (internal tracking)
  - Guidance (Web + Email): "Teacher case {case_id} handled by DO"
```

**When DO refers to Guidance:**
```python
IF involved party is student:
  NOTIFY:
  - All Counselors (Web + Email): "New major case {case_id} requires evaluation"
  - Student (Web + Email): "Your case has been forwarded to Guidance Office"
  - Student's adviser (Web + Email): "Case {case_id} for {student_name} forwarded to Guidance"

IF involved party is teacher:
  NOTIFY:
  - All Counselors (Web + Email): "Confidential teacher case {case_id} requires evaluation"
  - DO (internal tracking)
  - NO notification to teacher yet (confidential)
```

---

### Phase 3: Guidance Evaluation

#### Counselor Actions:
1. **Review Case** - Check history, evidence, context
2. **Determine Commission Level**:
   - 1st Commission (First offense)
   - 2nd Commission (Second offense)
   - 3rd Commission (Third+ offense)
3. **Select Intervention**:
   - Parent Conference with Adviser
   - Counseling/Follow-up
   - Values Reflective Formation (VRF)
   - Recommendation for Sanction

#### Notification Logic:

**For Student Cases:**

**If VRF Selected:**
```python
NOTIFY:
- All ESP Teachers (Web + Email): "New VRF case {case_id} assigned"
- Student (Web + Email): "You've been assigned to Values Reflective Formation program"
- Student's adviser (Web + Email): "Your advisee {student_name} assigned to VRF"
- Counselor (confirmation): "VRF case created for {student_name}"
```

**If Other Intervention:**
```python
NOTIFY:
- Student (Web + Email): "Counseling session scheduled for {date} at {time}"
- Student's adviser (Web + Email): "Counseling scheduled for {student_name} on {date}"
- Counselor (confirmation): "Counseling scheduled for {student_name}"
```

**For Teacher Cases:**

**If Counseling/Investigation:**
```python
NOTIFY:
- Teacher (Web + Email): "Meeting scheduled regarding case {case_id} on {date}"
- DO (Web + Email): "Teacher meeting scheduled for case {case_id}"
- Guidance (confirmation): "Teacher meeting scheduled"
- ESP/Commission (if required): "Teacher case {case_id} requires commission review"
```

**If Sanction Recommended:**
```python
NOTIFY:
- Principal (Web + Email): "Teacher case {case_id} requires sanction decision"
- DO (Web + Email): "Case {case_id} escalated to Principal"
- Guidance (confirmation): "Case escalated"
- Teacher (Web + Email): "Case {case_id} under Principal review"
```

---

### Phase 4: Intervention Execution

#### For VRF Cases (Students):
```python
ESP Teacher schedules session:
NOTIFY:
- Student (Web + Email): "VRF session scheduled for {date} at {time} in {location}"
- Student's adviser (Web + Email): "VRF session for {student_name} on {date}"
- Counselor (Web + Email): "VRF session scheduled by {esp_teacher}"

ESP Teacher updates status:
NOTIFY:
- Counselor (Web + Email): "VRF session for {student_name} marked as {status}"
- Student's adviser (Web + Email): "VRF session update for {student_name}"
```

#### For Counseling Cases (Students):
```python
Counselor schedules session:
NOTIFY:
- Student (Web + Email): "Counseling session on {date} at {time} in {location}"
- Student's adviser (Web + Email): "Counseling for {student_name} on {date}"

Counselor completes session:
NOTIFY:
- Student (Web + Email): "Counseling session completed"
- Student's adviser (Web + Email): "Counseling completed for {student_name}"
```

#### For Teacher Cases:
```python
Meeting scheduled:
NOTIFY:
- Teacher (Web + Email): "Meeting on {date} at {time} in {location}"
- DO (Web + Email): "Teacher meeting scheduled"
- Relevant commission members (if applicable)

Meeting completed:
NOTIFY:
- Teacher (Web + Email): "Meeting outcome: {summary}"
- DO (Web + Email): "Teacher meeting completed"
- Principal (if escalated)
```

---

## 📊 DATABASE SCHEMA UPDATES NEEDED

### 1. IncidentReport Model Updates:
```python
class IncidentReport(models.Model):
    # ... existing fields ...
    
    # NEW FIELDS:
    reporter_is_victim = models.BooleanField(default=False)
    is_confidential = models.BooleanField(default=False)
    involved_parties = models.ManyToManyField(
        'InvolvedParty',
        related_name='incident_reports',
        blank=True
    )
```

### 2. NEW InvolvedParty Model:
```python
class InvolvedParty(models.Model):
    PARTY_TYPE_CHOICES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    ]
    
    party_type = models.CharField(max_length=20, choices=PARTY_TYPE_CHOICES)
    
    # For students:
    student = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'role': 'student'},
        related_name='student_involved_parties'
    )
    curriculum = models.ForeignKey(Curriculum, null=True, blank=True)
    grade_level = models.CharField(max_length=10, null=True, blank=True)
    section = models.ForeignKey(Section, null=True, blank=True)
    adviser = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'role': 'teacher'},
        related_name='advised_involved_parties'
    )
    
    # For teachers:
    teacher = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'role': 'teacher'},
        related_name='teacher_involved_parties'
    )
    department = models.CharField(max_length=100, null=True, blank=True)
    grade_level_taught = models.CharField(max_length=50, null=True, blank=True)
    
    # Common fields:
    name_if_unknown = models.CharField(max_length=200, null=True, blank=True)
    is_confirmed = models.BooleanField(default=False)
    confirmed_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='confirmed_parties'
    )
    confirmed_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

### 3. Notification Model Updates:
```python
class Notification(models.Model):
    # ... existing fields ...
    
    # NEW FIELDS:
    notification_type = models.CharField(
        max_length=50,
        choices=[
            ('report_submitted', 'Report Submitted'),
            ('party_confirmed', 'Party Confirmed'),
            ('do_classified', 'DO Classified'),
            ('guidance_evaluation', 'Guidance Evaluation'),
            ('vrf_assigned', 'VRF Assigned'),
            ('counseling_scheduled', 'Counseling Scheduled'),
            ('session_completed', 'Session Completed'),
            ('status_update', 'Status Update'),
        ]
    )
    email_sent = models.BooleanField(default=False)
    email_sent_at = models.DateTimeField(null=True, blank=True)
```

---

## 📝 ALL REPORTS TABLE DISPLAY

### Columns:
```
| Report ID | Involved Parties | Party Type | Academic Info/Dept | Reporter Role | Incident Type | Status | Date | Actions |
```

### Example Rows:

**Student Case:**
```
| 2025-0001 | Maria Santos | Student | SHS 11-A STEM, Ms. Tan (Adviser) | Student | Bullying | Pending (DO) | 12/02/2025 | View |
```

**Teacher Case:**
```
| 2025-0002 | Mr. Reyes | Teacher | Math Department, Grade 10 | Student | Misconduct | Confidential (Guidance) | 12/02/2025 | View |
```

**Mixed Case:**
```
| 2025-0003 | Maria Santos, Mr. Reyes | Student, Teacher | Maria: 11-A, Ms. Tan; Mr. Reyes: Math Dept | Teacher | Cheating | Under Review (DO) | 12/02/2025 | View |
```

**Unknown Party:**
```
| 2025-0004 | Unknown Student | Student | Pending Confirmation | Teacher | Vandalism | Pending (DO) | 12/02/2025 | View |
```

---

## 🔔 NOTIFICATION SUMMARY TABLE

| Event | Student Case Notifications | Teacher Case Notifications |
|-------|---------------------------|---------------------------|
| **Report Submitted** | • DO (all)<br>• Reporter's adviser (if reporter is student)<br>• Student (if known)<br>• Student's adviser (if known) | • DO (all)<br>• Guidance (all)<br>• Reporter's adviser (if reporter is student) |
| **Party Confirmed by DO** | • Student<br>• Student's adviser | • DO (internal)<br>• Guidance |
| **DO Only Classification** | • Student<br>• Student's adviser | • Teacher<br>• DO<br>• Guidance |
| **Referred to Guidance** | • All counselors<br>• Student<br>• Student's adviser | • All counselors<br>• DO |
| **VRF Assigned** | • All ESP teachers<br>• Student<br>• Student's adviser<br>• Counselor | N/A |
| **Counseling Scheduled** | • Student<br>• Student's adviser<br>• Counselor | • Teacher<br>• DO<br>• Relevant commission |
| **Session Completed** | • Student<br>• Student's adviser | • Teacher<br>• DO<br>• Principal (if escalated) |

---

## 🎯 IMPLEMENTATION PRIORITY

### Phase 1 (High Priority):
1. ✅ Add `InvolvedParty` model
2. ✅ Update `IncidentReport` model
3. ✅ Update report form to handle party types
4. ✅ Implement "Reporter is Victim" checkbox
5. ✅ Add confidential report flag

### Phase 2 (Medium Priority):
6. ✅ Update notification logic for student cases
7. ✅ Update notification logic for teacher cases
8. ✅ Add email notification system
9. ✅ Update All Reports table display
10. ✅ Add party confirmation workflow for DO

### Phase 3 (Enhancement):
11. ✅ Add notification history tracking
12. ✅ Add email delivery status
13. ✅ Add notification preferences
14. ✅ Add bulk notification management

---

## 📧 EMAIL NOTIFICATION TEMPLATES

### For Students:
```
Subject: SIRMS - Case {case_id} Update

Dear {student_name},

{message_body}

Case ID: {case_id}
Status: {status}
Date: {date}

If you have questions, please contact the Guidance Office.

Best regards,
SIRMS Team
```

### For Teachers (Involved Party):
```
Subject: SIRMS - Confidential Case {case_id}

Dear {teacher_name},

{message_body}

Case ID: {case_id}
Status: {status}
Date: {date}

This is a confidential matter. Please contact the Discipline Office for details.

Best regards,
SIRMS Team
```

### For Advisers:
```
Subject: SIRMS - Advisee Update: {student_name}

Dear {adviser_name},

{message_body}

Student: {student_name}
Section: {section}
Case ID: {case_id}
Status: {status}

Please monitor your advisee and provide support as needed.

Best regards,
SIRMS Team
```

---

## ✅ TESTING CHECKLIST

### Student Case Tests:
- [ ] Submit report with student as involved party
- [ ] Verify student receives notification
- [ ] Verify adviser receives notification
- [ ] Test "Reporter is Victim" checkbox
- [ ] Test unknown student (no notification until confirmed)
- [ ] Test DO confirmation triggers notifications
- [ ] Test VRF assignment notifications
- [ ] Test counseling schedule notifications

### Teacher Case Tests:
- [ ] Submit report with teacher as involved party
- [ ] Verify confidential flag works
- [ ] Verify only DO and Guidance notified initially
- [ ] Test DO confirmation process
- [ ] Test teacher notification after confirmation
- [ ] Test commission notification (if applicable)
- [ ] Test escalation to Principal

### Mixed Case Tests:
- [ ] Submit report with both student and teacher
- [ ] Verify correct notifications for each party type
- [ ] Test confidential handling for teacher
- [ ] Test separate workflows for each party

### Email Tests:
- [ ] Verify emails sent successfully
- [ ] Check email templates render correctly
- [ ] Test email delivery status tracking
- [ ] Verify unsubscribe/preferences work

---

**This specification provides the complete blueprint for implementing a proper process and notification system that handles both students and teachers as involved parties with appropriate confidentiality and notification routing.**

