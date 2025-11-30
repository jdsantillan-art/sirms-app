"""
Create an ESP Teacher account
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sirms_project.settings')
django.setup()

from incidents.models import CustomUser

print("=" * 60)
print("CREATE ESP TEACHER ACCOUNT")
print("=" * 60)

# ESP Teacher details
username = "esp_teacher"
email = "esp.teacher@school.edu"
password = "esp123"  # Change this to a secure password
first_name = "Maria"
last_name = "Garcia"
role = "esp_teacher"

# Check if user already exists
existing_user = CustomUser.objects.filter(username=username).first()

if existing_user:
    print(f"\n⚠ User '{username}' already exists!")
    print(f"   Name: {existing_user.get_full_name()}")
    print(f"   Email: {existing_user.email}")
    print(f"   Role: {existing_user.get_role_display()}")
else:
    # Create the ESP teacher user
    user = CustomUser.objects.create_user(
        username=username,
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
        role=role
    )
    
    print("\n✓ ESP Teacher account created successfully!")
    print("\n" + "-" * 60)
    print("LOGIN CREDENTIALS:")
    print("-" * 60)
    print(f"Username: {username}")
    print(f"Password: {password}")
    print(f"Email: {email}")
    print(f"Name: {user.get_full_name()}")
    print(f"Role: {user.get_role_display()}")
    print("-" * 60)
    print("\nYou can now login with these credentials!")

print("\n" + "=" * 60)
