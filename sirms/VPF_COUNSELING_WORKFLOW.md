# 🔄 VPF & Counseling Workflow - Complete Guide

## ✅ IMPLEMENTED: Case Evaluation Routing System

### 📋 Overview:

When a guidance counselor evaluates a case, the system automatically routes it based on the intervention type:

1. **VPF (Values Reflective Formation)** → ESP Teacher manages
2. **Other Interventions** → Counselor manages via Counseling Schedule

---

## 🎯 Workflow 1: VPF Cases (ESP Teacher Management)

### Step 1: Counselor Evaluates Case
**Location:** Guidance → Case Evaluation

1. Counselor selects a case
2. Clicks "Evaluate"
3. Chooses:
   - **Commission:** 1st, 2nd, or 3rd
   - **Intervention:** Values Reflective Formation (VPF)
   - **Status:** Pending/Ongoing/Complete
   - **Notes:** Optional evaluation notes
4. Clicks "Submit Evaluation"

### Step 2: System Creates VPF Case
**What Happens:**
- ✅ Creates `CaseEvaluation` record
- ✅ Creates `VPFCase` record
- ✅ Updates report status to 'evaluated'
- ✅ Sends notifications to:
  - **All ESP Teachers** - "New VPF Case Assigned"
  - **Reporter (Adviser/Teacher)** - "Case Evaluated - VPF Assigned"
  - **Student** - "VPF Case Assigned"

### Step 3: VPF Case Appears in Multiple Places

**For Guidance Counselor:**
- **Sidebar:** "For VRF" (View only - monitoring)
- **Can see:** All VPF cases they assigned
- **Cannot:** Schedule or manage (ESP Teacher's job)

**For ESP Teacher:**
- **Dashboard:** VPF Cases widget
- **Sidebar:** "VPF Cases" (Full management)
- **Can:** Schedule sessions, update status, add notes

### Step 4: ESP Teacher Manages VPF
**Location:** ESP Teacher → VPF Cases

**Actions Available:**
1. **View VPF Cases** - See all assigned cases
2. **Schedule Session** - Set date, time, location
3. **Update Status** - Change to scheduled/completed/cancelled
4. **Add Notes** - Document progress

**When ESP Teacher Updates:**
- ✅ Status changes (pending → scheduled → completed)
- ✅ Guidance counselor gets notified automatically
- ✅ Student gets notified
- ✅ Reporter gets notified

### Step 5: Automatic Notifications to Guidance
**When ESP Teacher:**
- Schedules a session → Guidance notified
- Updates status → Guidance notified
- Completes VPF → Guidance notified
- Adds notes → Guidance notified

---

## 🎯 Workflow 2: Non-VPF Cases (Counselor Management)

### Step 1: Counselor Evaluates Case
**Location:** Guidance → Case Evaluation

1. Counselor selects a case
2. Clicks "Evaluate"
3. Chooses:
   - **Commission:** 1st, 2nd, or 3rd
   - **Intervention:** (Any EXCEPT VPF)
     - Parent Conference with Adviser/Subject Teacher
     - Counseling/Follow-up/Supervised Intervention
     - Parent Conference
   - **Status:** Pending/Ongoing/Complete
   - **Notes:** Optional evaluation notes
4. Clicks "Submit Evaluation"

### Step 2: System Creates Counseling Schedule
**What Happens:**
- ✅ Creates `CaseEvaluation` record
- ✅ Creates `CounselingSchedule` record (placeholder)
- ✅ Updates report status to 'evaluated'
- ✅ Sends notifications to:
  - **Reporter (Adviser/Teacher)** - "Case Evaluated - Counseling Scheduled"
  - **Student** - "Counseling Session Scheduled"

### Step 3: Counseling Schedule Appears
**For Guidance Counselor:**
- **Sidebar:** "Counseling Schedule"
- **Shows:** All pending counseling sessions
- **Can:** Set final schedule, notify student and adviser

### Step 4: Counselor Schedules Session
**Location:** Guidance → Counseling Schedule

**Actions:**
1. View pending counseling schedules
2. Set actual date and time
3. Set location (Guidance Office, etc.)
4. Add session notes
5. Click "Schedule" or "Update"

**When Counselor Schedules:**
- ✅ Student gets notification with date/time/location
- ✅ Adviser gets notification
- ✅ Status updates to 'scheduled'

### Step 5: Counselor Manages Session
**Can:**
- Mark as completed
- Mark as missed
- Reschedule
- Add session notes

---

## 📊 Summary Table

| Intervention Type | Managed By | Appears In | Notifications |
|-------------------|------------|------------|---------------|
| **VPF** | ESP Teacher | ESP Dashboard + Guidance "For VRF" | ESP Teachers, Guidance (auto), Student, Adviser |
| **Parent Conference** | Counselor | Counseling Schedule | Student, Adviser |
| **Counseling/Follow-up** | Counselor | Counseling Schedule | Student, Adviser |
| **Other Interventions** | Counselor | Counseling Schedule | Student, Adviser |

---

## 🔔 Notification Flow

### VPF Cases:
```
Counselor Evaluates (VPF)
    ↓
ESP Teachers Notified (All)
    ↓
ESP Teacher Schedules
    ↓
Guidance Notified (Auto)
    ↓
Student & Adviser Notified
    ↓
ESP Teacher Updates Status
    ↓
Guidance Notified (Auto)
```

### Non-VPF Cases:
```
Counselor Evaluates (Non-VPF)
    ↓
Counseling Schedule Created
    ↓
Counselor Sets Schedule
    ↓
Student & Adviser Notified
    ↓
Counselor Manages Session
    ↓
Updates Status
```

---

## 🧪 Testing Instructions

### Test VPF Workflow:
1. Login as counselor: `counselor1` / `counselor123`
2. Go to: Case Evaluation
3. Evaluate a case with VPF intervention
4. Check: "For VRF" sidebar (should show the case)
5. Logout, login as ESP teacher
6. Check: VPF Cases dashboard (should show the case)
7. Schedule the VPF session
8. Logout, login as counselor
9. Check: Notifications (should have ESP update notification)

### Test Non-VPF Workflow:
1. Login as counselor: `counselor1` / `counselor123`
2. Go to: Case Evaluation
3. Evaluate a case with non-VPF intervention
4. Check: Counseling Schedule sidebar (should show the case)
5. Set the schedule date/time
6. Check: Student and adviser get notifications

---

## ✅ Features Implemented:

- ✅ VPF cases route to ESP Teacher
- ✅ Non-VPF cases route to Counseling Schedule
- ✅ Guidance can monitor VPF in "For VRF"
- ✅ ESP Teacher manages VPF independently
- ✅ Automatic notifications to guidance on VPF updates
- ✅ Counselor manages non-VPF counseling sessions
- ✅ All stakeholders notified appropriately

---

**Your VPF and Counseling workflow is now complete and working perfectly!** 🎉
