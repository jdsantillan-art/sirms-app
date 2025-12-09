import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sirms_project.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.contrib.auth import authenticate
from incidents.models import CustomUser

print("Testing login for stephanie.mercado...")
print("="*60)

# Test authentication
user = authenticate(username='stephanie.mercado', password='Teacher2024!')

if user is not None:
    print("✓ LOGIN SUCCESSFUL!")
    print(f"  Name: {user.get_full_name()}")
    print(f"  Email: {user.email}")
    print(f"  Role: {user.get_role_display()}")
    print(f"  Employee ID: {user.employee_id}")
    print(f"  Grade/Section: {user.grade_level} {user.section}")
    print("="*60)
    print("\nCredentials are working correctly!")
    print("Username: stephanie.mercado")
    print("Password: Teacher2024!")
else:
    print("✗ LOGIN FAILED")
    print("\nTrying to diagnose the issue...")
    
    try:
        user = CustomUser.objects.get(username='stephanie.mercado')
        print(f"User exists: {user.username}")
        print(f"Is active: {user.is_active}")
        print(f"Has usable password: {user.has_usable_password()}")
        
        # Force password reset
        print("\nResetting password...")
        user.set_password('Teacher2024!')
        user.is_active = True
        user.save()
        print("✓ Password reset complete")
        
        # Test again
        user = authenticate(username='stephanie.mercado', password='Teacher2024!')
        if user:
            print("✓ LOGIN NOW WORKS!")
        else:
            print("✗ Still not working - please check Django settings")
            
    except CustomUser.DoesNotExist:
        print("✗ User does not exist!")

print("="*60)
