# SIRMS Entity Relationship Diagram (ERD)

## Database Schema Overview

This document provides a comprehensive Entity Relationship Diagram for the Student Incident Reporting and Management System (SIRMS).

---

## Core Entities

### 1. CustomUser (User Management)
**Primary Key:** id  
**Type:** Extended Django AbstractUser

**Attributes:**
- id (PK)
- username
- email
- password
- first_name
- last_name
- role (ENUM: student, teacher, do, counselor, esp_teacher)
- employee_id (UNIQUE)
- grade_level
- section

**Relationships:**
- ONE CustomUser → MANY IncidentReport (as reporter)
- ONE CustomUser → MANY IncidentReport (as reported_student)
- ONE CustomUser → MANY Section (as adviser)
- ONE CustomUser → MANY Classification (as classified_by)
- ONE CustomUser → MANY CounselingSession (as counselor)
- ONE CustomUser → MANY CounselingSession (as student)
- ONE CustomUser → MANY Notification (as user)
- ONE CustomUser → MANY ViolationHistory (as student)
- ONE CustomUser → MANY CaseEvaluation (as evaluated_by)
- ONE CustomUser → MANY InternalNote (as author)
- ONE CustomUser → MANY VPFCase (as student)
- ONE CustomUser → MANY VPFCase (as assigned_by)
- ONE CustomUser → MANY VPFSchedule (as esp_teacher)
- ONE CustomUser → MANY CounselingSchedule (as counselor/student)
- ONE CustomUser → MANY DOSchedule (as discipline_officer/student)

---

### 2. Curriculum
**Primary Key:** id

**Attributes:**
- id (PK)
- name
- description

**Relationships:**
- ONE Curriculum → MANY Track
- ONE Curriculum → MANY TeacherAssignment
- ONE Curriculum → MANY IncidentReport

---

### 3. Track
**Primary Key:** id

**Attributes:**
- id (PK)
- name
- curriculum_id (FK)

**Relationships:**
- MANY Track → ONE Curriculum
- ONE Track → MANY Grade
- ONE Track → MANY IncidentReport

---

### 4. Grade
**Primary Key:** id

**Attributes:**
- id (PK)
- level
- track_id (FK)

**Relationships:**
- MANY Grade → ONE Track
- ONE Grade → MANY Section
- ONE Grade → MANY IncidentReport

---

### 5. Section
**Primary Key:** id

**Attributes:**
- id (PK)
- name
- grade_id (FK)
- adviser_id (FK → CustomUser)

**Relationships:**
- MANY Section → ONE Grade
- MANY Section → ONE CustomUser (adviser)
- ONE Section → MANY IncidentReport

---

### 6. TeacherAssignment
**Primary Key:** id  
**Unique Together:** (teacher_name, grade_level, section_name, track_code)

**Attributes:**
- id (PK)
- teacher_name
- curriculum_id (FK)
- track_code
- grade_level
- section_name

**Relationships:**
- MANY TeacherAssignment → ONE Curriculum

---

## Incident Management Entities

### 7. IncidentType
**Primary Key:** id

**Attributes:**
- id (PK)
- name
- description
- severity (ENUM: prohibited, school_policy)
- legal_references

**Relationships:**
- ONE IncidentType → MANY IncidentReport
- ONE IncidentType → MANY ViolationHistory
- MANY IncidentType ↔ MANY LegalReference (M2M)

---

### 8. LegalReference
**Primary Key:** id

**Attributes:**
- id (PK)
- title
- reference_number
- description

**Relationships:**
- MANY LegalReference ↔ MANY IncidentType (M2M)

---

### 9. IncidentReport (Central Entity)
**Primary Key:** id  
**Unique:** case_id

**Attributes:**
- id (PK)
- case_id (UNIQUE, auto-generated: YYYY-####)
- reporter_id (FK → CustomUser)
- reporter_first_name
- reporter_middle_name
- reporter_last_name
- involved_students
- student_gender (ENUM: male, female)
- curriculum_id (FK)
- grade_level
- section_name
- teacher_name
- track_id (FK, legacy)
- grade_id (FK, legacy)
- section_id (FK, legacy)
- teacher_id (FK, legacy)
- incident_date
- incident_time
- incident_type_id (FK)
- description
- evidence (FILE)
- reported_student_id (FK → CustomUser)
- status (ENUM: pending, under_review, classified, evaluated, resolved, closed)
- evidence_status (ENUM: pending, clear, insufficient)
- evidence_notes
- created_at
- updated_at

**Relationships:**
- MANY IncidentReport → ONE CustomUser (reporter)
- MANY IncidentReport → ONE CustomUser (reported_student)
- MANY IncidentReport → ONE Curriculum
- MANY IncidentReport → ONE Track
- MANY IncidentReport → ONE Grade
- MANY IncidentReport → ONE Section
- MANY IncidentReport → ONE CustomUser (teacher)
- MANY IncidentReport → ONE IncidentType
- ONE IncidentReport → ONE Classification
- ONE IncidentReport → MANY CounselingSession
- ONE IncidentReport → MANY Notification
- ONE IncidentReport → MANY ViolationHistory
- ONE IncidentReport → ONE CaseEvaluation
- ONE IncidentReport → MANY InternalNote
- ONE IncidentReport → MANY VPFCase
- ONE IncidentReport → MANY DOSchedule

---

### 10. Classification
**Primary Key:** id  
**One-to-One:** report_id

**Attributes:**
- id (PK)
- report_id (FK, ONE-TO-ONE → IncidentReport)
- classified_by_id (FK → CustomUser)
- severity (ENUM: minor, major)
- internal_notes
- classified_at

**Relationships:**
- ONE Classification → ONE IncidentReport
- MANY Classification → ONE CustomUser (classified_by)

---

### 11. CaseEvaluation
**Primary Key:** id  
**One-to-One:** report_id

**Attributes:**
- id (PK)
- report_id (FK, ONE-TO-ONE → IncidentReport)
- evaluated_by_id (FK → CustomUser)
- evaluation_notes
- recommendation (ENUM: counseling, monitoring, resolved)
- verdict (ENUM: pending, guilty, not_guilty, insufficient_evidence)
- verdict_notes
- is_repeat_offender
- evaluated_at

**Relationships:**
- ONE CaseEvaluation → ONE IncidentReport
- MANY CaseEvaluation → ONE CustomUser (evaluated_by)
- MANY CaseEvaluation ↔ MANY IncidentReport (related_cases, M2M)
- ONE CaseEvaluation → MANY CounselingSchedule

---

## Counseling & Intervention Entities

### 12. CounselingSession
**Primary Key:** id

**Attributes:**
- id (PK)
- report_id (FK)
- counselor_id (FK → CustomUser)
- student_id (FK → CustomUser)
- scheduled_date
- status (ENUM: scheduled, completed, cancelled, referred_to_teacher)
- remarks
- created_at

**Relationships:**
- MANY CounselingSession → ONE IncidentReport
- MANY CounselingSession → ONE CustomUser (counselor)
- MANY CounselingSession → ONE CustomUser (student)

---

### 13. Counselor
**Primary Key:** id

**Attributes:**
- id (PK)
- name
- email
- phone
- specialization
- is_active
- created_at
- updated_at

**Relationships:**
- ONE Counselor → MANY VPFCase (esp_teacher_assigned)
- ONE Counselor → MANY VPFSchedule (counselor_assigned)

---

### 14. CounselingSchedule
**Primary Key:** id

**Attributes:**
- id (PK)
- evaluation_id (FK → CaseEvaluation)
- counselor_id (FK → CustomUser)
- student_id (FK → CustomUser)
- scheduled_date
- location
- notes
- status (ENUM: scheduled, completed, missed, rescheduled)
- created_at
- updated_at

**Relationships:**
- MANY CounselingSchedule → ONE CaseEvaluation
- MANY CounselingSchedule → ONE CustomUser (counselor)
- MANY CounselingSchedule → ONE CustomUser (student)

---

### 15. VPFCase (Values Reflective Formation)
**Primary Key:** id

**Attributes:**
- id (PK)
- report_id (FK → IncidentReport)
- student_id (FK → CustomUser)
- assigned_by_id (FK → CustomUser)
- esp_teacher_assigned_id (FK → Counselor)
- commission_level
- intervention
- status (ENUM: pending, scheduled, ongoing, completed, cancelled)
- notes
- assigned_at
- updated_at

**Relationships:**
- MANY VPFCase → ONE IncidentReport
- MANY VPFCase → ONE CustomUser (student)
- MANY VPFCase → ONE CustomUser (assigned_by)
- MANY VPFCase → ONE Counselor (esp_teacher_assigned)
- ONE VPFCase → MANY VPFSchedule

---

### 16. VPFSchedule
**Primary Key:** id

**Attributes:**
- id (PK)
- vpf_case_id (FK → VPFCase)
- esp_teacher_id (FK → CustomUser)
- counselor_assigned_id (FK → Counselor)
- scheduled_date
- location
- notes
- status (ENUM: scheduled, completed, missed, rescheduled)
- created_at
- updated_at

**Relationships:**
- MANY VPFSchedule → ONE VPFCase
- MANY VPFSchedule → ONE CustomUser (esp_teacher)
- MANY VPFSchedule → ONE Counselor (counselor_assigned)

---

### 17. DOSchedule (Discipline Officer Schedule)
**Primary Key:** id

**Attributes:**
- id (PK)
- report_id (FK → IncidentReport)
- discipline_officer_id (FK → CustomUser)
- student_id (FK → CustomUser)
- schedule_type (ENUM: parent_conference, interview, follow_up)
- scheduled_date
- location
- attendees
- purpose
- notes
- status (ENUM: scheduled, completed, cancelled, rescheduled, no_show)
- created_at
- updated_at

**Relationships:**
- MANY DOSchedule → ONE IncidentReport
- MANY DOSchedule → ONE CustomUser (discipline_officer)
- MANY DOSchedule → ONE CustomUser (student)

---

## History Entities

### 18. ViolationHistory
**Primary Key:** id

**Attributes:**
- id (PK)
- student_id (FK → CustomUser)
- report_id (FK → IncidentReport)
- violation_type_id (FK → IncidentType)
- severity (ENUM: minor, major)
- date_occurred
- status
- notes
- created_at

**Relationships:**
- MANY ViolationHistory → ONE CustomUser (student)
- MANY ViolationHistory → ONE IncidentReport
- MANY ViolationHistory → ONE IncidentType

---

## Supporting Entities

### 19. Notification
**Primary Key:** id

**Attributes:**
- id (PK)
- user_id (FK → CustomUser)
- title
- message
- report_id (FK → IncidentReport)
- is_read
- created_at

**Relationships:**
- MANY Notification → ONE CustomUser
- MANY Notification → ONE IncidentReport

---

### 20. InternalNote
**Primary Key:** id

**Attributes:**
- id (PK)
- report_id (FK → IncidentReport)
- author_id (FK → CustomUser)
- note
- is_private
- created_at

**Relationships:**
- MANY InternalNote → ONE IncidentReport
- MANY InternalNote → ONE CustomUser (author)

---

### 21. SystemBackup
**Primary Key:** id

**Attributes:**
- id (PK)
- backup_name
- backup_type (ENUM: manual, scheduled, emergency)
- file_path
- file_size
- created_by_id (FK → CustomUser)
- created_at

**Relationships:**
- MANY SystemBackup → ONE CustomUser (created_by)

---

### 22. ReportAnalytics
**Primary Key:** id

**Attributes:**
- id (PK)
- date_range_start
- date_range_end
- total_reports
- minor_violations
- major_violations
- resolved_cases
- pending_cases
- most_common_violation
- grade_with_most_violations
- generated_by_id (FK → CustomUser)
- generated_at

**Relationships:**
- MANY ReportAnalytics → ONE CustomUser (generated_by)

---

## Relationship Summary

### One-to-One Relationships
1. IncidentReport ↔ Classification
2. IncidentReport ↔ CaseEvaluation

### One-to-Many Relationships
1. CustomUser → IncidentReport (multiple roles)
2. Curriculum → Track → Grade → Section
3. IncidentReport → CounselingSession
4. IncidentReport → VPFCase
5. IncidentReport → DOSchedule
6. IncidentReport → Notification
7. IncidentReport → ViolationHistory
8. IncidentReport → InternalNote
9. VPFCase → VPFSchedule
10. CaseEvaluation → CounselingSchedule

### Many-to-Many Relationships
1. IncidentType ↔ LegalReference
2. CaseEvaluation ↔ IncidentReport (related_cases)

---

## Key Design Patterns

### 1. Case Flow Pattern
```
IncidentReport (created)
    ↓
Classification (DO routes case)
    ↓
CaseEvaluation (Counselor evaluates)
    ↓
VPFCase OR CounselingSchedule (intervention)
    ↓
Resolved/Closed
```

### 2. User Role Pattern
- CustomUser.role determines access and capabilities
- Role-based foreign keys with limit_choices_to
- Multiple relationship types per user (reporter, student, counselor, etc.)

### 3. Dual Storage Pattern
- New fields (grade_level, section_name, teacher_name) for direct storage
- Legacy FK fields (grade, section, teacher) for backward compatibility
- Allows flexible reporting without complex joins

### 4. Status Tracking Pattern
- Most entities have status field with ENUM choices
- Timestamps (created_at, updated_at) for audit trail
- Evidence tracking with separate status field

---

## Database Indexes (Recommended)

```sql
-- Performance optimization indexes
CREATE INDEX idx_incident_status ON incidents_incidentreport(status);
CREATE INDEX idx_incident_date ON incidents_incidentreport(incident_date);
CREATE INDEX idx_incident_student ON incidents_incidentreport(reported_student_id);
CREATE INDEX idx_case_id ON incidents_incidentreport(case_id);
CREATE INDEX idx_notification_user ON incidents_notification(user_id, is_read);
CREATE INDEX idx_violation_student ON incidents_violationhistory(student_id, date_occurred);
CREATE INDEX idx_counseling_date ON incidents_counselingschedule(scheduled_date);
CREATE INDEX idx_vpf_status ON incidents_vpfcase(status);
CREATE INDEX idx_do_schedule_date ON incidents_doschedule(scheduled_date);
```

---

## Visual ERD Representation

```
┌─────────────────┐
│   CustomUser    │
│   (Central)     │
└────────┬────────┘
         │
         ├──────────────────────────────────────────┐
         │                                          │
         ▼                                          ▼
┌─────────────────┐                      ┌──────────────────┐
│ IncidentReport  │◄─────────────────────│  Classification  │
│   (Core Case)   │                      └──────────────────┘
└────────┬────────┘
         │
         ├──────────┬──────────┬──────────┬──────────┐
         ▼          ▼          ▼          ▼          ▼
┌──────────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐
│CaseEvaluation│ │ VPFCase  │ │DOSchedule│ │Notification│
└──────┬───────┘ └────┬─────┘ └──────────┘ └──────────┘
       │              │
       ▼              ▼
┌──────────────┐ ┌──────────┐
│Counseling    │ │VPF       │
│Schedule      │ │Schedule  │
└──────────────┘ └──────────┘

Academic Structure:
Curriculum → Track → Grade → Section → TeacherAssignment
```

---

## Entity Count Summary
- **Total Entities:** 22
- **Core Entities:** 9 (User, Curriculum, Track, Grade, Section, TeacherAssignment, IncidentType, LegalReference, IncidentReport)
- **Process Entities:** 8 (Classification, CaseEvaluation, CounselingSession, Counselor, CounselingSchedule, VPFCase, VPFSchedule, DOSchedule)
- **Support Entities:** 5 (ViolationHistory, Notification, InternalNote, SystemBackup, ReportAnalytics)

---

**Generated:** November 30, 2025  
**System:** SIRMS (Student Incident Reporting and Management System)  
**Database:** SQLite/PostgreSQL Compatible
