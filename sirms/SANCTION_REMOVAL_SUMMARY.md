# Sanction Model and Principal Role Removal Summary

## Date: November 30, 2025

## Changes Made

### 1. Database Model Changes (models.py)
- **Removed:** `Sanction` model class entirely
- **Updated:** `CustomUser.ROLE_CHOICES` - removed 'principal' role
- **Updated:** `IncidentReport.STATUS_CHOICES` - removed 'sanctioned' status
- **Updated:** `CaseEvaluation.recommendation` - removed 'sanction' option

### 2. Admin Interface (admin.py)
- **Removed:** `Sanction` model registration from Django admin

### 3. Forms (forms.py)
- **Removed:** `SanctionForm` class
- **Removed:** `Sanction` from model imports

### 4. Views (views.py)
- **Removed:** `Sanction` from model imports
- **Removed:** `SanctionForm` from form imports

### 5. Documentation (SIRMS_ERD_DOCUMENTATION.md)
- **Removed:** Sanction entity section (was section 18)
- **Updated:** Entity numbering (19-23 renumbered to 18-22)
- **Updated:** Total entity count from 23 to 22
- **Updated:** One-to-One relationships section
- **Updated:** Case flow pattern diagram
- **Updated:** Visual ERD representation
- **Updated:** CustomUser relationships
- **Updated:** IncidentReport relationships and status choices
- **Updated:** CaseEvaluation recommendation choices
- **Updated:** Support entities count from 6 to 5

### 6. Database Migration
- **Created:** Migration file `0024_remove_sanction_and_principal.py`
- **Operations:**
  - Alter field `recommendation` on `CaseEvaluation`
  - Alter field `role` on `CustomUser`
  - Alter field `status` on `IncidentReport`
  - Delete model `Sanction`

## Updated User Roles
The system now supports only these roles:
1. Student
2. Teacher
3. Discipline Officer (DO)
4. Guidance Counselor
5. ESP Teacher/VPF Coordinator

## Updated Case Flow
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

## Updated Incident Report Statuses
- pending
- under_review
- classified
- evaluated
- resolved
- closed

## Updated Case Evaluation Recommendations
- counseling (Counseling Only)
- monitoring (Monitoring Required)
- resolved (Case Resolved)

## Migration Instructions

To apply these changes to your database:

```bash
# Apply the migration
python manage.py migrate

# Verify the changes
python manage.py showmigrations incidents
```

## Notes
- All references to the Sanction model have been removed from the codebase
- The principal role has been completely removed from user role choices
- The ERD documentation has been updated to reflect the new structure
- No data loss will occur for existing records (except Sanction records which will be deleted)
- If you have existing Sanction records, they will be permanently deleted when you run the migration

## Files Modified
1. `sirms/incidents/models.py`
2. `sirms/incidents/admin.py`
3. `sirms/incidents/forms.py`
4. `sirms/incidents/views.py`
5. `sirms/SIRMS_ERD_DOCUMENTATION.md`
6. `sirms/incidents/migrations/0024_remove_sanction_and_principal.py` (created)

## Verification
All Python files have been checked for syntax errors and no diagnostics were found.
