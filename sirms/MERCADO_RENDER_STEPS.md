# 📋 Step-by-Step: Create Ms. Mercado's Account on Render

## ✓ Step 1: Code Deployed (DONE)

The account creation code has been pushed to GitHub and Render is deploying it now.

---

## 🔄 Step 2: Wait for Deployment (IN PROGRESS)

1. Go to https://dashboard.render.com
2. Find your SIRMS service
3. Wait for the status to show **"Live"** (green)
4. This usually takes 2-5 minutes

---

## 🖥️ Step 3: Open Render Shell

1. Click on your SIRMS service name
2. Look for **"Shell"** in the left sidebar
3. Click on "Shell"
4. Wait for the terminal to connect (you'll see a prompt like `~ $`)

---

## ⌨️ Step 4: Run the Command

**Copy this command exactly:**

```bash
python manage.py shell -c "from incidents.models import CustomUser, TeacherAssignment; CustomUser.objects.filter(username='stephanie.mercado').delete(); user = CustomUser.objects.create_user(username='stephanie.mercado', password='Teacher2024!', email='stephanie.mercado@school.edu', first_name='Stephanie', last_name='Mercado', role='teacher', employee_id='TCH-2024-008', grade_level='Grade 8', section='Section 2', is_active=True); TeacherAssignment.objects.get_or_create(teacher_name='Ms. Stephanie Mercado', grade_level='8', section_name='Section 2', track_code='ICT'); print('✓ Account created successfully!')"
```

**Paste it into the Render Shell and press Enter**

---

## ✅ Step 5: Verify Success

You should see output like:
```
✓ Account created successfully!
```

---

## 🔐 Step 6: Test Login

1. Go to your Render app URL (e.g., https://sirms-app.onrender.com)
2. Click "Login"
3. Enter:
   - **Username:** stephanie.mercado
   - **Password:** Teacher2024!
4. Click "Login"

---

## 🎉 Success!

Ms. Mercado can now:
- ✓ Login to the production site
- ✓ View Grade 8 Section 2 student reports
- ✓ Receive notifications from Guidance, DO, and ESP Teacher
- ✓ Track case progress in real-time

---

## 📝 Important Notes

- **Username is case-sensitive:** use all lowercase `stephanie.mercado`
- **Password is case-sensitive:** `Teacher2024!` with capital T's and !
- **This creates the account in production** (Render's PostgreSQL database)
- **Local database is separate** - local and production accounts are different

---

## 🆘 Need Help?

**If the command doesn't work:**
1. Make sure deployment finished (green "Live" status)
2. Try refreshing the Shell page
3. Copy the command again (don't type it manually)
4. Make sure you're in the correct service

**If login doesn't work:**
1. Clear browser cache
2. Try incognito/private mode
3. Double-check you're on the Render URL (not localhost)
4. Verify username and password exactly as shown

---

## 📌 Quick Reference

| Item | Value |
|------|-------|
| Render Dashboard | https://dashboard.render.com |
| Username | stephanie.mercado |
| Password | Teacher2024! |
| Role | Teacher |
| Assignment | Grade 8 Section 2 (ICT) |
| Employee ID | TCH-2024-008 |

---

**Ready? Go to Render Dashboard now!** 🚀
