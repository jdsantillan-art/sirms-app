# Google OAuth 404 Error Fix

## Problem
Getting "Not Found" error when Google redirects to `/auth/callback/`

## Root Causes

### 1. Missing Environment Variables in Render
The most common cause - OAuth credentials not set in Render.

### 2. Deployment Not Complete
Render might still be deploying the latest changes.

### 3. URL Configuration Issue
The callback URL might not be properly registered.

## Solution Steps

### Step 1: Set Render Environment Variables (CRITICAL)

Go to your Render dashboard → sirms service → Environment tab and add:

```
GOOGLE_OAUTH_CLIENT_ID=your_client_id_from_google_cloud_console
GOOGLE_OAUTH_CLIENT_SECRET=your_client_secret_from_google_cloud_console
SITE_URL=https://sirms.onrender.com
```

**How to get these values:**
1. Go to https://console.cloud.google.com/
2. Select your project
3. Go to **APIs & Services** → **Credentials**
4. Click on your OAuth 2.0 Client ID
5. Copy the **Client ID** and **Client secret**

### Step 2: Update Google Cloud Console Redirect URIs

In the same Google Cloud Console page:

1. Scroll to **Authorized redirect URIs**
2. Click **+ ADD URI**
3. Add: `https://sirms.onrender.com/auth/callback/`
4. Click **SAVE**
5. Wait 5-10 minutes for changes to propagate

### Step 3: Verify Deployment

1. Go to your Render dashboard
2. Check that the deployment is complete (green checkmark)
3. Look at the logs for any errors

### Step 4: Test the URLs

Try accessing these URLs directly:

1. Health check: `https://sirms.onrender.com/health/`
   - Should return: `{"status": "ok"}`

2. Login page: `https://sirms.onrender.com/auth/google/`
   - Should redirect to Google login

3. If you get 404 on health check, the deployment has issues

## Debugging

### Check Render Logs

In Render dashboard → Logs, look for:
- `DEBUG: Callback received` - means the callback is working
- Any Python errors or tracebacks
- `ModuleNotFoundError` or `ImportError`

### Test Locally First

1. Set environment variables locally:
```bash
set GOOGLE_OAUTH_CLIENT_ID=your_client_id
set GOOGLE_OAUTH_CLIENT_SECRET=your_client_secret
set SITE_URL=http://localhost:8000
```

2. Run the server:
```bash
python manage.py runserver
```

3. Test at: `http://localhost:8000/auth/google/`

### Common Issues

#### Issue 1: "Not Found" on callback
**Cause:** Environment variables not set in Render
**Fix:** Add GOOGLE_OAUTH_CLIENT_ID and GOOGLE_OAUTH_CLIENT_SECRET in Render

#### Issue 2: "redirect_uri_mismatch"
**Cause:** Redirect URI not added to Google Cloud Console
**Fix:** Add `https://sirms.onrender.com/auth/callback/` to authorized redirect URIs

#### Issue 3: "Invalid token"
**Cause:** Wrong client ID or secret
**Fix:** Double-check the values in Render match Google Cloud Console

#### Issue 4: Deployment keeps failing
**Cause:** Build errors or missing dependencies
**Fix:** Check Render build logs for errors

## Quick Checklist

- [ ] GOOGLE_OAUTH_CLIENT_ID set in Render
- [ ] GOOGLE_OAUTH_CLIENT_SECRET set in Render
- [ ] SITE_URL set to `https://sirms.onrender.com` in Render
- [ ] Redirect URI `https://sirms.onrender.com/auth/callback/` added to Google Cloud Console
- [ ] Waited 5-10 minutes after Google Cloud Console changes
- [ ] Render deployment shows as "Live" (green)
- [ ] Checked Render logs for errors
- [ ] Tested health check URL first

## Still Not Working?

1. Check Render deployment status - must be "Live"
2. Look at Render logs for Python errors
3. Verify Google Cloud Console project is correct
4. Try in incognito/private browsing mode
5. Clear browser cache completely

## Environment Variables Template

Copy this to your Render environment variables:

```
# Required for OAuth
GOOGLE_OAUTH_CLIENT_ID=YOUR_CLIENT_ID_HERE
GOOGLE_OAUTH_CLIENT_SECRET=YOUR_CLIENT_SECRET_HERE
SITE_URL=https://sirms.onrender.com

# Should already be set
DEBUG=false
ALLOWED_HOSTS=sirms.onrender.com
USE_POSTGRESQL=true
```

## Testing After Fix

1. Go to: `https://sirms.onrender.com/auth/google/`
2. Click "Sign in with Google"
3. Select your DMLMHS Google account
4. Should redirect to dashboard if successful
5. If you see "No access", check email format requirements
