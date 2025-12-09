@echo off
echo ============================================================
echo DEPLOYING MS. MERCADO'S ACCOUNT TO RENDER
echo ============================================================
echo.
echo This will:
echo 1. Add the account creation command to git
echo 2. Commit the changes
echo 3. Push to Render
echo.
pause

echo.
echo Step 1: Adding files to git...
git add incidents/management/commands/create_mercado.py
git add DEPLOY_MERCADO_TO_RENDER.md

echo.
echo Step 2: Committing changes...
git commit -m "Add Ms. Stephanie Mercado teacher account creation command"

echo.
echo Step 3: Pushing to Render...
git push origin main

echo.
echo ============================================================
echo DEPLOYMENT INITIATED
echo ============================================================
echo.
echo Next steps:
echo 1. Wait for Render to finish deploying (check dashboard)
echo 2. Go to Render Dashboard: https://dashboard.render.com
echo 3. Click on your SIRMS service
echo 4. Go to "Shell" tab
echo 5. Run: python manage.py create_mercado
echo.
echo OR run this one-liner in Render Shell:
echo.
echo python manage.py shell -c "from incidents.models import CustomUser, TeacherAssignment; CustomUser.objects.filter(username='stephanie.mercado').delete(); user = CustomUser.objects.create_user(username='stephanie.mercado', password='Teacher2024!', email='stephanie.mercado@school.edu', first_name='Stephanie', last_name='Mercado', role='teacher', employee_id='TCH-2024-008', grade_level='Grade 8', section='Section 2', is_active=True); TeacherAssignment.objects.get_or_create(teacher_name='Ms. Stephanie Mercado', grade_level='8', section_name='Section 2', track_code='ICT'); print('✓ Account created!')"
echo.
echo ============================================================
echo CREDENTIALS FOR MS. MERCADO
echo ============================================================
echo Username: stephanie.mercado
echo Password: Teacher2024!
echo ============================================================
echo.
pause
