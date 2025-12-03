# 📧 Email Deployment Checklist

Use this checklist to deploy email notifications to Render step by step.

---

## 🎯 Pre-Deployment

### Gmail Account Setup
- [ ] Have Gmail account ready (or school Google Workspace)
- [ ] Account has 2-Step Verification enabled
- [ ] Can access Google Account Security settings

---

## 📝 Step 1: Generate Gmail App Password

- [ ] Go to https://myaccount.google.com/security
- [ ] Click "2-Step Verification"
- [ ] Scroll to "App passwords"
- [ ] Click "App passwords"
- [ ] Select app: "Mail"
- [ ] Select device: "Other (Custom name)"
- [ ] Enter name: "SIRMS Render"
- [ ] Click "Generate"
- [ ] Copy 16-character password
- [ ] Remove spaces from password
- [ ] Save password securely (you'll need it next)

**Your App Password:** `________________` (write it down temporarily)

---

## 🔧 Step 2: Configure Render

### Access Render Dashboard
- [ ] Go to https://dashboard.render.com
- [ ] Log in to your account
- [ ] Select your SIRMS service
- [ ] Click "Environment" in left sidebar

### Add Environment Variables

Add these 7 variables one by one:

#### Variable 1: EMAIL_BACKEND
- [ ] Click "Add Environment Variable"
- [ ] Key: `EMAIL_BACKEND`
- [ ] Value: `django.core.mail.backends.smtp.EmailBackend`
- [ ] Click "Add"

#### Variable 2: EMAIL_HOST
- [ ] Click "Add Environment Variable"
- [ ] Key: `EMAIL_HOST`
- [ ] Value: `smtp.gmail.com`
- [ ] Click "Add"

#### Variable 3: EMAIL_PORT
- [ ] Click "Add Environment Variable"
- [ ] Key: `EMAIL_PORT`
- [ ] Value: `587`
- [ ] Click "Add"

#### Variable 4: EMAIL_USE_TLS
- [ ] Click "Add Environment Variable"
- [ ] Key: `EMAIL_USE_TLS`
- [ ] Value: `True`
- [ ] Click "Add"

#### Variable 5: EMAIL_HOST_USER
- [ ] Click "Add Environment Variable"
- [ ] Key: `EMAIL_HOST_USER`
- [ ] Value: `your-gmail@gmail.com` (replace with your email)
- [ ] Click "Add"

#### Variable 6: EMAIL_HOST_PASSWORD
- [ ] Click "Add Environment Variable"
- [ ] Key: `EMAIL_HOST_PASSWORD`
- [ ] Value: (paste your 16-character app password)
- [ ] Click "Add"

#### Variable 7: DEFAULT_FROM_EMAIL
- [ ] Click "Add Environment Variable"
- [ ] Key: `DEFAULT_FROM_EMAIL`
- [ ] Value: `DMLMHS SIRMS <your-gmail@gmail.com>`
- [ ] Click "Add"

#### Variable 8: SITE_URL (if not already set)
- [ ] Click "Add Environment Variable"
- [ ] Key: `SITE_URL`
- [ ] Value: `https://your-app.onrender.com` (your actual URL)
- [ ] Click "Add"

### Save and Deploy
- [ ] Click "Save Changes" button
- [ ] Render starts automatic redeployment
- [ ] Wait for deployment to complete (2-5 minutes)

---

## ⏳ Step 3: Monitor Deployment

### Watch Deployment Progress
- [ ] Go to "Logs" tab
- [ ] Watch for "Building..."
- [ ] Watch for "Build successful"
- [ ] Watch for "Starting service..."
- [ ] Watch for "Deploy live"
- [ ] No error messages appear

### Verify Deployment
- [ ] Deployment status shows "Live"
- [ ] Service is running (green indicator)
- [ ] No errors in recent logs

---

## ✅ Step 4: Test Email Configuration

### Run Verification Script
- [ ] Go to Render Dashboard → Shell tab
- [ ] Run: `python verify_email_config.py`
- [ ] All checks pass with ✅
- [ ] Test email sent successfully
- [ ] No error messages

### Check Email Inbox
- [ ] Open email inbox (the one you configured)
- [ ] Look for email from "DMLMHS SIRMS"
- [ ] Subject: "[SIRMS] Email Configuration Test"
- [ ] Email received within 1-2 minutes
- [ ] Email has professional HTML formatting
- [ ] Email displays correctly

### Test Real Notification
- [ ] Log into SIRMS on Render
- [ ] Create a test incident report
- [ ] Submit the report
- [ ] Check reporter's email inbox
- [ ] Notification email received
- [ ] Email contains case details
- [ ] "View in SIRMS Dashboard" button works

---

## 🎉 Step 5: Final Verification

### Functionality Tests
- [ ] Submit incident report → Email sent
- [ ] Confirm involved party → Email sent
- [ ] Schedule counseling → Email sent
- [ ] Complete session → Email sent
- [ ] All notification types working

### Email Quality Checks
- [ ] Professional HTML formatting
- [ ] DMLMHS branding visible
- [ ] Case details included
- [ ] Links work correctly
- [ ] Not going to spam folder

### Database Tracking
- [ ] Notifications have `email_sent=True`
- [ ] `email_sent_at` timestamp recorded
- [ ] Can query email statistics

---

## 📊 Step 6: Monitor Performance

### First 24 Hours
- [ ] Monitor Render logs for email errors
- [ ] Check Gmail sending quota (500/day limit)
- [ ] Verify users receiving emails
- [ ] No complaints about missing emails
- [ ] Email delivery rate > 95%

### User Feedback
- [ ] Ask users if they received emails
- [ ] Verify email formatting on different devices
- [ ] Check if emails are in spam
- [ ] Gather feedback on email content

---

## 🔐 Step 7: Security & Cleanup

### Security
- [ ] App password not committed to Git
- [ ] Environment variables secure on Render
- [ ] 2-Step Verification still enabled
- [ ] Regular password rotation scheduled

### Documentation
- [ ] Team knows email is enabled
- [ ] Support staff trained on email features
- [ ] Troubleshooting guide accessible
- [ ] Monitoring process documented

### Cleanup
- [ ] Delete temporary password notes
- [ ] Remove test notifications
- [ ] Clear test emails from inbox

---

## 🚨 Troubleshooting Checklist

If emails not working, check:

- [ ] All 7 environment variables set correctly
- [ ] No typos in variable names
- [ ] App password copied correctly (no spaces)
- [ ] Using App Password (not regular password)
- [ ] 2-Step Verification enabled on Gmail
- [ ] Render deployment completed successfully
- [ ] No errors in Render logs
- [ ] Gmail account not locked/suspended
- [ ] Not exceeding Gmail sending limits (500/day)
- [ ] Check spam folder

---

## 📈 Success Metrics

Your deployment is successful when:

- ✅ All checklist items completed
- ✅ Test email received in inbox
- ✅ Real notifications trigger emails
- ✅ No errors in Render logs
- ✅ Users receiving emails consistently
- ✅ Email delivery rate > 95%
- ✅ Professional email formatting
- ✅ Links in emails work

---

## 📞 Support Resources

**If you need help:**

1. **Check Render Logs:**
   - Dashboard → Logs tab
   - Look for email-related errors

2. **Run Verification Script:**
   - Dashboard → Shell tab
   - `python verify_email_config.py`

3. **Test Gmail Credentials:**
   - Try logging into Gmail directly
   - Verify App Password is valid

4. **Review Documentation:**
   - `DEPLOY_EMAIL_TO_RENDER.md` (detailed guide)
   - `EMAIL_RENDER_QUICK_SETUP.md` (quick reference)
   - `EMAIL_NOTIFICATIONS_SETUP.md` (feature guide)

---

## ✅ Completion

**Date Completed:** _______________

**Deployed By:** _______________

**Gmail Account Used:** _______________

**Render Service:** _______________

**Test Email Received:** ☐ Yes  ☐ No

**Production Ready:** ☐ Yes  ☐ No

---

**Notes:**
_____________________________________________
_____________________________________________
_____________________________________________

---

🎉 **Congratulations! Email notifications are now live!**

**Created:** December 3, 2025  
**Version:** 1.0
