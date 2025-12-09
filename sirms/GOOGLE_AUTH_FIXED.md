# Google OAuth Fixed - December 9, 2025

## What Was Fixed

### 1. URL Encoding Issue
The redirect URI wasn't being properly URL-encoded when sent to Google. Fixed by using `urllib.parse.urlencode()` instead of manual string concatenation.

**Before:**
```python
query_string = '&'.join([f"{k}={v}" for k, v in params.items()])
```

**After:**
```python
from urllib.parse import urlencode
query_string = urlencode(params)
```

### 2. Added Documentation
Created comprehensive troubleshooting guides:
- `GOOGLE_OAUTH_FIX.md` - Detailed fix guide
- `FIX_GOOGLE_AUTH_NOW.md` - Quick 5-minute fix
- `verify_google_oauth.py` - Configuration verification script

## What You Need to Do

### Step 1: Update Google Cloud Console (REQUIRED)
1. Go to https://console.cloud.google.com/
2. Navigate to **APIs & Services** → **Credentials**
3. Click on your OAuth 2.0 Client ID
4. Under **Authorized redirect URIs**, add:
   ```
   https://sirms.onrender.com/auth/callback/
   http://localhost:8000/auth/callback/
   ```
5. Click **SAVE**
6. Wait 5-10 minutes

### Step 2: Verify Render Environment Variables
Make sure these are set in your Render dashboard:
- `SITE_URL` = `https://sirms.onrender.com`
- `GOOGLE_OAUTH_CLIENT_ID` = (your Google client ID)
- `GOOGLE_OAUTH_CLIENT_SECRET` = (your Google client secret)

### Step 3: Test
1. Wait for Render to finish deploying (check dashboard)
2. Clear browser cache
3. Visit: https://sirms.onrender.com/auth/google/
4. Try logging in with your DMLMHS Google account

## Verification

Run this command to verify your configuration:
```bash
cd sirms
python verify_google_oauth.py
```

## Deployment Status
✓ Code changes pushed to GitHub
✓ Render will auto-deploy (check dashboard)
✓ Documentation created

## Important Notes

1. **Trailing Slash Required:** The redirect URI MUST end with `/`
   - ✓ Correct: `https://sirms.onrender.com/auth/callback/`
   - ✗ Wrong: `https://sirms.onrender.com/auth/callback`

2. **Protocol Matters:**
   - Production (Render): Use `https://`
   - Local development: Use `http://`

3. **Propagation Time:** Google Cloud Console changes take 5-10 minutes to take effect

## Troubleshooting

If still not working:
1. Check Render deployment logs for errors
2. Run `python verify_google_oauth.py` to check configuration
3. Verify the redirect URI in Google Cloud Console matches exactly
4. Clear browser cache and cookies
5. Try in incognito/private browsing mode

## Files Changed
- `incidents/google_auth.py` - Fixed URL encoding
- `GOOGLE_OAUTH_FIX.md` - Detailed documentation
- `FIX_GOOGLE_AUTH_NOW.md` - Quick fix guide
- `verify_google_oauth.py` - Verification script
