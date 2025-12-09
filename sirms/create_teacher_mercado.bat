@echo off
echo Creating teacher account for Ms. Stephanie Mercado...
echo.

python manage.py shell -c "from django.contrib.auth.models import User; from incidents.models import Teacher, TeacherAssignment; user, created = User.objects.get_or_create(username='stephanie.mercado', defaults={'email': 'stephanie.mercado@school.edu', 'first_name': 'Stephanie', 'last_name': 'Mercado'}); user.set_password('Teacher2024!'); user.save(); teacher, _ = Teacher.objects.get_or_create(user=user, defaults={'employee_id': 'TCH-2024-008', 'department': 'Junior High School', 'contact_number': '09XX-XXX-XXXX', 'email_notifications_enabled': True}); teacher.email_notifications_enabled = True; teacher.save(); assignment, _ = TeacherAssignment.objects.get_or_create(teacher=teacher, grade_level='Grade 8', section='Section 2', defaults={'subject': 'ICT', 'is_adviser': True, 'school_year': '2024-2025'}); assignment.is_adviser = True; assignment.subject = 'ICT'; assignment.save(); print('SUCCESS: Teacher account created!'); print(f'Username: stephanie.mercado'); print(f'Password: Teacher2024!'); print(f'Assignment: Grade 8 Section 2 (ICT)'); print(f'Email Notifications: ENABLED')"

echo.
echo ============================================================
echo ACCOUNT CREATED SUCCESSFULLY
echo ============================================================
echo.
pause
