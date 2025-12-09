# Fix Google OAuth - Quick Guide

## The Problem
You're getting: **Error 400: redirect_uri_mismatch**

This means Google doesn't recognize your redirect URI.

## The Fix (5 Minutes)

### Step 1: Go to Google Cloud Console
1. Visit: https://console.cloud.google.com/
2. Select your SIRMS project
3. Click **APIs & Services** → **Credentials**

### Step 2: Find Your OAuth Client
1. Look for "OAuth 2.0 Client IDs"
2. Click on your client (probably named "Web client" or similar)

### Step 3: Add Redirect URIs
In the **Authorized redirect URIs** section, click **+ ADD URI** and add:

```
https://sirms.onrender.com/auth/callback/
```

**CRITICAL:** Include the trailing slash `/` at the end!

Also add for local testing:
```
http://localhost:8000/auth/callback/
```

### Step 4: Save
1. Click **SAVE** at the bottom
2. Wait 5-10 minutes for changes to take effect

### Step 5: Test
1. Clear your browser cache (Ctrl+Shift+Delete)
2. Go to: https://sirms.onrender.com/auth/google/
3. Try logging in

## Still Not Working?

### Check Render Environment Variables
Go to your Render dashboard → sirms service → Environment:

Make sure these are set:
- `SITE_URL` = `https://sirms.onrender.com`
- `GOOGLE_OAUTH_CLIENT_ID` = (your client ID from Google)
- `GOOGLE_OAUTH_CLIENT_SECRET` = (your client secret from Google)

### Run Verification Script
```bash
python verify_google_oauth.py
```

This will show you exactly what's configured.

## Common Mistakes

❌ **Wrong:** `https://sirms.onrender.com/auth/callback` (no trailing slash)
✅ **Correct:** `https://sirms.onrender.com/auth/callback/`

❌ **Wrong:** Using `http://` for Render
✅ **Correct:** Using `https://` for Render

❌ **Wrong:** Using `https://` for localhost
✅ **Correct:** Using `http://` for localhost

## Need Help?

If you're still stuck, run the verification script and share the output:
```bash
cd sirms
python verify_google_oauth.py
```
