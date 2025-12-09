# Repeat Offender Detection Workflow

## Complete Workflow Integration

This document shows how automatic repeat offender detection integrates with the existing SIRMS workflow.

## Step-by-Step Process

### Step 1: Incident Reported
- Teacher/Student reports an incident
- System creates new IncidentReport
- Automatically checks if student has previous violations
- No manual action needed

### Step 2: DO Reviews Report
What DO Sees:
- Case ID with student name
- Red badge if repeat offender: REPEATED (2x)
- Can immediately identify patterns

### Step 3: DO Classifies Case
- If Major → Routes to Guidance Counselor
- If Minor → DO handles directly
- Repeat offender status carries forward

### Step 4: Guidance Counselor Evaluates
What Counselor Sees:
- Student name with repeat badge
- Automatic note in evaluation
- Can make informed intervention decision

### Step 5: Intervention Assignment
Based on Repeat Offender Status:
- 1st offense → Counseling session
- 2nd offense → VRF 1st Commission
- 3rd offense → VRF 2nd Commission
- 4th+ offense → VRF 3rd Commission + Parent conference

### Step 6: Ongoing Monitoring
- System tracks all future violations
- Updates repeat count automatically
- Flags escalating patterns
- Supports data-driven decisions

## Quick Reference

Badge Meanings:
- No badge = First offense
- REPEATED (1x) = Second offense
- REPEATED (2x) = Third offense
- REPEATED (3x+) = Chronic offender

Quick Actions:
1. See badge → Click report for details
2. Review history → Check violation patterns
3. Assess severity → Consider cumulative impact
4. Select intervention → Match to offense count
5. Monitor progress → Track future violations

Status: Fully Integrated
Date: December 9, 2025
