# Counseling Schedule System Flow

## Complete Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    REFERRAL EVALUATION                          │
│                  (Counselor evaluates case)                     │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │  Select Commission   │
              │  Select Intervention │
              │  Add Notes           │
              └──────────┬───────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │ Check Intervention   │
              │      Type            │
              └──────────┬───────────┘
                         │
         ┌───────────────┴───────────────┐
         │                               │
         ▼                               ▼
┌────────────────────┐         ┌────────────────────┐
│  VPF Intervention  │         │ Non-VPF Intervention│
│                    │         │                     │
│ • Values Reflective│         │ • Parent Conference │
│   Formation        │         │ • Counseling/Follow │
│                    │         │ • Supervised Interv │
└────────┬───────────┘         └────────┬───────────┘
         │                               │
         ▼                               ▼
┌────────────────────┐         ┌────────────────────┐
│   VPF SCHEDULE     │         │ COUNSELING SCHEDULE│
│  (ESP Teacher)     │         │   (Counselor)      │
│                    │         │                    │
│ • Managed by ESP   │         │ • Managed by       │
│   Teacher          │         │   Counselor        │
│ • VPF Cases page   │         │ • Auto-redirect    │
│ • VPF Schedule page│         │ • Schedule modal   │
└────────────────────┘         └────────┬───────────┘
                                        │
                                        ▼
                         ┌──────────────────────────┐
                         │  COUNSELING SCHEDULE     │
                         │         PAGE             │
                         │                          │
                         │ ┌──────────────────────┐ │
                         │ │ Pending Cases        │ │
                         │ │ (Need Scheduling)    │ │
                         │ └──────────────────────┘ │
                         │                          │
                         │ ┌──────────────────────┐ │
                         │ │ Calendar View        │ │
                         │ │ (Monthly Display)    │ │
                         │ └──────────────────────┘ │
                         │                          │
                         │ ┌──────────────────────┐ │
                         │ │ List View            │ │
                         │ │ (Table Format)       │ │
                         │ └──────────────────────┘ │
                         └────────┬─────────────────┘
                                  │
                                  ▼
                    ┌─────────────────────────┐
                    │  SCHEDULE SESSION       │
                    │                         │
                    │ • Select Date/Time      │
                    │ • Add Location          │
                    │ • Add Notes             │
                    │ • Click "Schedule"      │
                    └────────┬────────────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │  NOTIFICATIONS SENT  │
                  │                      │
                  │ ✉️ Student           │
                  │ ✉️ Reporter (Teacher)│
                  └──────────┬───────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │  SESSION SCHEDULED   │
                  │                      │
                  │ • Appears in Calendar│
                  │ • Appears in List    │
                  │ • Status: Scheduled  │
                  └──────────┬───────────┘
                             │
                             ▼
              ┌──────────────────────────────┐
              │   SESSION DAY ARRIVES        │
              └──────────┬───────────────────┘
                         │
         ┌───────────────┴───────────────┐
         │                               │
         ▼                               ▼
┌────────────────────┐         ┌────────────────────┐
│ Student Attends    │         │ Student Misses     │
│                    │         │                    │
│ Counselor marks:   │         │ Counselor marks:   │
│ ✅ COMPLETED       │         │ ❌ MISSED          │
└────────┬───────────┘         └────────┬───────────┘
         │                               │
         ▼                               ▼
┌────────────────────┐         ┌────────────────────┐
│ Notification:      │         │ Notification:      │
│ "Session Completed"│         │ "Session Missed"   │
│ → Student          │         │ → Student          │
└────────────────────┘         └────────────────────┘
```

## Key Decision Points

### 1. Intervention Type Check
```
IF intervention contains "VPF" OR "Values Reflective Formation"
    THEN → Route to VPF Schedule (ESP Teacher)
ELSE
    THEN → Route to Counseling Schedule (Counselor)
```

### 2. Commission Levels
```
1st Commission:
  ├─ Parent Conference with Adviser/Subject Teacher → Counseling Schedule
  └─ Counseling/Follow-up/Supervised Intervention → Counseling Schedule

2nd Commission:
  ├─ Parent Conference → Counseling Schedule
  ├─ Counseling/Follow-up/Supervised Intervention → Counseling Schedule
  └─ Values Reflective Formation (VPF) → VPF Schedule

3rd Commission:
  ├─ Parent Conference → Counseling Schedule
  ├─ Counseling/Follow-up/Supervised Intervention → Counseling Schedule
  └─ Values Reflective Formation (VPF) → VPF Schedule
```

## Data Flow

```
┌──────────────┐
│ CaseEvaluation│
│   (Created)   │
└───────┬───────┘
        │
        ▼
┌──────────────────┐
│ CounselingSchedule│
│    (Created)      │
│                   │
│ • evaluation_id   │
│ • counselor_id    │
│ • student_id      │
│ • scheduled_date  │
│ • location        │
│ • notes           │
│ • status          │
└───────┬───────────┘
        │
        ▼
┌──────────────────┐
│  Notifications   │
│   (Created)      │
│                  │
│ • To Student     │
│ • To Reporter    │
└──────────────────┘
```

## Status Lifecycle

```
┌─────────────┐
│  SCHEDULED  │ ← Initial status when created
└──────┬──────┘
       │
       ├─────────────┐
       │             │
       ▼             ▼
┌─────────────┐  ┌─────────────┐
│  COMPLETED  │  │   MISSED    │
└─────────────┘  └──────┬──────┘
                        │
                        ▼
                 ┌─────────────┐
                 │ RESCHEDULED │ (Future feature)
                 └─────────────┘
```

## User Roles & Access

```
┌─────────────────────────────────────────────────────┐
│                    COUNSELOR                        │
│                                                     │
│ ✓ Evaluate cases                                   │
│ ✓ Schedule counseling sessions                     │
│ ✓ View all schedules                               │
│ ✓ Mark sessions as completed/missed                │
│ ✓ Manage non-VPF interventions                     │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│                   ESP TEACHER                       │
│                                                     │
│ ✓ View VPF cases                                   │
│ ✓ Schedule VPF sessions                            │
│ ✓ Manage VPF interventions only                    │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│                     STUDENT                         │
│                                                     │
│ ✓ Receive notifications                            │
│ ✓ View their own counseling schedule               │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│                TEACHER (Reporter)                   │
│                                                     │
│ ✓ Receive notifications when session scheduled     │
│ ✓ View case status updates                         │
└─────────────────────────────────────────────────────┘
```

## Integration Points

```
┌─────────────────┐
│ Referral        │
│ Evaluation      │ ──────┐
└─────────────────┘       │
                          │
┌─────────────────┐       │
│ Case Evaluation │       │
│ Model           │ ◄─────┤
└─────────────────┘       │
                          │
┌─────────────────┐       │
│ Counseling      │       │
│ Schedule Model  │ ◄─────┤
└─────────────────┘       │
                          │
┌─────────────────┐       │
│ Notification    │       │
│ System          │ ◄─────┘
└─────────────────┘
```
