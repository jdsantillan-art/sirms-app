# Complete OAuth Fix - December 9, 2025

## Changes Made

### 1. Fixed Static File Issue
- Inlined auto_capitalize.js directly in base.html
- OAuth templates are now standalone (don't depend on base.html)
- No more FileNotFoundError for static files

### 2. Added Error Handling
- Wrapped callback processing in try-catch
- Added debug logging throughout
- Better error messages

### 3. Added Test Endpoints
- `/auth/test/` - Test if OAuth routing works
- `/auth/callback` - Handle callback without trailing slash
- Both callback URLs now work

### 4. Improved URL Routing
- Added callback URL without trailing slash
- More flexible URL matching

## How to Fix Your Deployment

### Step 1: Set Environment Variables in Render

Go to Render Dashboard → sirms → Environment and add:

```
GOOGLE_OAUTH_CLIENT_ID=your_client_id_here
GOOGLE_OAUTH_CLIENT_SECRET=your_client_secret_here
SITE_URL=https://sirms.onrender.com
```

**Where to get these:**
1. Go to https://console.cloud.google.com/
2. Select your project
3. APIs & Services → Credentials
4. Copy Client ID and Client Secret

### Step 2: Update Google Cloud Console

1. Go to https://console.cloud.google.com/
2. APIs & Services → Credentials
3. Click your OAuth 2.0 Client ID
4. Under "Authorized redirect URIs", add BOTH:
   ```
   https://sirms.onrender.com/auth/callback/
   https://sirms.onrender.com/auth/callback
   ```
5. Save and wait 5-10 minutes

### Step 3: Test the Deployment

1. **Test OAuth routing:**
   Visit: `https://sirms.onrender.com/auth/test/`
   
   Should show:
   ```json
   {
     "status": "ok",
     "message": "OAuth routing is working",
     "client_id_set": true,
     "client_secret_set": true,
     "redirect_uri": "https://sirms.onrender.com/auth/callback/",
     "site_url": "https://sirms.onrender.com"
   }
   ```

2. **Test health check:**
   Visit: `https://sirms.onrender.com/health/`
   
   Should show: `{"status": "ok"}`

3. **Test login:**
   Visit: `https://sirms.onrender.com/auth/google/`
   
   Should redirect to Google login

## Troubleshooting

### Issue: OAuth test shows client_id_set: false

**Fix:** Environment variables not set in Render
- Go to Render Dashboard → Environment
- Add GOOGLE_OAUTH_CLIENT_ID and GOOGLE_OAUTH_CLIENT_SECRET
- Wait for automatic redeploy

### Issue: Still getting 404 on callback

**Possible causes:**
1. Deployment not finished - check Render dashboard
2. Build failed - check Render logs
3. Static files issue - should be fixed now

**Fix:**
- Check Render logs for errors
- Ensure deployment shows "Live" status
- Try manual redeploy in Render dashboard

### Issue: redirect_uri_mismatch

**Fix:** Add both URLs to Google Cloud Console:
- `https://sirms.onrender.com/auth/callback/` (with slash)
- `https://sirms.onrender.com/auth/callback` (without slash)

### Issue: Invalid token or authentication failed

**Fix:** 
- Verify Client ID and Secret match Google Cloud Console
- Check that you're using the correct Google account
- Ensure email format matches DMLMHS requirements

## Testing Checklist

- [ ] Environment variables set in Render
- [ ] Redirect URIs added to Google Cloud Console
- [ ] Deployment shows "Live" in Render
- [ ] `/health/` returns `{"status": "ok"}`
- [ ] `/auth/test/` shows OAuth config
- [ ] `/auth/google/` redirects to Google
- [ ] Can complete login flow

## Email Format Requirements

Your Google email must match this format:

- **Student:** `lastname.dmlmhsstudent@gmail.com`
- **Teacher:** `lastnameFMdmlmhs.teacher@gmail.com` (F=first initial, M=middle initial)
- **Guidance:** `lastname.dmlmhsguidance@gmail.com`
- **DO:** `lastname.dmlmhsdo@gmail.com`
- **Principal:** `lastname.dmlmhsprincipal@gmail.com`
- **ESP Teacher:** `lastname.dmlmhsesp_teacher@gmail.com`

## Quick Commands

### Check Render logs:
```bash
# In Render dashboard, click "Logs" tab
```

### Test locally:
```bash
set GOOGLE_OAUTH_CLIENT_ID=your_id
set GOOGLE_OAUTH_CLIENT_SECRET=your_secret
set SITE_URL=http://localhost:8000
python manage.py runserver
```

Then visit: `http://localhost:8000/auth/test/`

## Files Changed

1. `templates/base.html` - Inlined auto_capitalize script
2. `incidents/oauth_views.py` - Added error handling and test endpoint
3. `incidents/urls.py` - Added test endpoint and flexible callback URL
4. `templates/oauth/google_callback_loading.html` - New loading template

## Next Steps

1. Deploy these changes to Render (push to GitHub)
2. Set environment variables in Render
3. Update Google Cloud Console redirect URIs
4. Wait 5-10 minutes
5. Test at `/auth/test/` first
6. Then try logging in at `/auth/google/`

## Support

If still not working after following all steps:
1. Check Render logs for Python errors
2. Run `/auth/test/` and share the output
3. Verify Google Cloud Console project is correct
4. Try in incognito/private browsing mode
