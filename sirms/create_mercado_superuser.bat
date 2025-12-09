@echo off
echo Creating Ms. Mercado's account using Django admin...
echo.
echo When prompted:
echo   Username: stephanie.mercado
echo   Email: stephanie.mercado@school.edu
echo   Password: Teacher2024!
echo   Password (again): Teacher2024!
echo.
pause
python manage.py createsuperuser --username stephanie.mercado --email stephanie.mercado@school.edu
echo.
echo Now updating role to teacher...
python manage.py shell -c "from incidents.models import CustomUser; u = CustomUser.objects.get(username='stephanie.mercado'); u.role = 'teacher'; u.employee_id = 'TCH-2024-008'; u.grade_level = 'Grade 8'; u.section = 'Section 2'; u.save(); print('✓ Role updated to teacher')"
echo.
echo Account ready!
pause
