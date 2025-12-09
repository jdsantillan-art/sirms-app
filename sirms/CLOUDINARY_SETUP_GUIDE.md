# Cloudinary Setup - Step by Step Guide

## Step 1: Sign Up for Cloudinary

1. **Go to Cloudinary website**
   - Open your browser
   - Visit: https://cloudinary.com/users/register/free

2. **Fill in the registration form**
   - Email: Use your email address
   - Password: Create a strong password
   - Click "Sign up for free"

3. **Verify your email**
   - Check your email inbox
   - Click the verification link from Cloudinary
   - This activates your account

## Step 2: Get Your Credentials

### Option A: From Dashboard (Easiest)

1. **Login to Cloudinary**
   - Go to: https://cloudinary.com/users/login
   - Enter your email and password
   - Click "Log in"

2. **View Dashboard**
   - You'll be taken to the Dashboard automatically
   - Look for the "Account Details" section (usually at the top)

3. **Copy Your Credentials**
   You'll see a box with these details:
   
   ```
   Cloud name: dxxxxxxxx
   API Key: 123456789012345
   API Secret: aBcDeFgHiJkLmNoPqRsTuVwXyZ
   ```

   **Copy these three values:**
   - Cloud name (example: `dxxxxxxxx`)
   - API Key (example: `123456789012345`)
   - API Secret (example: `aBcDeFgHiJkLmNoPqRsTuVwXyZ`)

### Option B: From Settings

1. **Click on Settings** (gear icon in top right)
2. **Go to "Account" tab**
3. **Scroll to "Account Details"**
4. **Copy the three credentials** as shown above

## Step 3: What Each Credential Means

- **Cloud Name**: Your unique Cloudinary account identifier
  - Format: Usually starts with 'd' followed by random characters
  - Example: `dab12cd34`

- **API Key**: Public key for API access
  - Format: 15-digit number
  - Example: `123456789012345`

- **API Secret**: Private key for API access (keep this secret!)
  - Format: Random alphanumeric string
  - Example: `aBcDeFgHiJkLmNoPqRsTuVwXyZ`

## Step 4: Save Your Credentials Securely

**IMPORTANT**: Keep these credentials safe!

1. **Copy to a text file** (temporarily)
2. **DO NOT commit them to Git**
3. **DO NOT share them publicly**

Example format to save:
```
CLOUDINARY_CLOUD_NAME=dab12cd34
CLOUDINARY_API_KEY=123456789012345
CLOUDINARY_API_SECRET=aBcDeFgHiJkLmNoPqRsTuVwXyZ
```

## Step 5: Verify Your Free Tier Limits

On the Dashboard, you'll see:
- **Storage**: 25 GB
- **Bandwidth**: 25 GB/month
- **Transformations**: 25,000/month

This is more than enough for your SIRMS application!

## Visual Guide

```
┌─────────────────────────────────────────┐
│  Cloudinary Dashboard                   │
├─────────────────────────────────────────┤
│                                         │
│  Account Details                        │
│  ┌───────────────────────────────────┐ │
│  │ Cloud name: dab12cd34             │ │
│  │ API Key: 123456789012345          │ │
│  │ API Secret: aBcDeFgHiJkLmNoPqRs   │ │
│  │ [Show/Hide button]                │ │
│  └───────────────────────────────────┘ │
│                                         │
│  Usage This Month                       │
│  Storage: 0 / 25 GB                    │
│  Bandwidth: 0 / 25 GB                  │
│                                         │
└─────────────────────────────────────────┘
```

## Troubleshooting

### Can't find credentials?
- Make sure you're logged in
- Look for "Account Details" or "API Keys" section
- Try clicking the gear icon (Settings) → Account tab

### API Secret is hidden?
- Click the "Show" or "Reveal" button next to it
- You may need to re-enter your password

### Need to regenerate credentials?
- Go to Settings → Security
- You can regenerate API Secret if needed
- **Warning**: This will break existing integrations

## Next Steps

Once you have your credentials:
1. ✅ Copy all three values
2. ✅ Keep them safe
3. ✅ Provide them to configure SIRMS
4. ✅ I'll set up the integration
5. ✅ Deploy to Render

---

**Ready?** Once you have these three credentials, let me know and I'll configure everything!
