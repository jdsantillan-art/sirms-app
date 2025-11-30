# Requested Features - Implementation Guide

## Summary of Requested Features

### 1. ESP Teacher VPF Status Updates
- ESP Teachers can update VPF case status
- Status options: Pending, Ongoing, Complete
- Can add notes with each status update
- Guidance counselor receives notification on status change

### 2. DO Behavioral Concerns Evaluation
- DO can evaluate behavioral concerns
- Evaluation actions: Intake Interview, Investigate, Parent Conference
- Can add notes with evaluation
- Student (violator) receives notification

### 3. Bullying Type Dropdown
- When "Bullying" is selected in incident report
- Show dropdown with bullying types:
  - Physical
  - Psychological
  - Sexual
  - Emotional
  - Cyber
  - Social
  - Gender-based

### 4. Terminology Change: Case → Referral
- Change "Case ID" to "Referral ID"
- Change all "case" references to "referral"
- System-wide terminology update

## Implementation Complexity

| Feature | Complexity | Files | Est. Time | Priority |
|---------|-----------|-------|-----------|----------|
| Bullying Dropdown | Low | 2-3 | 20 min | High |
| ESP Status Update | Medium | 4-5 | 45 min | High |
| DO Evaluation | Medium | 4-5 | 45 min | Medium |
| Terminology Change | High | 30+ | 2-3 hrs | Medium |

## Recommendation

Due to the extensive scope (especially the terminology change affecting 30+ files), I recommend:

**Option A: Implement Features 1-3 Now**
- Quick implementation of bullying dropdown
- ESP status updates with notifications
- DO evaluation with notifications
- Provide detailed guide for terminology change

**Option B: Implement All Features**
- Complete implementation of all 4 features
- Will require 3-4 hours total
- Extensive testing needed
- Risk of breaking existing functionality

**Option C: Phased Approach**
- Phase 1: Bullying dropdown (today)
- Phase 2: ESP & DO features (today/tomorrow)
- Phase 3: Terminology change (separate session with testing)

## My Recommendation: Option A

Implement Features 1-3 now (functional improvements) and provide a comprehensive guide for Feature 4 (terminology change) that you can review and approve before implementation, since it affects the entire system.

Would you like me to proceed with Option A, or would you prefer a different approach?
