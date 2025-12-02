# 🚀 Deploy Fixes to Render - Manual Steps

## ⚠️ Important: Close Any Running Python Processes First!

If you have a migration prompt stuck, press **Ctrl+C** to cancel it, then close the terminal and open a new one.

---

## 📦 What's Being Deployed:

1. ✅ **Fixed indentation error** in `incidents/views.py` (line 1556)
2. ✅ **Fixed all reports template** - removed truncatewords from section name
3. ✅ **Added behavior concerns schedule** - new view for DO appointments
4. ✅ **Updated URLs** - routes to new behavior concerns view

---

## 🔧 Deployment Steps:

### Step 1: Open Fresh Terminal
```bash
# Close any existing terminals
# Open new Command Prompt or PowerShell
cd path\to\sirms
```

### Step 2: Check Git Status
```bash
git status
```

### Step 3: Add All Changes
```bash
git add .
```

### Step 4: Commit Changes
```bash
git commit -m "Fix: Behavior concerns schedule + indentation error + template fixes"
```

### Step 5: Push to GitHub
```bash
git push origin main
```

### Step 6: Monitor Render
- Go to: https://dashboard.render.com
- Watch the build logs
- Wait for deployment to complete (5-10 minutes)

---

## 🧪 After Deployment - Test These:

### Test 1: Behavior Concerns Schedule
1. Login as DO: `do_admin` / `do123`
2. Go to Behavior Concerns
3. Click calendar icon on any case
4. Fill in appointment details
5. Submit
6. ✅ Should see success message
7. ✅ Check DO Schedule sidebar - appointment should appear

### Test 2: All Reports Display
1. Go to All Reports
2. Check Grade/Section column
3. ✅ Should show full section name (e.g., "G7 - Rizal")
4. ✅ No truncation

### Test 3: General Functionality
1. Try creating a new incident report
2. ✅ Should work without errors
3. Check notifications
4. ✅ Should be sent correctly

---

## 📝 Files Changed:

- `incidents/views.py` - Fixed indentation error
- `templates/all_reports.html` - Fixed section name display
- `incidents/behavior_concerns_views.py` - NEW file for schedule functionality
- `incidents/urls.py` - Updated to use new view

---

## ✅ Expected Results:

After deployment:
- ✅ No more 500 errors on behavior concerns schedule
- ✅ DO can schedule appointments successfully
- ✅ Students and advisers get notifications
- ✅ Appointments appear in DO Schedule sidebar
- ✅ All reports show full section names
- ✅ No indentation errors in views.py

---

## 🆘 If Deployment Fails:

Check Render logs for errors. Common issues:
- **Migration errors**: Run `python manage.py migrate` in Render shell
- **Import errors**: Check if all files are committed
- **Syntax errors**: Run `python manage.py check` locally first

---

## 📞 Quick Commands Reference:

```bash
# Check what's changed
git status

# Add all changes
git add .

# Commit with message
git commit -m "Your message here"

# Push to GitHub (triggers Render deployment)
git push origin main

# Check for Python errors locally
python manage.py check

# Run migrations locally (if needed)
python manage.py migrate
```

---

**Ready to deploy! Follow the steps above.** 🚀

