# SIRMS Database Documentation

## Current Database Configuration

**Database Type**: SQLite3  
**Database File**: `db.sqlite3`  
**Location**: `sirms/db.sqlite3`

> **Note**: For production deployment, you should migrate to PostgreSQL or MySQL.

---

## Database Tables (Models)

Your SIRMS system has **23 database tables** organized into the following categories:

### 1. User Management (1 table)

#### **CustomUser**
- **Purpose**: Store all system users (students, teachers, DO, counselors, principal, ESP teachers)
- **Key Fields**:
  - `username`, `email`, `password`
  - `role` (student, teacher, do, counselor, principal, esp_teacher)
  - `first_name`, `last_name`
  - `employee_id` (for staff)
  - `grade_level`, `section` (for students)
- **Relationships**: Base user model for all other tables

---

### 2. Academic Structure (5 tables)

#### **Curriculum**
- **Purpose**: Store curriculum types (e.g., K-12, Senior High)
- **Key Fields**: `name`, `description`

#### **Track**
- **Purpose**: Store academic tracks (STEM, ABM, HUMSS, etc.)
- **Key Fields**: `name`, `curriculum` (FK)

#### **Grade**
- **Purpose**: Store grade levels (7-12)
- **Key Fields**: `level`, `track` (FK)

#### **Section**
- **Purpose**: Store class sections
- **Key Fields**: `name`, `grade` (FK), `adviser` (FK to CustomUser)

#### **TeacherAssignment**
- **Purpose**: Map teachers to specific grade/track/section combinations
- **Key Fields**: `teacher_name`, `curriculum`, `track_code`, `grade_level`, `section_name`

---

### 3. Incident Management (3 tables)

#### **IncidentType**
- **Purpose**: Define types of violations
- **Key Fields**: 
  - `name`, `description`
  - `severity` (prohibited acts or school policies)
  - `legal_references`
- **Examples**: Bullying, Vandalism, Tardiness, etc.

#### **LegalReference**
- **Purpose**: Store legal documents and references
- **Key Fields**: `title`, `reference_number`, `description`
- **Relationships**: Many-to-many with IncidentType

#### **IncidentReport**
- **Purpose**: Main incident report records
- **Key Fields**:
  - `case_id` (auto-generated: YYYY-0001)
  - `reporter` (FK to CustomUser)
  - `reported_student` (FK to CustomUser)
  - `reporter_first_name`, `reporter_last_name`
  - `involved_students`, `student_gender`
  - `curriculum`, `grade_level`, `section_name`, `teacher_name`
  - `incident_date`, `incident_time`
  - `incident_type` (FK)
  - `description`, `evidence` (file upload)
  - `status` (pending, under_review, classified, evaluated, sanctioned, resolved, closed)
  - `evidence_status`, `evidence_notes`
- **Auto-generated**: `case_id`, `created_at`, `updated_at`

---

### 4. Case Processing (2 tables)

#### **Classification**
- **Purpose**: DO classification of incidents
- **Key Fields**:
  - `report` (OneToOne with IncidentReport)
  - `classified_by` (FK to CustomUser - DO)
  - `severity` (minor = DO handles, major = send to counselor)
  - `internal_notes`
  - `classified_at`

#### **CaseEvaluation**
- **Purpose**: Counselor evaluation of cases
- **Key Fields**:
  - `report` (OneToOne with IncidentReport)
  - `evaluated_by` (FK to CustomUser - Counselor)
  - `evaluation_notes`
  - `recommendation` (counseling, sanction, monitoring, resolved)
  - `verdict` (pending, guilty, not_guilty, insufficient_evidence)
  - `verdict_notes`
  - `is_repeat_offender`
  - `related_cases` (ManyToMany with IncidentReport)

---

### 5. Counseling & Interventions (5 tables)

#### **Counselor**
- **Purpose**: Store counselor/ESP teacher information
- **Key Fields**: `name`, `email`, `phone`, `specialization`, `is_active`

#### **CounselingSession**
- **Purpose**: General counseling sessions
- **Key Fields**:
  - `report` (FK to IncidentReport)
  - `counselor`, `student` (FK to CustomUser)
  - `scheduled_date`
  - `status` (scheduled, completed, cancelled, referred_to_teacher)
  - `remarks`

#### **CounselingSchedule**
- **Purpose**: Scheduled counseling appointments (non-VPF)
- **Key Fields**:
  - `evaluation` (FK to CaseEvaluation)
  - `counselor`, `student` (FK to CustomUser)
  - `scheduled_date`, `location`
  - `status` (scheduled, completed, missed, rescheduled)
  - `notes`

#### **VPFCase**
- **Purpose**: Values Reflective Formation cases
- **Key Fields**:
  - `report` (FK to IncidentReport)
  - `student` (FK to CustomUser)
  - `assigned_by` (FK to CustomUser - Counselor)
  - `esp_teacher_assigned` (FK to Counselor)
  - `commission_level` (1st, 2nd, 3rd)
  - `intervention`
  - `status` (pending, scheduled, ongoing, completed, cancelled)

#### **VPFSchedule**
- **Purpose**: VPF counseling schedule managed by ESP Teacher
- **Key Fields**:
  - `vpf_case` (FK to VPFCase)
  - `esp_teacher` (FK to CustomUser)
  - `counselor_assigned` (FK to Counselor)
  - `scheduled_date`, `location`
  - `status` (scheduled, completed, missed, rescheduled)

---

### 6. Discipline Office (1 table)

#### **DOSchedule**
- **Purpose**: DO parent conferences and interviews
- **Key Fields**:
  - `report` (FK to IncidentReport)
  - `discipline_officer` (FK to CustomUser)
  - `student` (FK to CustomUser)
  - `schedule_type` (parent_conference, interview, follow_up)
  - `scheduled_date`, `location`
  - `attendees`, `purpose`, `notes`
  - `status` (scheduled, completed, cancelled, rescheduled, no_show)

---

### 7. Sanctions & Actions (1 table)

#### **Sanction**
- **Purpose**: Principal-issued sanctions
- **Key Fields**:
  - `report` (OneToOne with IncidentReport)
  - `issued_by` (FK to CustomUser - Principal)
  - `sanction_type` (warning, suspension, expulsion)
  - `duration_days`
  - `reason`

---

### 8. Tracking & History (2 tables)

#### **ViolationHistory**
- **Purpose**: Track student violation patterns
- **Key Fields**:
  - `student` (FK to CustomUser)
  - `report` (FK to IncidentReport)
  - `violation_type` (FK to IncidentType)
  - `severity` (minor, major)
  - `date_occurred`
  - `status`, `notes`

#### **InternalNote**
- **Purpose**: Internal staff notes on cases
- **Key Fields**:
  - `report` (FK to IncidentReport)
  - `author` (FK to CustomUser)
  - `note`
  - `is_private`

---

### 9. System Management (3 tables)

#### **Notification**
- **Purpose**: User notifications
- **Key Fields**:
  - `user` (FK to CustomUser)
  - `title`, `message`
  - `report` (FK to IncidentReport)
  - `is_read`

#### **SystemBackup**
- **Purpose**: Track system backups
- **Key Fields**:
  - `backup_name`, `backup_type`
  - `file_path`, `file_size`
  - `created_by` (FK to CustomUser)

#### **ReportAnalytics**
- **Purpose**: Store analytics data
- **Key Fields**:
  - `date_range_start`, `date_range_end`
  - `total_reports`, `minor_violations`, `major_violations`
  - `resolved_cases`, `pending_cases`
  - `most_common_violation`, `grade_with_most_violations`

---

## Database Relationships

### One-to-One Relationships
- IncidentReport ↔ Classification
- IncidentReport ↔ CaseEvaluation
- IncidentReport ↔ Sanction

### One-to-Many Relationships
- CustomUser → IncidentReport (as reporter)
- CustomUser → IncidentReport (as reported_student)
- CustomUser → CounselingSession
- CustomUser → VPFCase
- CustomUser → Notification
- IncidentReport → CounselingSession
- IncidentReport → VPFCase
- IncidentReport → InternalNote
- IncidentReport → DOSchedule
- VPFCase → VPFSchedule
- CaseEvaluation → CounselingSchedule

### Many-to-Many Relationships
- IncidentType ↔ LegalReference
- CaseEvaluation ↔ IncidentReport (related_cases)

---

## Database Statistics

**Total Tables**: 23

**By Category**:
- User Management: 1
- Academic Structure: 5
- Incident Management: 3
- Case Processing: 2
- Counseling & Interventions: 5
- Discipline Office: 1
- Sanctions: 1
- Tracking & History: 2
- System Management: 3

---

## Key Database Features

### Auto-Generated Fields
- **case_id**: Automatically generated as YYYY-0001 format
- **created_at**: Timestamp when record is created
- **updated_at**: Timestamp when record is updated

### File Uploads
- **IncidentReport.evidence**: Stored in `media/evidence/`

### Status Tracking
- **IncidentReport**: 7 status stages (pending → resolved)
- **CounselingSession**: 4 statuses
- **VPFCase**: 5 statuses
- **DOSchedule**: 5 statuses

### Data Validation
- Email format validation
- Role-based access control
- Foreign key constraints
- Unique constraints (case_id, employee_id)

---

## Database Commands

### View Database Schema
```bash
python manage.py inspectdb
```

### Create Migrations
```bash
python manage.py makemigrations
```

### Apply Migrations
```bash
python manage.py migrate
```

### Export Data
```bash
python manage.py dumpdata > backup.json
```

### Import Data
```bash
python manage.py loaddata backup.json
```

### Access Database Shell
```bash
python manage.py dbshell
```

### Django Shell (Query Data)
```bash
python manage.py shell
```

---

## Sample Queries

### Count Total Reports
```python
from incidents.models import IncidentReport
total = IncidentReport.objects.count()
```

### Get Pending Reports
```python
pending = IncidentReport.objects.filter(status='pending')
```

### Get Student's Reports
```python
student_reports = IncidentReport.objects.filter(reported_student__username='student123')
```

### Get Major Cases
```python
major_cases = IncidentReport.objects.filter(classification__severity='major')
```

### Get Reports by Date Range
```python
from datetime import datetime
reports = IncidentReport.objects.filter(
    incident_date__range=['2024-01-01', '2024-12-31']
)
```

---

## Migration to Production Database

### For PostgreSQL
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'sirms_db',
        'USER': 'your_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### For MySQL
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'sirms_db',
        'USER': 'your_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

---

## Database Backup Strategy

### Recommended Backup Schedule
- **Daily**: Automated backups at midnight
- **Weekly**: Full database export
- **Monthly**: Archive backups
- **Before Deployment**: Manual backup

### Backup Commands
```bash
# SQLite backup
cp db.sqlite3 backups/db_backup_$(date +%Y%m%d).sqlite3

# PostgreSQL backup
pg_dump sirms_db > backups/sirms_backup_$(date +%Y%m%d).sql

# Django data export
python manage.py dumpdata > backups/data_backup_$(date +%Y%m%d).json
```

---

## Security Considerations

1. **Never commit db.sqlite3 to Git**
2. **Use environment variables for database credentials**
3. **Enable database encryption in production**
4. **Regular backups with secure storage**
5. **Implement database access logging**
6. **Use read-only database users where appropriate**
7. **Regular security audits**

---

## Performance Optimization

### Indexes
Django automatically creates indexes on:
- Primary keys
- Foreign keys
- Unique fields

### Query Optimization
- Use `select_related()` for foreign keys
- Use `prefetch_related()` for many-to-many
- Add database indexes for frequently queried fields
- Use `only()` and `defer()` to limit fields

### Example Optimized Query
```python
reports = IncidentReport.objects.select_related(
    'reporter', 'reported_student', 'incident_type', 'classification'
).prefetch_related(
    'counseling_sessions', 'internal_notes'
).filter(status='pending')
```

---

## Database Maintenance

### Regular Tasks
- [ ] Weekly database backups
- [ ] Monthly data cleanup (old notifications, logs)
- [ ] Quarterly performance analysis
- [ ] Annual data archiving

### Monitoring
- Database size
- Query performance
- Connection pool usage
- Slow query logs

---

This documentation covers all 23 database tables in your SIRMS system. For specific queries or modifications, refer to Django's ORM docume