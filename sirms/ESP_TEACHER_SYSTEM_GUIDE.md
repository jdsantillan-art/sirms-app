# ESP Teacher Management System - Complete Guide

## Overview
The ESP Teacher (Values Reflective Formation Coordinator) system allows guidance counselors to manage up to 5 ESP teachers and assign them to VPF (Values Reflective Formation) cases.

## Features

### 1. Manage ESP Teachers
**Location:** Dashboard → Manage ESP Teachers

**Capabilities:**
- Add up to 5 ESP teachers
- View all registered ESP teachers
- Edit teacher information
- Deactivate teachers (only if they have no active cases)

**Teacher Information Stored:**
- **Name:** Full name of the ESP teacher
- **Email:** Format: `lastnameespteacher@gmail.com`
- **Phone:** Format: `09XX XXX XXXX` (11 digits)
- **Specialization:** e.g., Values Education, Behavioral Counseling, Character Formation

### 2. For VPF Page
**Location:** Dashboard → For VPF

**Features:**
- View all VPF cases
- See pending assignments (cases without ESP teachers)
- See assigned cases (cases with ESP teachers)
- Statistics dashboard showing:
  - Total VPF cases
  - Pending assignments
  - Assigned cases

**Pending VPF Cases Table:**
- Case ID
- Student name and grade/section
- Commission level
- Intervention type
- Assigned date
- **Action:** "Assign Teacher" button

**Assigned VPF Cases Table:**
- Case ID
- Student name and grade/section
- ESP Teacher name and specialization
- Contact information (email and phone)
- Status (Pending, Scheduled, Ongoing, Completed)
- View Details link

### 3. Assign ESP Teacher
**Location:** For VPF → Click "Assign Teacher" on any pending case

**Process:**
1. View VPF case details (Commission level, Intervention, Status)
2. Select an ESP teacher from the dropdown list
3. Each teacher card shows:
   - Name
   - Email
   - Phone
   - Specialization
   - Active case count (or "Available" badge)
4. Click "Assign Teacher" to complete assignment

**Dropdown Display:**
The dropdown shows all active ESP teachers with their complete information in a card format, making it easy to select the most appropriate teacher based on:
- Workload (number of active cases)
- Specialization
- Contact availability

## How to Use

### Step 1: Add ESP Teachers
1. Go to **Dashboard** → **Manage ESP Teachers**
2. Click **"Add ESP Teacher"** button
3. Fill in the form:
   - Name: e.g., "Maria Santos"
   - Email: e.g., "santosespteacher@gmail.com"
   - Phone: e.g., "09171234567"
   - Specialization: e.g., "Values Education"
4. Click **"Save ESP Teacher"**
5. Repeat until you have up to 5 teachers

### Step 2: View VPF Cases
1. Go to **Dashboard** → **For VPF**
2. View statistics at the top
3. Check **"Pending ESP Teacher Assignment"** section for unassigned cases
4. Check **"Assigned VPF Cases"** section for cases with teachers

### Step 3: Assign Teacher to VPF Case
1. In the **"Pending ESP Teacher Assignment"** table
2. Find the case you want to assign
3. Click **"Assign Teacher"** button
4. Review the VPF case details
5. Select an ESP teacher from the list (radio button selection)
6. Click **"Assign Teacher"** to confirm
7. The case will move to the "Assigned VPF Cases" section

### Step 4: Monitor Assigned Cases
1. Go to **For VPF** page
2. View the **"Assigned VPF Cases"** table
3. See teacher contact information for each case
4. Monitor case status
5. Click **"View Details"** to see full case information

## Email Format Requirements

### ESP Teacher Email Format
- Pattern: `lastnameespteacher@gmail.com`
- Examples:
  - `santosespteacher@gmail.com`
  - `delacruzespteacher@gmail.com`
  - `reyesespteacher@gmail.com`

### Phone Format
- Pattern: `09XX XXX XXXX`
- Must be 11 digits
- Examples:
  - `09171234567`
  - `09181234568`
  - `09191234569`

## Populating Sample Data

To quickly add 5 sample ESP teachers, run:

```bash
python populate_esp_teachers.py
```

This will create 5 ESP teachers with sample data:
1. Maria Santos - Values Education
2. Juan Dela Cruz - Behavioral Counseling
3. Ana Reyes - Character Formation
4. Pedro Garcia - Moral Development
5. Rosa Martinez - Student Guidance

## Database Structure

### Counselor Model
The ESP teachers are stored in the `Counselor` model with these fields:
- `name` - Full name (auto-capitalized)
- `email` - Email address (unique)
- `phone` - Contact number
- `specialization` - Area of expertise
- `is_active` - Active status (default: True)

### VPFCase Model
VPF cases link to ESP teachers through:
- `esp_teacher_assigned` - Foreign key to Counselor model
- `status` - Case status (pending, scheduled, ongoing, completed)
- `student` - Student assigned to VPF
- `report` - Related incident report
- `commission_level` - 1st, 2nd, or 3rd Commission
- `intervention` - Type of intervention

## Workflow

```
1. Guidance Counselor evaluates case
   ↓
2. Decides case needs VPF intervention
   ↓
3. Creates VPF case with commission level and intervention
   ↓
4. Case appears in "For VPF" → "Pending Assignment"
   ↓
5. Counselor clicks "Assign Teacher"
   ↓
6. Selects appropriate ESP teacher from dropdown
   ↓
7. Case moves to "Assigned VPF Cases"
   ↓
8. ESP teacher receives notification
   ↓
9. ESP teacher schedules and conducts VPF sessions
   ↓
10. Case status updates (scheduled → ongoing → completed)
```

## Access Control

### Guidance Counselor Can:
- ✅ Manage ESP teachers (add, edit, deactivate)
- ✅ View all VPF cases
- ✅ Assign ESP teachers to VPF cases
- ✅ Monitor case progress

### ESP Teacher Can:
- ✅ View assigned VPF cases
- ✅ Update case status
- ✅ Schedule VPF sessions
- ✅ Add session notes

### Discipline Officer Can:
- ✅ View VPF cases (read-only)

## Limitations

1. **Maximum 5 ESP Teachers:** System enforces a limit of 5 active ESP teachers
2. **Cannot Delete Teachers with Active Cases:** Must complete or reassign cases first
3. **Unique Email Addresses:** Each ESP teacher must have a unique email
4. **Required Fields:** Name, email, and phone are mandatory

## Troubleshooting

### Cannot Add More Teachers
- **Issue:** "Maximum of 5 ESP teachers reached"
- **Solution:** Deactivate an existing teacher (only if they have no active cases)

### Cannot Deactivate Teacher
- **Issue:** "Cannot deactivate. This teacher has X active case(s)"
- **Solution:** Complete or reassign their active cases first

### Email Already Exists
- **Issue:** "This email address is already registered"
- **Solution:** Use a different email address or edit the existing teacher

### No Teachers in Dropdown
- **Issue:** "No ESP Teachers Available"
- **Solution:** Add ESP teachers first via "Manage ESP Teachers"

## URLs Reference

- Manage ESP Teachers: `/manage-esp-teachers/`
- Add ESP Teacher: `/esp-teacher/add/`
- Edit ESP Teacher: `/esp-teacher/<id>/edit/`
- Delete ESP Teacher: `/esp-teacher/<id>/delete/`
- For VPF: `/for-vpf/`
- Assign Teacher: `/vpf-case/<id>/assign-teacher/`

## Related Documentation

- `ESP_TEACHER_FEATURE.md` - Feature implementation details
- `VPF_COUNSELING_WORKFLOW.md` - VPF counseling process
- `DEPLOYMENT_DEC3_2025.md` - Latest deployment information

---

**Last Updated:** December 4, 2025
**System Version:** SIRMS v2.0
**Feature Status:** ✅ Fully Implemented and Deployed
