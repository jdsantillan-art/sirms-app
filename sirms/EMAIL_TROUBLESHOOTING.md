# 🔧 Email Notifications Troubleshooting Guide

Quick solutions for common email notification issues.

---

## 🚨 Problem: "Authentication Failed" Error

### Symptoms:
- Render logs show: `SMTPAuthenticationError`
- Emails not sending
- Error: "Username and Password not accepted"

### Solutions:

#### Solution 1: Use App Password (Not Regular Password)
```
❌ Wrong: Using your regular Gmail password
✅ Correct: Using 16-character App Password

Steps:
1. Go to Google Account → Security
2. Enable 2-Step Verification
3. Generate App Password for "Mail"
4. Use that password in EMAIL_HOST_PASSWORD
```

#### Solution 2: Check Email Address
```
Verify EMAIL_HOST_USER matches the Gmail account
Example: jdsantillandionson@gmail.com
```

#### Solution 3: Regenerate App Password
```
1. Delete old App Password in Google Account
2. Generate new one
3. Update EMAIL_HOST_PASSWORD on Render
4. Save and redeploy
```

---

## 🚨 Problem: Emails Not Arriving

### Symptoms:
- No errors in logs
- Notification created successfully
- Email never arrives in inbox

### Solutions:

#### Solution 1: Check Spam Folder
```
1. Open email inbox
2. Check Spam/Junk folder
3. Mark SIRMS emails as "Not Spam"
4. Add sender to contacts
```

#### Solution 2: Verify Email Address
```python
# Run in Render Shell
from incidents.models import CustomUser
user = CustomUser.objects.get(username='test_user')
print(user.email)  # Should show valid email
```

#### Solution 3: Check Gmail Sent Folder
```
1. Log into Gmail account (the one sending emails)
2. Check "Sent" folder
3. If email is there → delivery issue
4. If not there → sending issue
```

#### Solution 4: Verify Environment Variables
```
Render Dashboard → Environment

Check all variables are set:
✅ EMAIL_BACKEND
✅ EMAIL_HOST
✅ EMAIL_PORT
✅ EMAIL_USE_TLS
✅ EMAIL_HOST_USER
✅ EMAIL_HOST_PASSWORD
✅ DEFAULT_FROM_EMAIL
```

---

## 🚨 Problem: "Connection Refused" Error

### Symptoms:
- Error: `Connection refused`
- Error: `[Errno 111] Connection refused`

### Solutions:

#### Solution 1: Check Port Number
```
EMAIL_PORT should be: 587
Not: 465, 25, or other ports
```

#### Solution 2: Verify TLS Setting
```
EMAIL_USE_TLS should be: True
Not: False or missing
```

#### Solution 3: Check Firewall
```
Render should allow outbound SMTP connections
Usually not an issue on Render
```

---

## 🚨 Problem: Emails Going to Spam

### Symptoms:
- Emails arrive but in spam folder
- Users not seeing notifications

### Solutions:

#### Solution 1: Use Professional Email
```
❌ Bad: personal.email123@gmail.com
✅ Good: sirms@dmlmhs.edu.ph
✅ Good: noreply@dmlmhs.edu.ph
```

#### Solution 2: Improve Email Content
```
- Avoid spam trigger words (FREE, URGENT, CLICK HERE)
- Use professional language
- Include unsubscribe option
- Add school contact information
```

#### Solution 3: Use Email Service Provider
```
Instead of Gmail, use:
- SendGrid (100 emails/day free)
- Mailgun (5,000 emails/month free)
- Amazon SES (62,000 emails/month free)
```

#### Solution 4: Add SPF Records
```
If using custom domain (dmlmhs.edu.ph):
1. Add SPF record to DNS
2. Add DKIM record
3. Verify domain with email provider
```

---

## 🚨 Problem: "Quota Exceeded" Error

### Symptoms:
- Error: `Daily sending quota exceeded`
- Emails stop sending after many notifications

### Solutions:

#### Solution 1: Check Gmail Limits
```
Free Gmail: 500 emails/day
Google Workspace: 2,000 emails/day

Wait 24 hours for quota to reset
```

#### Solution 2: Upgrade to Google Workspace
```
Cost: ~$6/user/month
Benefit: 2,000 emails/day
Better deliverability
```

#### Solution 3: Use Email Service
```
SendGrid Free: 100 emails/day
SendGrid Paid: 40,000+ emails/month

Mailgun Free: 5,000 emails/month
Mailgun Paid: Custom limits
```

---

## 🚨 Problem: Deployment Fails After Adding Variables

### Symptoms:
- Render deployment fails
- Build errors
- Service won't start

### Solutions:

#### Solution 1: Check Variable Names
```
❌ Wrong: email_backend
✅ Correct: EMAIL_BACKEND

All variables should be UPPERCASE
```

#### Solution 2: Remove Quotes
```
❌ Wrong: "django.core.mail.backends.smtp.EmailBackend"
✅ Correct: django.core.mail.backends.smtp.EmailBackend

Render adds quotes automatically
```

#### Solution 3: Check for Typos
```
Common typos:
- EMAIL_BACKEND (not EMAIL_BACK_END)
- EMAIL_HOST_USER (not EMAIL_HOST_USERNAME)
- DEFAULT_FROM_EMAIL (not DEFAULT_EMAIL_FROM)
```

---

## 🚨 Problem: Email Tracking Not Working

### Symptoms:
- Emails sending but `email_sent` always False
- No `email_sent_at` timestamp

### Solutions:

#### Solution 1: Run Migration
```bash
# In Render Shell
python manage.py migrate
```

#### Solution 2: Check Database Fields
```python
# In Render Shell
from incidents.models import Notification
n = Notification.objects.first()
print(hasattr(n, 'email_sent'))  # Should be True
print(hasattr(n, 'email_sent_at'))  # Should be True
```

#### Solution 3: Verify Code Integration
```python
# Check notification_utils.py has email tracking
# Should update email_sent and email_sent_at
```

---

## 🚨 Problem: HTML Email Not Formatting

### Symptoms:
- Email arrives as plain text
- No colors or styling
- Looks unprofessional

### Solutions:

#### Solution 1: Check Email Client
```
Some email clients strip HTML:
- Try different email client
- Check on web version of Gmail
- Test on mobile device
```

#### Solution 2: Verify HTML Message
```python
# email_utils.py should use html_message parameter
send_mail(
    ...
    html_message=html_message,  # This line is important
)
```

---

## 🚨 Problem: Links in Email Don't Work

### Symptoms:
- "View in SIRMS Dashboard" button broken
- Links go to localhost
- 404 errors when clicking links

### Solutions:

#### Solution 1: Set SITE_URL
```
Add to Render Environment:
SITE_URL=https://your-app.onrender.com

Replace with your actual Render URL
```

#### Solution 2: Check URL Format
```
❌ Wrong: http://localhost:8000
❌ Wrong: your-app.onrender.com (missing https://)
✅ Correct: https://your-app.onrender.com
```

---

## 🚨 Problem: Emails Sending Slowly

### Symptoms:
- Long delay before email arrives
- Users complain about slow notifications

### Solutions:

#### Solution 1: Check Gmail Server
```
Gmail usually delivers instantly
If slow, check Gmail status:
https://www.google.com/appsstatus
```

#### Solution 2: Use Async Email Sending
```python
# For future improvement
# Use Celery or Django-Q for background tasks
# Sends emails asynchronously
```

---

## 🔍 Diagnostic Commands

### Check Email Configuration
```bash
# In Render Shell
python verify_email_config.py
```

### Test Email Sending
```python
# In Render Shell
from django.core.mail import send_mail
from django.conf import settings

send_mail(
    'Test Email',
    'This is a test.',
    settings.DEFAULT_FROM_EMAIL,
    ['your-email@gmail.com'],
)
```

### Check Recent Notifications
```python
# In Render Shell
from incidents.models import Notification

# Recent notifications
recent = Notification.objects.order_by('-created_at')[:10]
for n in recent:
    print(f"{n.title} - Email sent: {n.email_sent}")
```

### Check Email Statistics
```python
# In Render Shell
from incidents.models import Notification

total = Notification.objects.count()
sent = Notification.objects.filter(email_sent=True).count()
print(f"Success rate: {sent/total*100:.1f}%")
```

---

## 📊 Monitoring Checklist

Regular checks to ensure email system is healthy:

### Daily Checks
- [ ] Check Render logs for email errors
- [ ] Verify recent notifications sent emails
- [ ] Monitor Gmail sending quota
- [ ] Check user feedback

### Weekly Checks
- [ ] Review email delivery rate
- [ ] Check spam folder reports
- [ ] Verify email formatting on different devices
- [ ] Test all notification types

### Monthly Checks
- [ ] Rotate Gmail App Password
- [ ] Review email content and improve
- [ ] Check for new email service options
- [ ] Update documentation

---

## 🆘 Emergency Procedures

### If Email System Completely Fails:

1. **Switch to Console Backend (Temporary)**
```
Render Environment:
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend

This disables real emails but keeps system running
```

2. **Check Render Status**
```
https://status.render.com
Verify no Render outages
```

3. **Verify Gmail Account**
```
Log into Gmail directly
Check for security alerts
Verify account not locked
```

4. **Regenerate Credentials**
```
1. Delete old App Password
2. Generate new one
3. Update Render environment
4. Redeploy
```

5. **Contact Support**
```
If all else fails:
- Render Support: https://render.com/support
- Gmail Support: https://support.google.com
```

---

## 📞 Getting Help

### Before Asking for Help:

1. ✅ Run `verify_email_config.py`
2. ✅ Check Render logs
3. ✅ Verify environment variables
4. ✅ Test Gmail credentials manually
5. ✅ Review this troubleshooting guide

### Information to Provide:

- Error message (exact text)
- Render logs (last 50 lines)
- Environment variables (hide password)
- Steps to reproduce
- When it started failing

---

## ✅ Prevention Tips

### Avoid Common Issues:

1. **Use App Passwords**
   - Never use regular Gmail password
   - Regenerate every 3-6 months

2. **Monitor Quotas**
   - Track daily email count
   - Upgrade if approaching limits

3. **Test Regularly**
   - Weekly test emails
   - Verify all notification types

4. **Keep Documentation Updated**
   - Document any changes
   - Update team on issues

5. **Have Backup Plan**
   - Keep console backend as fallback
   - Consider secondary email service

---

**Last Updated:** December 3, 2025  
**Version:** 1.0

🎯 **Most issues are solved by regenerating the App Password!**
