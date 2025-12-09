import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sirms_project.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from incidents.models import CustomUser
from django.contrib.auth import authenticate

print("="*60)
print("VERIFYING MS. MERCADO'S ACCOUNT")
print("="*60)

# Check if user exists
try:
    user = CustomUser.objects.get(username='stephanie.mercado')
    print(f"✓ User found: {user.username}")
    print(f"  - Full Name: {user.get_full_name()}")
    print(f"  - Email: {user.email}")
    print(f"  - Role: {user.role}")
    print(f"  - Employee ID: {user.employee_id}")
    print(f"  - Grade Level: {user.grade_level}")
    print(f"  - Section: {user.section}")
    print(f"  - Is Active: {user.is_active}")
    print(f"  - Has Usable Password: {user.has_usable_password()}")
    
    # Test authentication
    print("\n" + "="*60)
    print("TESTING LOGIN")
    print("="*60)
    
    auth_user = authenticate(username='stephanie.mercado', password='Teacher2024!')
    
    if auth_user is not None:
        print("✓ LOGIN SUCCESSFUL!")
        print(f"  Authenticated as: {auth_user.get_full_name()}")
    else:
        print("✗ LOGIN FAILED - Password does not match")
        print("\nAttempting to reset password...")
        user.set_password('Teacher2024!')
        user.save()
        print("✓ Password has been reset")
        
        # Test again
        auth_user = authenticate(username='stephanie.mercado', password='Teacher2024!')
        if auth_user is not None:
            print("✓ LOGIN NOW WORKS!")
        else:
            print("✗ Still having issues - checking user status...")
            if not user.is_active:
                user.is_active = True
                user.save()
                print("✓ User activated")
    
except CustomUser.DoesNotExist:
    print("✗ User 'stephanie.mercado' does not exist!")
    print("\nCreating account now...")
    
    user = CustomUser.objects.create_user(
        username='stephanie.mercado',
        password='Teacher2024!',
        email='stephanie.mercado@school.edu',
        first_name='Stephanie',
        last_name='Mercado',
        role='teacher',
        employee_id='TCH-2024-008',
        grade_level='Grade 8',
        section='Section 2'
    )
    user.is_active = True
    user.save()
    print("✓ Account created successfully!")

print("\n" + "="*60)
print("FINAL CREDENTIALS")
print("="*60)
print("Username: stephanie.mercado")
print("Password: Teacher2024!")
print("="*60)
