import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sirms_project.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from incidents.models import CustomUser

print("="*60)
print("ALL USERS IN DATABASE")
print("="*60)

users = CustomUser.objects.all()

if users.count() == 0:
    print("No users found in database!")
else:
    for user in users:
        print(f"\nUsername: {user.username}")
        print(f"  Name: {user.get_full_name()}")
        print(f"  Email: {user.email}")
        print(f"  Role: {user.get_role_display()}")
        print(f"  Active: {user.is_active}")
        print(f"  Has Password: {user.has_usable_password()}")
        if user.role == 'teacher':
            print(f"  Grade/Section: {user.grade_level} {user.section}")

print("\n" + "="*60)
print(f"Total users: {users.count()}")
print("="*60)

# Check specifically for stephanie.mercado
print("\nLooking for stephanie.mercado...")
try:
    user = CustomUser.objects.get(username='stephanie.mercado')
    print("✓ FOUND!")
    print(f"  Full details: {user}")
except CustomUser.DoesNotExist:
    print("✗ NOT FOUND - Account does not exist in this database")
    print("\nThis means you're either:")
    print("  1. Testing on production (Render) but account was created locally")
    print("  2. Using a different database")
    print("  3. Account was not created successfully")
