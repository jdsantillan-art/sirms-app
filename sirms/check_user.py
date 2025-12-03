"""
Check if a specific user exists in the database
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sirms_project.settings')
django.setup()

from incidents.models import CustomUser

# Email to check
email_to_check = 'jdsantillan.chmsu@gmail.com'

print("=" * 70)
print("USER ACCOUNT CHECK")
print("=" * 70)
print()

# Check if user exists
user = CustomUser.objects.filter(email=email_to_check).first()

if user:
    print(f"✅ User found!")
    print(f"   Email: {user.email}")
    print(f"   Username: {user.username}")
    print(f"   Name: {user.get_full_name()}")
    print(f"   Role: {user.role}")
    print(f"   Active: {user.is_active}")
else:
    print(f"❌ User with email '{email_to_check}' NOT found")
    print()
    print("Available users in database:")
    print()
    
    all_users = CustomUser.objects.all()[:10]
    if all_users:
        for u in all_users:
            print(f"   - {u.email} ({u.get_full_name()}) - Role: {u.role}")
    else:
        print("   No users found in database")

print()
print("=" * 70)
