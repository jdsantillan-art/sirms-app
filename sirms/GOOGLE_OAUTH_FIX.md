# Google OAuth Redirect URI Fix

## Problem
Error 400: redirect_uri_mismatch - The redirect URI in your Google Cloud Console doesn't match what your app is sending.

## Solution

### Step 1: Get Your Render App URL
Your app is deployed at: `https://sirms.onrender.com`

### Step 2: Update Google Cloud Console

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Select your project
3. Navigate to: **APIs & Services** → **Credentials**
4. Click on your OAuth 2.0 Client ID
5. Under **Authorized redirect URIs**, add these URIs:

```
https://sirms.onrender.com/auth/callback/
http://localhost:8000/auth/callback/
```

**IMPORTANT:** Make sure to include the trailing slash `/` at the end!

### Step 3: Verify Render Environment Variables

In your Render dashboard, ensure these environment variables are set:

```
SITE_URL=https://sirms.onrender.com
GOOGLE_OAUTH_CLIENT_ID=your_client_id_here
GOOGLE_OAUTH_CLIENT_SECRET=your_client_secret_here
```

### Step 4: Optional - Set Explicit Redirect URI

If you want to be extra sure, you can set an explicit redirect URI in Render:

```
GOOGLE_OAUTH_REDIRECT_URI=https://sirms.onrender.com/auth/callback/
```

## Common Issues

### Issue 1: Missing Trailing Slash
❌ Wrong: `https://sirms.onrender.com/auth/callback`
✅ Correct: `https://sirms.onrender.com/auth/callback/`

### Issue 2: HTTP vs HTTPS
- Production (Render): Use `https://`
- Local development: Use `http://`

### Issue 3: Multiple Domains
If you have multiple domains, add ALL of them to Google Cloud Console:
- `https://sirms.onrender.com/auth/callback/`
- `https://your-custom-domain.com/auth/callback/`
- `http://localhost:8000/auth/callback/`

## Testing

After updating Google Cloud Console:

1. Wait 5-10 minutes for changes to propagate
2. Clear your browser cache
3. Try logging in again at: `https://sirms.onrender.com/auth/google/`

## Quick Reference

**Your OAuth URLs:**
- Login: `https://sirms.onrender.com/auth/google/`
- Callback: `https://sirms.onrender.com/auth/callback/`
- Logout: `https://sirms.onrender.com/auth/logout/`

**Local Development URLs:**
- Login: `http://localhost:8000/auth/google/`
- Callback: `http://localhost:8000/auth/callback/`
- Logout: `http://localhost:8000/auth/logout/`
