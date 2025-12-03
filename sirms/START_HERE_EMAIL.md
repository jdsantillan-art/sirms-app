# 📧 START HERE - Email Deployment

## 🎯 Your Mission
Enable real email notifications on Render (5 minutes)

---

## 📍 You Are Here
```
✅ Email code implemented
✅ Database migrated
✅ Tests passing
⏳ Need to configure Gmail on Render ← YOU ARE HERE
```

---

## ⚡ 3 Steps to Success

### 1️⃣ Get Gmail App Password (2 min)
```
https://myaccount.google.com/security
→ 2-Step Verification
→ App passwords
→ Generate for "Mail"
→ Copy 16-character code
```

### 2️⃣ Configure Render (3 min)
```
https://dashboard.render.com
→ Your SIRMS service
→ Environment
→ Add 7 variables (see below)
→ Save Changes
```

### 3️⃣ Test (2 min)
```
Wait for redeploy
→ Create test report
→ Check email inbox
→ Done! ✅
```

---

## 📋 Copy-Paste This to Render

```
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-gmail@gmail.com
EMAIL_HOST_PASSWORD=your-16-char-app-password
DEFAULT_FROM_EMAIL=DMLMHS SIRMS <your-gmail@gmail.com>
SITE_URL=https://your-app.onrender.com
```

**Replace:**
- `your-gmail@gmail.com` → Your Gmail
- `your-16-char-app-password` → From Step 1
- `your-app.onrender.com` → Your Render URL

---

## 📚 Need More Help?

| Guide | When to Use | Time |
|-------|-------------|------|
| `EMAIL_RENDER_QUICK_SETUP.md` | Quick reference | 5 min |
| `DEPLOY_EMAIL_TO_RENDER.md` | Detailed instructions | 15 min |
| `EMAIL_DEPLOYMENT_CHECKLIST.md` | Step-by-step checklist | 10 min |
| `EMAIL_TROUBLESHOOTING.md` | Something's wrong | As needed |

---

## ✅ Success Looks Like

- ✅ Render deploys without errors
- ✅ Test email arrives in inbox
- ✅ Professional HTML formatting
- ✅ Users receive notifications

---

## 🚨 Common Issues

| Problem | Solution |
|---------|----------|
| Authentication failed | Use App Password, not regular password |
| Emails not arriving | Check spam folder |
| Deployment fails | Check for typos in variable names |

---

## 🎯 Ready? Pick Your Path:

**Path A: Quick Setup (5 min)**
```
→ Open EMAIL_RENDER_QUICK_SETUP.md
```

**Path B: Detailed Guide (15 min)**
```
→ Open DEPLOY_EMAIL_TO_RENDER.md
```

**Path C: Checklist (10 min)**
```
→ Open EMAIL_DEPLOYMENT_CHECKLIST.md
```

---

🚀 **Let's deploy email notifications!**
