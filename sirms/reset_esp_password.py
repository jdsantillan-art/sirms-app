"""
Reset ESP Teacher password
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sirms_project.settings')
django.setup()

from incidents.models import CustomUser

print("=" * 60)
print("RESET ESP TEACHER PASSWORD")
print("=" * 60)

username = "esp_teacher"
new_password = "esp123"

try:
    user = CustomUser.objects.get(username=username)
    user.set_password(new_password)
    user.save()
    
    print(f"\n✓ Password reset successfully for '{username}'!")
    print("\n" + "-" * 60)
    print("LOGIN CREDENTIALS:")
    print("-" * 60)
    print(f"Username: {username}")
    print(f"Password: {new_password}")
    print(f"Email: {user.email}")
    print(f"Name: {user.get_full_name()}")
    print(f"Role: {user.get_role_display()}")
    print("-" * 60)
    
except CustomUser.DoesNotExist:
    print(f"\n✗ User '{username}' not found!")
    print("\nCreating new ESP teacher account...")
    
    user = CustomUser.objects.create_user(
        username=username,
        email="esp.teacher@school.edu",
        password=new_password,
        first_name="Maria",
        last_name="Garcia",
        role="esp_teacher"
    )
    
    print(f"\n✓ ESP Teacher account created!")
    print("\n" + "-" * 60)
    print("LOGIN CREDENTIALS:")
    print("-" * 60)
    print(f"Username: {username}")
    print(f"Password: {new_password}")
    print(f"Email: {user.email}")
    print(f"Name: {user.get_full_name()}")
    print(f"Role: {user.get_role_display()}")
    print("-" * 60)

print("\n" + "=" * 60)
