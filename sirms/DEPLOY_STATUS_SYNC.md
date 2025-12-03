# Deploy Status Sync Feature - Checklist

## ✅ Implementation Complete

### Files Modified:
1. ✅ `incidents/do_schedule_views.py` - Added auto-sync logic
2. ✅ `incidents/behavior_concerns_views.py` - Added auto-sync logic

### Files Created:
1. ✅ `test_status_sync.py` - Test script
2. ✅ `AUTO_STATUS_SYNC_FEATURE.md` - Feature documentation
3. ✅ `STATUS_SYNC_VISUAL_GUIDE.md` - Visual guide
4. ✅ `DEPLOY_STATUS_SYNC.md` - This checklist

## Pre-Deployment Testing

### Local Testing Steps:

```bash
# 1. Test the synchronization
python test_status_sync.py

# 2. Run Django checks
python manage.py check

# 3. Test migrations (if any)
python manage.py makemigrations
python manage.py migrate

# 4. Run the development server
python manage.py runserver
```

### Manual Testing Checklist:

- [ ] Login as DO user
- [ ] Navigate to Behavioral Concerns page
- [ ] Find a case with status "Classified"
- [ ] Click "Schedule Appointment"
- [ ] Fill form and submit
- [ ] Verify status changed to "Under Review"
- [ ] Verify notifications were sent
- [ ] Navigate to DO Schedule page
- [ ] Find the created schedule
- [ ] Click "Mark as Complete"
- [ ] Verify status changed to "Resolved"
- [ ] Verify completion notifications were sent

## Deployment Steps

### Step 1: Commit Changes

```bash
git add incidents/do_schedule_views.py
git add incidents/behavior_concerns_views.py
git add test_status_sync.py
git add AUTO_STATUS_SYNC_FEATURE.md
git add STATUS_SYNC_VISUAL_GUIDE.md
git add DEPLOY_STATUS_SYNC.md
git commit -m "Add automatic status sync between Behavioral Concerns and DO Schedule"
```

### Step 2: Push to Repository

```bash
git push origin main
```

### Step 3: Deploy to Render (or your hosting)

If using Render:
```bash
# Render will auto-deploy on git push
# Monitor the deployment at: https://dashboard.render.com
```

If using manual deployment:
```bash
# SSH into server
ssh user@your-server.com

# Pull latest changes
cd /path/to/sirms
git pull origin main

# Restart the application
sudo systemctl restart sirms
# or
sudo supervisorctl restart sirms
```

### Step 4: Post-Deployment Verification

- [ ] Check application logs for errors
- [ ] Test schedule creation on production
- [ ] Verify status updates work
- [ ] Verify notifications are sent
- [ ] Check database for correct status values

## Rollback Plan

If issues occur, rollback using:

```bash
# Revert the commit
git revert HEAD

# Push the revert
git push origin main

# Or restore previous version
git checkout <previous-commit-hash>
git push -f origin main
```

## Database Considerations

**No migrations required** - This feature only modifies business logic, not database schema.

Existing status values used:
- `classified` - Pending schedule
- `under_review` - Scheduled
- `resolved` - Completed

## Monitoring

### What to Monitor:

1. **Status Updates:**
   - Check that statuses update correctly
   - Monitor for any stuck cases

2. **Notifications:**
   - Verify notifications are being created
   - Check notification delivery

3. **Performance:**
   - Monitor query performance
   - Check for any slowdowns

### Logging:

Add to your monitoring dashboard:
```python
# Track status changes
logger.info(f"Auto-sync: Report {report.case_id} status updated to {report.status}")

# Track notification creation
logger.info(f"Notification sent to {user.username} for report {report.case_id}")
```

## User Communication

### Announcement Template:

```
📢 New Feature: Automatic Status Updates

We've improved the Behavioral Concerns workflow!

When you create a DO Schedule:
✅ Status automatically updates to "Scheduled"
✅ All parties are notified automatically

When you complete a DO Schedule:
✅ Status automatically updates to "Resolved"
✅ Completion notifications sent automatically

No more manual status updates needed!

Questions? Contact the IT team.
```

## Training Materials

Share with DO staff:
1. `AUTO_STATUS_SYNC_FEATURE.md` - Technical overview
2. `STATUS_SYNC_VISUAL_GUIDE.md` - Visual guide with examples

## Success Criteria

Feature is successful if:
- ✅ Status updates automatically when schedule is created
- ✅ Status updates automatically when schedule is completed
- ✅ Notifications are sent to all relevant parties
- ✅ No manual status updates needed
- ✅ No errors in production logs
- ✅ User feedback is positive

## Support

### Common Issues:

**Issue:** Status not updating
- **Solution:** Check if report is linked to schedule
- **Check:** `schedule.report` should not be None

**Issue:** Notifications not sent
- **Solution:** Verify notification_type field exists
- **Check:** Database schema for Notification model

**Issue:** Wrong status value
- **Solution:** Verify status choices in model
- **Check:** IncidentReport.STATUS_CHOICES

## Timeline

- **Development:** ✅ Complete
- **Testing:** ⏳ In Progress
- **Deployment:** ⏳ Pending
- **Monitoring:** ⏳ Pending

## Sign-off

- [ ] Developer tested locally
- [ ] Code reviewed
- [ ] Documentation complete
- [ ] Ready for deployment

---

**Deployment Date:** _____________
**Deployed By:** _____________
**Status:** ⏳ Pending Deployment
