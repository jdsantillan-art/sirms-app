# 📧 Deploy Email Notifications to Render - Step by Step

## 🎯 Goal
Enable real Gmail SMTP email sending on your Render deployment so users receive actual emails instead of console output.

---

## ⚡ Quick Setup (5 Minutes)

### Step 1: Get Gmail App Password

1. **Go to Google Account Settings:**
   - Visit: https://myaccount.google.com/security
   - Or search "Google Account Security"

2. **Enable 2-Step Verification** (if not already enabled):
   - Click "2-Step Verification"
   - Follow the setup wizard
   - Verify with your phone

3. **Generate App Password:**
   - Go back to Security page
   - Click "2-Step Verification"
   - Scroll down to "App passwords"
   - Click "App passwords"
   - Select app: "Mail"
   - Select device: "Other (Custom name)"
   - Enter: "SIRMS Render"
   - Click "Generate"
   - **COPY THE 16-CHARACTER PASSWORD** (e.g., `abcd efgh ijkl mnop`)
   - Remove spaces: `abcdefghijklmnop`

### Step 2: Configure Render Environment Variables

1. **Go to Render Dashboard:**
   - Visit: https://dashboard.render.com
   - Select your SIRMS service

2. **Add Environment Variables:**
   - Click "Environment" in left sidebar
   - Click "Add Environment Variable"
   - Add these variables one by one:

```
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-gmail@gmail.com
EMAIL_HOST_PASSWORD=abcdefghijklmnop
DEFAULT_FROM_EMAIL=DMLMHS SIRMS <your-gmail@gmail.com>
SITE_URL=https://your-app.onrender.com
```

**Replace:**
- `your-gmail@gmail.com` → Your actual Gmail address
- `abcdefghijklmnop` → Your 16-character app password (no spaces)
- `your-app.onrender.com` → Your actual Render URL

3. **Save Changes:**
   - Click "Save Changes"
   - Render will automatically redeploy

### Step 3: Wait for Deployment

- Render will redeploy automatically (takes 2-5 minutes)
- Watch the deployment logs
- Wait for "Build successful" and "Deploy live"

### Step 4: Test Email Notifications

1. **Log into your SIRMS app on Render**
2. **Create a test notification:**
   - Submit an incident report, OR
   - Schedule a counseling session, OR
   - Confirm an involved party
3. **Check your email inbox**
4. **Look for email from "DMLMHS SIRMS"**

---

## 📋 Environment Variables Reference

Copy this template and fill in your details:

```bash
# Email Configuration for Render
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=jdsantillandionson@gmail.com
EMAIL_HOST_PASSWORD=your-16-char-app-password-here
DEFAULT_FROM_EMAIL=DMLMHS SIRMS <jdsantillandionson@gmail.com>
SITE_URL=https://sirms-dmlmhs.onrender.com
```

---

## 🔍 Verification Checklist

After deployment, verify everything is working:

### ✅ Check 1: Environment Variables Set
```
Go to Render Dashboard → Environment
Verify all 7 EMAIL_* variables are present
```

### ✅ Check 2: Deployment Successful
```
Go to Render Dashboard → Logs
Look for "Build successful"
Look for "Deploy live"
No error messages about email
```

### ✅ Check 3: Create Test Notification
```
1. Log into SIRMS
2. Submit a test incident report
3. Check the reporter's email inbox
4. Email should arrive within 1-2 minutes
```

### ✅ Check 4: Email Content
```
Subject: [SIRMS] New Incident Report - SIRMS-XXXX-XXX
From: DMLMHS SIRMS <your-email@gmail.com>
Contains: Professional HTML formatting
Contains: Case ID and details
Contains: "View in SIRMS Dashboard" button
```

---

## 🚨 Troubleshooting

### Problem: "Authentication failed" error

**Cause:** Wrong email or password

**Solution:**
1. Double-check EMAIL_HOST_USER is correct
2. Verify you're using App Password (not regular password)
3. Regenerate App Password if needed
4. Make sure no spaces in password

### Problem: Emails not arriving

**Cause:** Gmail blocking or wrong configuration

**Solution:**
1. Check Gmail "Sent" folder
2. Check recipient's Spam folder
3. Verify EMAIL_PORT=587 and EMAIL_USE_TLS=True
4. Try sending test email from Gmail directly

### Problem: "SMTPAuthenticationError"

**Cause:** 2-Step Verification not enabled

**Solution:**
1. Enable 2-Step Verification on Google Account
2. Generate new App Password
3. Update EMAIL_HOST_PASSWORD on Render

### Problem: Deployment fails after adding variables

**Cause:** Syntax error in environment variables

**Solution:**
1. Check for typos in variable names
2. Remove quotes around values (Render adds them automatically)
3. Verify no extra spaces

### Problem: Emails go to Spam

**Solutions:**
- Use a verified domain email (not personal Gmail)
- Add SPF records to your domain
- Use professional email service (SendGrid, Mailgun)
- Ask recipients to mark as "Not Spam"

---

## 🔐 Security Best Practices

### ✅ DO:
- Use App Passwords (never regular password)
- Enable 2-Step Verification
- Use environment variables (never hardcode)
- Rotate passwords every 3-6 months
- Monitor email sending activity

### ❌ DON'T:
- Commit passwords to Git
- Share App Passwords
- Use same password for multiple apps
- Disable 2-Step Verification
- Use personal email for production

---

## 📊 Gmail Sending Limits

**Free Gmail Account:**
- 500 emails per day
- 100 recipients per email
- Resets at midnight PST

**Google Workspace:**
- 2,000 emails per day
- 2,000 recipients per email

**If you exceed limits:**
- Emails will be queued
- Account may be temporarily suspended
- Consider upgrading to Google Workspace
- Or use SendGrid/Mailgun

---

## 🎓 Alternative: Use School Email

If your school has Google Workspace:

```bash
EMAIL_HOST_USER=sirms@dmlmhs.edu.ph
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=DMLMHS SIRMS <sirms@dmlmhs.edu.ph>
```

**Benefits:**
- More professional
- Higher sending limits (2,000/day)
- Better deliverability
- School branding

---

## 📈 Monitoring Email Performance

### Check Email Stats in Django Shell:

```python
# Connect to Render Shell
# Dashboard → Shell tab

from incidents.models import Notification

# Total notifications
total = Notification.objects.count()

# Emails sent
sent = Notification.objects.filter(email_sent=True).count()

# Success rate
print(f"Email success rate: {sent/total*100:.1f}%")

# Recent emails
recent = Notification.objects.filter(
    email_sent=True
).order_by('-email_sent_at')[:10]

for n in recent:
    print(f"{n.user.email} - {n.title} - {n.email_sent_at}")
```

---

## 🚀 Next Steps After Deployment

1. **Test thoroughly:**
   - Create various notification types
   - Test with different user roles
   - Verify email formatting

2. **Monitor for 24 hours:**
   - Check for failed emails
   - Monitor Gmail sending quota
   - Review user feedback

3. **Document for team:**
   - Share email notification guide
   - Train staff on email features
   - Set up email monitoring

4. **Consider upgrades:**
   - Google Workspace for higher limits
   - SendGrid for better analytics
   - Custom domain for branding

---

## 📞 Support

**If you need help:**
1. Check Render deployment logs
2. Review Django error logs
3. Test Gmail credentials manually
4. Verify environment variables
5. Check Gmail account status

**Common Issues:**
- Wrong App Password → Regenerate
- 2FA not enabled → Enable it
- Quota exceeded → Wait 24 hours
- Emails in Spam → Whitelist sender

---

## ✅ Success Indicators

You'll know it's working when:

1. ✅ Render deployment completes without errors
2. ✅ Test notification creates email in inbox
3. ✅ Email has professional HTML formatting
4. ✅ Links in email work correctly
5. ✅ No errors in Render logs
6. ✅ Users receive notifications instantly

---

**Created:** December 3, 2025  
**Status:** Ready for deployment  
**Estimated Time:** 5-10 minutes  
**Difficulty:** Easy

🎉 **You're ready to deploy! Follow Step 1 to get started.**
