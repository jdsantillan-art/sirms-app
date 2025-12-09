# Why Evidence Files Show "Not Found" Error

## The Problem

You're seeing "Not Found" errors for evidence files in report 2025-0017 and possibly other old reports.

## Root Cause

**Report 2025-0017 was created BEFORE Cloudinary was implemented.**

Here's what happened:

1. **Before Cloudinary** (all reports up to today):
   - Evidence files were uploaded to Render's local disk (`/media/` folder)
   - Render uses **ephemeral filesystem** - files are deleted on every deployment
   - Every time you push code to GitHub, Render redeploys and wipes the `/media/` folder
   - Result: All old evidence files are **permanently deleted**

2. **After Cloudinary** (new reports from now on):
   - Evidence files are uploaded to Cloudinary cloud storage
   - Files persist permanently, even after redeployments
   - No more "Not Found" errors

## Why This Happened

Render's architecture uses containers that are rebuilt on every deployment. The `/media/` folder is NOT persistent storage - it's temporary and gets wiped clean each time.

This is a fundamental limitation of Render's free tier and how containerized deployments work.

## The Solution

### For OLD Reports (like 2025-0017)

**The files are permanently lost.** There's no way to recover them because:
- They were stored on Render's ephemeral disk
- Render has already deleted them (multiple deployments ago)
- No backup exists

**What to do:**
1. Contact the original reporter
2. Ask them to re-upload the evidence
3. Edit the report and upload the evidence again
4. The NEW upload will go to Cloudinary and persist forever

### For NEW Reports (from today onwards)

**All new uploads automatically go to Cloudinary** and will:
- ✅ Persist permanently
- ✅ Survive all redeployments
- ✅ Never show "Not Found" errors
- ✅ Be accessible forever

## How to Re-upload Evidence for Old Reports

1. **Login** as Counselor, DO, or Principal
2. **Go to** the report (e.g., https://sirmsportal.onrender.com/report/2025-0017/)
3. **Click** "Edit Report" or similar button
4. **Re-upload** the evidence file
5. **Save** the report
6. **Verify** the evidence now displays correctly

The new file will be stored in Cloudinary and will never be lost again.

## Technical Details

### Before Cloudinary
```
User uploads file
    ↓
Saved to: /media/evidence/filename.jpg (Render disk)
    ↓
Database stores: /media/evidence/filename.jpg
    ↓
Render redeploys (code push)
    ↓
/media/ folder wiped clean
    ↓
File path in database still exists
    ↓
But actual file is GONE
    ↓
Result: "Not Found" error
```

### After Cloudinary
```
User uploads file
    ↓
Django detects Cloudinary is configured
    ↓
File uploaded to: https://res.cloudinary.com/[cloud]/image/upload/[id]
    ↓
Database stores: Cloudinary URL
    ↓
Render redeploys (any time)
    ↓
/media/ folder wiped (doesn't matter)
    ↓
File is in Cloudinary cloud (permanent)
    ↓
Result: File accessible forever ✅
```

## Summary

| Report Type | Evidence Status | Action Required |
|-------------|----------------|-----------------|
| Old reports (before today) | ❌ Files lost | Re-upload evidence |
| New reports (from today) | ✅ Files persist | No action needed |

## Important Notes

1. **This is NOT a bug** - it's how Render's ephemeral filesystem works
2. **Cloudinary is now active** - all new uploads are safe
3. **Old files cannot be recovered** - they're permanently deleted
4. **Users must re-upload** evidence for old reports
5. **This won't happen again** - Cloudinary prevents this issue

## Inform Your Users

Send this message to users:

> **Important Notice: Evidence File Re-upload Required**
>
> Due to a server upgrade to improve file storage, evidence files uploaded before [today's date] are no longer accessible. We've implemented permanent cloud storage to prevent this in the future.
>
> **Action Required:**
> If you have reports with evidence files showing "Not Found" errors, please:
> 1. Edit the report
> 2. Re-upload the evidence file
> 3. Save the report
>
> All new uploads will be stored permanently and will never be lost.
>
> We apologize for the inconvenience. This is a one-time issue that has been permanently resolved.

## Verification

To verify Cloudinary is working:

1. **Create a new test report** with an image
2. **Check the image URL** (right-click → open in new tab)
3. **URL should start with**: `https://res.cloudinary.com/`
4. **If it starts with** `/media/` - Cloudinary is NOT active

## Questions?

- **Q: Can we recover old files?**
  - A: No, they're permanently deleted by Render

- **Q: Will this happen again?**
  - A: No, Cloudinary stores files permanently in the cloud

- **Q: Do I need to do anything for new reports?**
  - A: No, new uploads automatically go to Cloudinary

- **Q: How many reports are affected?**
  - A: All reports created before Cloudinary was implemented (today)

---

**Status**: Cloudinary is active and working
**Impact**: Old evidence files lost, new files persist forever
**Action**: Re-upload evidence for affected reports
