# 🎯 Ms. Mercado's Account - Final Instructions

## The Problem Was...

You created the account **locally** (on your computer), but you need it on **Render** (production server). These are two separate databases!

## ✅ What I Did

1. ✓ Created a Django management command to create the account
2. ✓ Committed the code to git
3. ✓ Pushed to GitHub (which triggers Render deployment)

## 🚀 What YOU Need to Do Now

### Go to Render and Run ONE Command

**That's it! Just one command in Render Shell:**

```bash
python manage.py shell -c "from incidents.models import CustomUser, TeacherAssignment; CustomUser.objects.filter(username='stephanie.mercado').delete(); user = CustomUser.objects.create_user(username='stephanie.mercado', password='Teacher2024!', email='stephanie.mercado@school.edu', first_name='Stephanie', last_name='Mercado', role='teacher', employee_id='TCH-2024-008', grade_level='Grade 8', section='Section 2', is_active=True); TeacherAssignment.objects.get_or_create(teacher_name='Ms. Stephanie Mercado', grade_level='8', section_name='Section 2', track_code='ICT'); print('✓ Account created!')"
```

### How to Run It:

1. **Go to:** https://dashboard.render.com
2. **Click:** Your SIRMS service
3. **Wait:** For deployment to finish (green "Live")
4. **Click:** "Shell" in left sidebar
5. **Paste:** The command above
6. **Press:** Enter

### You'll See:

```
✓ Account created!
```

## 🔑 Login Credentials

**URL:** Your Render app URL  
**Username:** `stephanie.mercado`  
**Password:** `Teacher2024!`

## ⚡ Quick Copy-Paste

Here's the command again for easy copying:

```
python manage.py shell -c "from incidents.models import CustomUser, TeacherAssignment; CustomUser.objects.filter(username='stephanie.mercado').delete(); user = CustomUser.objects.create_user(username='stephanie.mercado', password='Teacher2024!', email='stephanie.mercado@school.edu', first_name='Stephanie', last_name='Mercado', role='teacher', employee_id='TCH-2024-008', grade_level='Grade 8', section='Section 2', is_active=True); TeacherAssignment.objects.get_or_create(teacher_name='Ms. Stephanie Mercado', grade_level='8', section_name='Section 2', track_code='ICT'); print('✓ Account created!')"
```

## 📚 More Details

- See `MERCADO_RENDER_STEPS.md` for detailed step-by-step guide
- See `RUN_ON_RENDER_NOW.md` for troubleshooting

## 💡 Why This Happened

- **Local database** = SQLite file on your computer (db.sqlite3)
- **Render database** = PostgreSQL on Render's servers
- Creating account locally only affects your local database
- To create on Render, you must run commands on Render's server

## ✨ After Account is Created

Ms. Mercado will be able to:
- ✓ Login to production site
- ✓ View all Grade 8 Section 2 student reports
- ✓ Receive notifications from Guidance, DO, ESP Teacher
- ✓ Track case progress
- ✓ Add comments to reports
- ✓ Export reports to Excel

---

**Next Step: Go to Render Dashboard NOW!** 🚀

https://dashboard.render.com
