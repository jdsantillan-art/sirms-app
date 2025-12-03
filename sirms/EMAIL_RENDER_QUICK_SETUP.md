# ⚡ Email Setup - Quick Reference Card

## 🎯 3-Step Setup (5 Minutes)

### 1️⃣ Get Gmail App Password
```
1. Go to: https://myaccount.google.com/security
2. Enable "2-Step Verification"
3. Click "App passwords"
4. Generate password for "Mail"
5. Copy 16-character code (remove spaces)
```

### 2️⃣ Add to Render Environment
```
Go to: Render Dashboard → Your Service → Environment

Add these 7 variables:

EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-gmail@gmail.com
EMAIL_HOST_PASSWORD=your-16-char-password
DEFAULT_FROM_EMAIL=DMLMHS SIRMS <your-gmail@gmail.com>
SITE_URL=https://your-app.onrender.com
```

### 3️⃣ Test
```
1. Wait for Render to redeploy (2-5 min)
2. Create incident report in SIRMS
3. Check email inbox
4. Done! ✅
```

---

## 📋 Copy-Paste Template

Replace the values and paste into Render:

```
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=jdsantillandionson@gmail.com
EMAIL_HOST_PASSWORD=PASTE_YOUR_16_CHAR_PASSWORD_HERE
DEFAULT_FROM_EMAIL=DMLMHS SIRMS <jdsantillandionson@gmail.com>
SITE_URL=https://sirms-dmlmhs.onrender.com
```

---

## 🚨 Common Issues

| Problem | Solution |
|---------|----------|
| Authentication failed | Use App Password, not regular password |
| Emails not arriving | Check Spam folder |
| SMTPAuthenticationError | Enable 2-Step Verification first |
| Deployment fails | Check for typos in variable names |

---

## ✅ Success Checklist

- [ ] 2-Step Verification enabled
- [ ] App Password generated
- [ ] All 7 variables added to Render
- [ ] Render redeployed successfully
- [ ] Test email received
- [ ] Email looks professional

---

## 📊 Limits

- **Free Gmail:** 500 emails/day
- **Google Workspace:** 2,000 emails/day

---

**Need detailed help?** See `DEPLOY_EMAIL_TO_RENDER.md`
