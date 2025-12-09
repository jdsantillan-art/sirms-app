import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sirms_project.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from incidents.models import CustomUser

username = 'stephanie.mercado'
new_password = 'Teacher2024!'

try:
    user = CustomUser.objects.get(username=username)
    user.set_password(new_password)
    user.is_active = True
    user.save()
    
    print("="*60)
    print("PASSWORD RESET SUCCESSFUL")
    print("="*60)
    print(f"Username: {username}")
    print(f"Password: {new_password}")
    print(f"Name: {user.get_full_name()}")
    print(f"Role: {user.get_role_display()}")
    print(f"Active: {user.is_active}")
    print("="*60)
    print("\nYou can now login with these credentials!")
    
except CustomUser.DoesNotExist:
    print(f"User '{username}' not found. Creating new account...")
    
    user = CustomUser.objects.create_user(
        username=username,
        password=new_password,
        email='stephanie.mercado@school.edu',
        first_name='Stephanie',
        last_name='Mercado',
        role='teacher',
        employee_id='TCH-2024-008',
        grade_level='Grade 8',
        section='Section 2',
        is_active=True
    )
    
    print("="*60)
    print("ACCOUNT CREATED SUCCESSFULLY")
    print("="*60)
    print(f"Username: {username}")
    print(f"Password: {new_password}")
    print(f"Name: {user.get_full_name()}")
    print(f"Role: {user.get_role_display()}")
    print("="*60)
