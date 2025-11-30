# VPF Teacher Assignment Feature

## Overview
Guidance counselors can now assign ESP Teachers/VPF Counselors to VPF cases directly from the "For VPF" page.

## Features Implemented

### 1. Model Changes
- Added `esp_teacher_assigned` field to `VPFCase` model
- Links to the `Counselor` model (where VPF teachers are managed)
- Migration created and applied: `0017_vpfcase_esp_teacher_assigned.py`

### 2. Template Updates (`for_vpf.html`)
- Added "Assign Teacher" button for cases without assigned teachers
- Shows assigned teacher name with checkmark for cases with teachers
- Modal dialog for teacher assignment with:
  - Case ID and student name display
  - Dropdown to select ESP Teacher from Counselor list
  - Optional notes field
  - Form validation

### 3. Views Added

#### `for_vpf` View
- Displays VPF cases assigned by the counselor
- Loads VPF teachers from Counselor model
- Shows statistics (total, pending, scheduled, completed)
- URL: `/for-vpf/`

#### `assign_vpf_teacher` View
- Handles teacher assignment POST request
- Updates VPF case with assigned teacher
- Sends notifications to:
  - All ESP teachers (role: esp_teacher)
  - The student involved in the case
- URL: `/assign-vpf-teacher/`

### 4. URL Routes Added
```python
path('for-vpf/', views.for_vpf, name='for_vpf'),
path('assign-vpf-teacher/', views.assign_vpf_teacher, name='assign_vpf_teacher'),
```

## How It Works

1. **Counselor assigns VPF intervention** during case evaluation
2. **VPF case appears** in "For VPF" page
3. **Counselor clicks "Assign Teacher"** button
4. **Modal opens** showing:
   - Case details
   - List of VPF teachers from "Manage Counselors"
   - Optional notes field
5. **On assignment**:
   - Teacher is linked to the VPF case
   - ESP teachers receive notification
   - Student receives notification
   - Case appears in ESP teacher's VPF dashboard

## Notifications Sent

### To ESP Teachers
- **Title**: "VPF Case Assigned to Teacher"
- **Message**: Case details, student name, assigned teacher name
- **Action**: Schedule VPF session

### To Student
- **Title**: "VPF Teacher Assigned"
- **Message**: Case ID and assigned teacher name
- **Action**: Wait for session scheduling

## Integration Points

- **Manage Counselors**: VPF teachers are managed here (active counselors)
- **ESP Dashboard**: Assigned cases appear in ESP teacher's view
- **VPF Schedule**: ESP teachers can schedule sessions for assigned cases

## UI Elements

- **Green "Assign Teacher" button**: For unassigned cases
- **Green badge with checkmark**: Shows assigned teacher name
- **Modal dialog**: Clean, user-friendly assignment interface
- **Success messages**: Confirmation after assignment

## Database Schema

```
VPFCase
├── esp_teacher_assigned (FK to Counselor, nullable)
├── report (FK to IncidentReport)
├── student (FK to CustomUser)
├── assigned_by (FK to CustomUser - counselor)
├── commission_level
├── intervention
├── status
└── notes
```

## Testing Checklist

- [ ] Counselor can view VPF cases in "For VPF" page
- [ ] "Assign Teacher" button appears for unassigned cases
- [ ] Modal opens with correct case information
- [ ] VPF teachers list loads from Counselor model
- [ ] Assignment saves successfully
- [ ] Notifications sent to ESP teachers
- [ ] Notifications sent to student
- [ ] Assigned teacher name displays with checkmark
- [ ] Case appears in ESP teacher's dashboard
