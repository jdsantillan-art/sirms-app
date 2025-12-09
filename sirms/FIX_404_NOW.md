# Fix 404 Error - Do This Now

## The Issue
You're getting "Not Found" when Google tries to redirect back to your app.

## The Fix (2 Minutes)

### Step 1: Go to Render Dashboard
1. Visit: https://dashboard.render.com/
2. Click on your **sirms** service

### Step 2: Add Environment Variables
1. Click **Environment** in the left sidebar
2. Click **Add Environment Variable**
3. Add these THREE variables:

**Variable 1:**
- Key: `GOOGLE_OAUTH_CLIENT_ID`
- Value: (Get from Google Cloud Console - see below)

**Variable 2:**
- Key: `GOOGLE_OAUTH_CLIENT_SECRET`  
- Value: (Get from Google Cloud Console - see below)

**Variable 3:**
- Key: `SITE_URL`
- Value: `https://sirms.onrender.com`

4. Click **Save Changes**

### Step 3: Get Google OAuth Credentials

1. Go to: https://console.cloud.google.com/
2. Select your SIRMS project
3. Click **APIs & Services** → **Credentials**
4. Find your OAuth 2.0 Client ID
5. Copy the **Client ID** → paste into Render as GOOGLE_OAUTH_CLIENT_ID
6. Copy the **Client secret** → paste into Render as GOOGLE_OAUTH_CLIENT_SECRET

### Step 4: Add Redirect URI in Google Cloud Console

While you're in Google Cloud Console:

1. Click on your OAuth 2.0 Client ID
2. Scroll to **Authorized redirect URIs**
3. Click **+ ADD URI**
4. Enter: `https://sirms.onrender.com/auth/callback/`
5. Click **SAVE**

### Step 5: Wait and Test

1. Wait 2-3 minutes for Render to redeploy
2. Go to: https://sirms.onrender.com/auth/google/
3. Try logging in

## That's It!

The 404 error happens because Render doesn't have your Google OAuth credentials. Once you add them, it will work.

## Need Help Finding Your Google Credentials?

If you don't have a Google Cloud project set up yet:

1. Go to: https://console.cloud.google.com/
2. Create a new project (or select existing)
3. Enable Google+ API
4. Create OAuth 2.0 credentials
5. Set authorized redirect URI to: `https://sirms.onrender.com/auth/callback/`
6. Copy the Client ID and Client Secret to Render

## Verification

After adding the environment variables, check:
- Render shows "Live" status (green checkmark)
- Visit: https://sirms.onrender.com/health/ (should show `{"status": "ok"}`)
- Visit: https://sirms.onrender.com/auth/google/ (should redirect to Google)
