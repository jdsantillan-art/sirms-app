# Manual Deployment Instructions

## Current Status
- ✅ All code changes are committed
- ✅ Commit `afbf119` is on origin/main
- ⏳ Render should be auto-deploying

## If You Need to Force Deploy

### Option 1: Using Git Bash or Terminal
```bash
cd sirms
git add .
git commit -m "Force deploy" --allow-empty
git push origin main
```

### Option 2: Using Windows Command Prompt
```cmd
cd sirms
git add .
git commit -m "Force deploy" --allow-empty
git push origin main
```

### Option 3: Using the Batch File
```cmd
cd sirms
quick_deploy.bat
```

### Option 4: Manual Render Redeploy
1. Go to https://dashboard.render.com
2. Find your "sirmsportal" service
3. Click "Manual Deploy" button
4. Select "Deploy latest commit"
5. Click "Deploy"

## Verify Deployment

### Check Build Status:
1. Go to Render Dashboard
2. Click on "sirmsportal"
3. Check "Events" tab for deployment status
4. Look for "Deploy succeeded" message

### Check Live Site:
1. Visit: https://sirmsportal.onrender.com
2. Login as DO
3. Go to: /behavior-concerns/
4. Click "Evaluate Case" button
5. Verify simple dropdown appears

## What's Being Deployed

### Latest Commit: afbf119
**Features:**
1. ✅ Simplified Behavior Concerns evaluation
2. ✅ 3-option status dropdown (Pending, Ongoing, Completed)
3. ✅ Automatic case locking when completed
4. ✅ Auto-notifications to student, adviser, reporter
5. ✅ Repeat offender detection with badges
6. ✅ Schedule notification detail view
7. ✅ DO Schedule integration
8. ✅ Improved student name matching

## Troubleshooting

### If Deployment Fails:

**Check Logs:**
```
Render Dashboard → sirmsportal → Logs
```

**Common Issues:**
- Build timeout: Wait and retry
- Python errors: Check logs for details
- Database errors: Usually auto-resolves

**Force Fresh Deploy:**
```bash
git commit --allow-empty -m "Redeploy"
git push origin main --force
```

## Expected Timeline

- **Build:** 4-6 minutes
- **Deploy:** 4-6 minutes  
- **Total:** 8-12 minutes

## Contact

If issues persist:
1. Check Render dashboard
2. Review build logs
3. Verify git push succeeded
4. Try manual deploy from Render UI

---

**Last Updated:** December 2, 2025
**Status:** Ready to Deploy
**Commit:** afbf119
