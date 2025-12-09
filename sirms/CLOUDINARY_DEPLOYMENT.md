# Cloudinary Deployment Guide

## ✅ Configuration Complete!

I've configured your SIRMS app to use Cloudinary for media storage. Here's what's left to do:

## What I Did

1. ✅ Added Cloudinary packages to `requirements.txt`
2. ✅ Updated `INSTALLED_APPS` in settings.py
3. ✅ Added Cloudinary configuration
4. ✅ Set up automatic media file storage

## What You Need To Do

### Step 1: Get Your Cloudinary Credentials

1. Go to: https://cloudinary.com/users/login
2. Login to your account
3. Copy these 3 values from the Dashboard:
   - **Cloud name** (example: `dab12cd34`)
   - **API Key** (example: `123456789012345`)
   - **API Secret** (example: `aBcDeFgHiJkLmNoPqRsTuVwXyZ`)

### Step 2: Add Environment Variables to Render

1. Go to: https://dashboard.render.com
2. Click on your SIRMS service
3. Click "Environment" in the left sidebar
4. Click "Add Environment Variable"
5. Add these THREE variables:

```
Name: CLOUDINARY_CLOUD_NAME
Value: [paste your cloud name]

Name: CLOUDINARY_API_KEY
Value: [paste your API key]

Name: CLOUDINARY_API_SECRET
Value: [paste your API secret]
```

6. Click "Save Changes"

### Step 3: Deploy to GitHub

```bash
cd sirms
git add requirements.txt sirms_project/settings.py
git commit -m "Add Cloudinary for media storage"
git push origin main
```

Or use GitHub Desktop:
1. Open GitHub Desktop
2. You'll see the changes
3. Write commit message: "Add Cloudinary for media storage"
4. Click "Commit to main"
5. Click "Push origin"

### Step 4: Wait for Render Deployment

- Render will automatically detect the push
- Wait 5-10 minutes for deployment
- Check deployment logs for any errors

### Step 5: Re-upload Evidence Files

**Important**: Existing evidence files were lost (Render's ephemeral filesystem).

Users will need to:
1. Go to their reports
2. Edit the report
3. Re-upload evidence images/videos
4. Save

**New uploads will now persist permanently!**

## How It Works

### Before (Broken)
```
User uploads image
    ↓
Saved to /media/ folder on Render
    ↓
Render redeploys
    ↓
❌ Files deleted (ephemeral filesystem)
    ↓
"Not Found" error
```

### After (Fixed)
```
User uploads image
    ↓
Automatically uploaded to Cloudinary
    ↓
Stored permanently in cloud
    ↓
Render redeploys
    ↓
✅ Files still accessible from Cloudinary
    ↓
Images/videos work perfectly
```

## Testing

After deployment:

1. **Upload a test image**
   - Create a new incident report
   - Upload an image as evidence
   - Submit the report

2. **View the report**
   - Go to the report detail page
   - Image should display correctly

3. **Trigger a redeploy**
   - Make any small change and push to GitHub
   - Wait for Render to redeploy
   - Check the report again
   - ✅ Image should still be there!

## Troubleshooting

### Images still not showing?
- Check that environment variables are set in Render
- Verify credentials are correct
- Check Render deployment logs for errors

### "Cloudinary" errors in logs?
- Make sure all 3 environment variables are set
- Check for typos in variable names
- Restart the Render service

### Old images still missing?
- This is expected - old files were lost
- Users need to re-upload evidence
- New uploads will persist

## Free Tier Limits

Cloudinary free tier includes:
- **25 GB storage** (plenty for your needs)
- **25 GB bandwidth/month**
- **25,000 transformations/month**

This is more than enough for a school incident reporting system!

## Summary

**Files Changed:**
- `requirements.txt` - Added Cloudinary packages
- `sirms_project/settings.py` - Added Cloudinary configuration

**Next Steps:**
1. Get Cloudinary credentials
2. Add to Render environment variables
3. Push to GitHub
4. Wait for deployment
5. Test by uploading new evidence

---

**Status**: ✅ Code ready - needs credentials and deployment
**Priority**: HIGH (fixes media file persistence)
**Risk**: LOW (only adds cloud storage)
