# Behavior Concerns Feature

## Overview
The "Behavior Concerns" page replaces "Classify Violations" and shows only cases that were routed to the Discipline Office (DO) for handling. DO staff can monitor these cases, update their status, and automatically notify reporters.

## Key Features

### 1. Filtered Case View
- Shows only cases routed to DO (not sent to counselor)
- Clean, organized interface
- Real-time statistics dashboard

### 2. Status Management
DO can update case status to:
- **Pending** - Awaiting action
- **Under Review** - Being processed
- **Completed** - Case resolved

### 3. Automatic Notifications
When status is updated:
- ✉️ Reporter receives detailed notification
- ✉️ Student receives notification (if applicable)
- 📝 Notes are timestamped and saved

### 4. Case Tracking
- View all case details
- See classification notes
- Track status history
- Monitor progress

## How to Use

### Access Behavior Concerns:
1. Login as DO
2. Click "Behavior Concerns" in sidebar
3. View all DO-handled cases

### Update Case Status:
1. Find the case in the list
2. Click "Update Status" button
3. Select new status
4. Add required notes
5. Click "Update & Notify"
6. Reporter and student automatically notified

## Benefits
- ✅ Focused view of DO cases only
- ✅ Easy status tracking
- ✅ Automatic notifications
- ✅ Complete audit trail
- ✅ Better case management

## Technical Details
- **View**: `behavior_concerns` in `views.py`
- **Template**: `templates/do/behavior_concerns.html`
- **URL**: `/behavior-concerns/`
- **Filters**: Cases with `classification.severity='minor'`
