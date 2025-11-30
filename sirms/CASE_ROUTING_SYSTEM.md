# Case Routing System - DO Classification Update

## Overview
Updated the DO classification system to focus on **case routing decisions** rather than severity levels. The DO now decides whether to handle the case internally or refer it to the Guidance Counselor.

## Key Changes

### Previous System:
- DO classified cases as "Minor" or "Major" violations
- Classification was based on severity

### New System:
- DO makes **routing decisions** based on case requirements
- Two routing options:
  1. **Handle by Discipline Office (DO)** - For cases DO can manage
  2. **Send to Guidance Counselor** - For cases requiring counseling

## Routing Options Explained

### 🏢 Handle by Discipline Office (DO)
**When to use:**
- Minor policy violations
- First-time offenses
- Cases requiring warnings or sanctions
- Disciplinary actions that don't need counseling
- Behavioral issues DO can monitor

**What happens:**
- Case stays with DO for handling
- DO staff receive notification
- Student notified case is under DO review
- DO can apply sanctions, warnings, monitoring

**Examples:**
- Uniform violations
- Tardiness
- Minor classroom disruptions
- First-time minor infractions

### 🧠 Send to Guidance Counselor
**When to use:**
- Major violations requiring intervention
- Behavioral issues needing assessment
- Repeated offenses
- Cases involving emotional/psychological factors
- Situations requiring counseling support

**What happens:**
- Case forwarded to Guidance Office
- All counselors receive notification
- Student notified about counseling requirement
- Counselor schedules session and provides intervention

**Examples:**
- Bullying incidents
- Aggressive behavior
- Emotional distress cases
- Repeated violations
- Cases requiring behavioral modification

## Workflow

### Step 1: Evidence Verification
```
DO reviews report → Checks evidence
├─ ✅ Clear: Proceed to routing
└─ ⚠️ Insufficient: Request more evidence from reporter
```

### Step 2: Case Routing (if evidence clear)
```
DO evaluates case nature
├─ 🏢 Handle by DO: Minor violations, DO can manage
└─ 🧠 Send to Counselor: Major violations, needs counseling
```

### Step 3: Notifications
```
Routing Decision Made
├─ If DO: Notify DO staff + Student
└─ If Counselor: Notify Counselors + Student
```

## Benefits

1. **Clear Decision Framework**: DO knows exactly what to decide
2. **Appropriate Intervention**: Cases go to the right department
3. **Efficient Resource Use**: Counselors focus on cases needing their expertise
4. **Better Student Support**: Students get appropriate level of intervention
5. **Streamlined Process**: Clear path from report to resolution

## Technical Implementation

### Database Changes
- Updated `Classification.severity` field choices
- Added `ROUTING_CHOICES` constant
- Added `get_routing_destination()` helper method

### Notification Updates
- DO routing: Notifies DO staff and student
- Counselor routing: Notifies counselors and student
- Clear messaging about next steps

### UI Changes
- Replaced dropdown with radio buttons
- Clear descriptions for each routing option
- Visual distinction (blue for DO, purple for Counselor)
- Better user guidance

## Migration
Applied migration: `0014_alter_classification_internal_notes_and_more.py`

## Usage Guide for DO Staff

### When to Route to DO:
✅ Student can be corrected with warnings/sanctions
✅ First-time minor offense
✅ Clear policy violation with straightforward resolution
✅ No underlying behavioral/emotional issues

### When to Route to Counselor:
✅ Pattern of repeated violations
✅ Behavioral issues requiring assessment
✅ Emotional/psychological factors involved
✅ Bullying or interpersonal conflicts
✅ Student needs support beyond discipline

## Future Enhancements
- Add routing history tracking
- Generate routing statistics
- Create routing guidelines reference
- Add routing decision templates
