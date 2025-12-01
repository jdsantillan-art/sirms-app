# 🚀 Deploy DO Account to Render - QUICK GUIDE

## ✅ What I Just Did:

Added a **DO Admin account** that will be automatically created on Render:

```
Username: do_admin
Password: do123
Role: Discipline Officer
```

## 🎯 Deploy to Render NOW:

### Option 1: Run the Batch File (Easiest)
```bash
cd sirms
deploy_do_account.bat
```

### Option 2: Manual Commands
Open a **NEW** Command Prompt (not the Python shell) and run:
```bash
cd sirms
git add -A
git commit -m "Add DO admin account for Render"
git push origin main
```

## ⏳ After Pushing:

1. **Wait 5-10 minutes** for Render to deploy
2. **Go to your Render URL** (e.g., `https://sirms.onrender.com`)
3. **Login with:**
   - Username: `do_admin`
   - Password: `do123`
4. **You're in!** 🎉

## 📋 All DO Accounts Available:

| Username | Password | Name |
|----------|----------|------|
| do_admin | do123 | Discipline Officer |
| do1 | do123 | Ana Garcia |

Both accounts have full DO access!

## 🔍 Check Deployment Status:

Go to your Render dashboard and watch:
- ✅ Build phase (2-3 min)
- ✅ Deploy phase (1-2 min)
- ✅ Live! (Ready to login)

---

**Next Step:** Close the Python shell, open a new Command Prompt, and run `deploy_do_account.bat`
