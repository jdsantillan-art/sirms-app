# Deploy Ms. Mercado's Account to Render

## The Issue

The account was created in your **local database** (SQLite), but you need it in **Render's production database** (PostgreSQL). These are two separate databases.

## Solution: Deploy to Render

### Step 1: Commit the Management Command

The management command has been created at:
`sirms/incidents/management/commands/create_mercado.py`

### Step 2: Deploy to Render

```bash
cd sirms
git add .
git commit -m "Add Ms. Mercado teacher account creation command"
git push origin main
```

### Step 3: Run Command on Render

After deployment completes, go to Render Dashboard:

1. Go to your Render dashboard: https://dashboard.render.com
2. Click on your SIRMS service
3. Go to the "Shell" tab
4. Run this command:

```bash
python manage.py create_mercado
```

This will create the account in Render's PostgreSQL database.

### Alternative: Use Render Shell Directly

Or run this one-liner in Render Shell:

```bash
python manage.py shell -c "from incidents.models import CustomUser, TeacherAssignment; CustomUser.objects.filter(username='stephanie.mercado').delete(); user = CustomUser.objects.create_user(username='stephanie.mercado', password='Teacher2024!', email='stephanie.mercado@school.edu', first_name='Stephanie', last_name='Mercado', role='teacher', employee_id='TCH-2024-008', grade_level='Grade 8', section='Section 2', is_active=True); TeacherAssignment.objects.get_or_create(teacher_name='Ms. Stephanie Mercado', grade_level='8', section_name='Section 2', track_code='ICT'); print('Account created!')"
```

## Quick Deploy Script

I'll create a deployment script for you.
