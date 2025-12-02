# 📧 Email Notifications Setup Guide

## Overview

The SIRMS system now sends email notifications in addition to web-based notifications. Every time a user receives a notification in the system, they also receive an email.

---

## Features

✅ **Automatic Email Sending** - Every web notification triggers an email  
✅ **Professional HTML Emails** - Beautiful, branded email templates  
✅ **Email Tracking** - Track which emails were sent successfully  
✅ **Fail-Safe** - Email failures don't break the application  
✅ **Configurable** - Easy to configure different email providers

---

## Setup Instructions

### 1. Add Email Fields to Database

Run the migration to add email tracking fields:

```bash
cd sirms
python add_email_notification_fields.py
python manage.py migrate
```

### 2. Configure Email Settings

#### Option A: Gmail SMTP (Recommended for Production)

1. **Create App Password:**
   - Go to Google Account → Security
   - Enable 2-Step Verification
   - Generate App Password for "Mail"

2. **Set Environment Variables on Render:**
   ```
   EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-app-password
   DEFAULT_FROM_EMAIL=DMLMHS SIRMS <your-email@gmail.com>
   SITE_URL=https://your-app.onrender.com
   ```

#### Option B: Console Backend (Development/Testing)

For local testing, emails will print to console:
```
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

#### Option C: Other SMTP Providers

**SendGrid:**
```
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=your-sendgrid-api-key
```

**Mailgun:**
```
EMAIL_HOST=smtp.mailgun.org
EMAIL_PORT=587
EMAIL_HOST_USER=your-mailgun-username
EMAIL_HOST_PASSWORD=your-mailgun-password
```

---

## Email Template

### HTML Email Features:
- **Professional Header** - DMLMHS SIRMS branding
- **Styled Content** - Clean, readable layout
- **Report Details** - Case ID, status, date
- **Action Button** - Direct link to dashboard
- **Footer** - School information

### Email Structure:
```
┌─────────────────────────────────┐
│  🔔 DMLMHS SIRMS Notification   │ ← Header
├─────────────────────────────────┤
│  Hello, [User Name]!            │
│                                 │
│  ┌───────────────────────────┐ │
│  │ [Notification Title]      │ │ ← Message Box
│  │ [Notification Message]    │ │
│  └───────────────────────────┘ │
│                                 │
│  📋 Report Details:             │ ← Report Info
│  Case ID: SIRMS-2024-001        │
│  Status: Under Review           │
│  Date: December 02, 2025        │
│                                 │
│  [View in SIRMS Dashboard]      │ ← Action Button
│                                 │
│  This is an automated...        │
├─────────────────────────────────┤
│  DMLMHS SIRMS © 2025            │ ← Footer
└─────────────────────────────────┘
```

---

## How It Works

### 1. Notification Created
```python
notification = Notification.objects.create(
    user=user,
    title="New Incident Report",
    message="A new report requires your attention",
    report=report
)
```

### 2. Email Automatically Sent
```python
# System automatically calls:
send_notification_email(user, title, message, report)
```

### 3. Email Tracked
```python
notification.email_sent = True
notification.email_sent_at = timezone.now()
notification.save()
```

---

## Notification Types That Send Emails

All notification types send emails:

1. **Report Submitted** - New incident report created
2. **Party Confirmed** - Involved party confirmed by DO
3. **DO Classified** - Case classified by Discipline Officer
4. **Guidance Evaluation** - Case evaluated by Guidance
5. **VRF Assigned** - Student assigned to VRF program
6. **Counseling Scheduled** - Counseling session scheduled
7. **Session Completed** - Counseling session completed
8. **Status Update** - General status updates

---

## Testing Email Notifications

### Local Testing (Console Backend):

1. Set in `.env` or environment:
   ```
   EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
   ```

2. Create a test notification:
   ```python
   python manage.py shell
   
   from incidents.models import CustomUser, Notification
   user = CustomUser.objects.first()
   
   Notification.objects.create(
       user=user,
       title="Test Notification",
       message="This is a test email notification"
   )
   ```

3. Check console output for email content

### Production Testing (Gmail):

1. Configure Gmail SMTP (see above)
2. Create a test report or notification
3. Check recipient's email inbox
4. Verify email formatting and links

---

## Email Content Examples

### Example 1: New Report Notification
```
Subject: [SIRMS] New Incident Report - SIRMS-2024-001

Hello, Juan Dela Cruz!

New Incident Report - SIRMS-2024-001

A new incident report requires fact-checking. 
Case ID: SIRMS-2024-001

Report Details:
Case ID: SIRMS-2024-001
Status: Pending
Date: December 02, 2025

[View in SIRMS Dashboard]
```

### Example 2: Counseling Scheduled
```
Subject: [SIRMS] Counseling Scheduled - SIRMS-2024-001

Hello, Maria Santos!

Counseling Scheduled - SIRMS-2024-001

Your counseling session has been scheduled for 
December 05, 2025 at 2:00 PM.

Report Details:
Case ID: SIRMS-2024-001
Status: Under Review
Date: December 02, 2025

[View in SIRMS Dashboard]
```

---

## Troubleshooting

### Issue: Emails Not Sending

**Check:**
1. EMAIL_BACKEND is set to SMTP backend
2. EMAIL_HOST_USER and EMAIL_HOST_PASSWORD are correct
3. Gmail App Password is generated (not regular password)
4. Port 587 is not blocked by firewall

**Solution:**
```bash
# Test email configuration
python manage.py shell

from django.core.mail import send_mail
send_mail(
    'Test Email',
    'This is a test.',
    'from@example.com',
    ['to@example.com'],
)
```

### Issue: Emails Go to Spam

**Solutions:**
- Use verified domain email
- Add SPF and DKIM records
- Use professional email service (SendGrid, Mailgun)
- Avoid spam trigger words

### Issue: Email Tracking Not Working

**Check:**
1. Migration applied: `python manage.py migrate`
2. Fields exist: `email_sent`, `email_sent_at`
3. Check notification object: `notification.email_sent`

---

## Security Best Practices

⚠️ **Never commit email credentials to Git**  
⚠️ **Use environment variables for sensitive data**  
⚠️ **Use App Passwords, not regular passwords**  
⚠️ **Enable 2FA on email account**  
⚠️ **Rotate credentials regularly**  
⚠️ **Monitor email sending limits**

---

## Email Sending Limits

### Gmail:
- Free: 500 emails/day
- Google Workspace: 2,000 emails/day

### SendGrid:
- Free: 100 emails/day
- Paid: 40,000+ emails/month

### Mailgun:
- Free: 5,000 emails/month
- Paid: Custom limits

---

## Monitoring

### Check Email Status:
```python
# In Django shell
from incidents.models import Notification

# Total notifications
total = Notification.objects.count()

# Emails sent successfully
sent = Notification.objects.filter(email_sent=True).count()

# Success rate
print(f"Email success rate: {sent/total*100:.1f}%")
```

### View Recent Email Notifications:
```python
recent = Notification.objects.filter(
    email_sent=True
).order_by('-email_sent_at')[:10]

for n in recent:
    print(f"{n.user.email} - {n.title} - {n.email_sent_at}")
```

---

## Production Deployment

### On Render:

1. **Add Environment Variables:**
   - Go to Dashboard → Your Service → Environment
   - Add all EMAIL_* variables
   - Save changes

2. **Redeploy:**
   - Render will automatically redeploy
   - Or manually trigger: "Manual Deploy" → "Deploy latest commit"

3. **Run Migration:**
   - Go to Shell tab
   - Run: `python manage.py migrate`

4. **Test:**
   - Create a test notification
   - Check email inbox

---

## Benefits

✅ **Instant Notifications** - Users notified immediately via email  
✅ **No Login Required** - Read notifications without logging in  
✅ **Mobile Friendly** - Emails work on all devices  
✅ **Audit Trail** - Track all email notifications  
✅ **Professional** - Branded, professional appearance  
✅ **Reliable** - Fail-safe design doesn't break app

---

**Created:** December 2, 2025  
**Status:** ✅ Ready for deployment  
**Next Step:** Configure email settings and run migration
