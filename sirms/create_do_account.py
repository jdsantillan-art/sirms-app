"""
Script to create a Discipline Officer (DO) account
Run: python create_do_account.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sirms_project.settings')
django.setup()

from incidents.models import CustomUser

def create_do_account():
    """Create a DO account"""
    print("\n" + "="*60)
    print("🔐 CREATE DISCIPLINE OFFICER ACCOUNT")
    print("="*60)
    
    # Get input
    username = input("\nEnter username (e.g., 'do_admin'): ").strip()
    if not username:
        username = "do_admin"
    
    email = input("Enter email (e.g., 'do@school.edu'): ").strip()
    if not email:
        email = "do@school.edu"
    
    password = input("Enter password (e.g., 'do123'): ").strip()
    if not password:
        password = "do123"
    
    first_name = input("Enter first name (e.g., 'John'): ").strip()
    if not first_name:
        first_name = "John"
    
    last_name = input("Enter last name (e.g., 'Doe'): ").strip()
    if not last_name:
        last_name = "Doe"
    
    # Check if user exists
    if CustomUser.objects.filter(username=username).exists():
        print(f"\n⚠️  User '{username}' already exists!")
        update = input("Update existing user? (y/n): ").strip().lower()
        if update != 'y':
            print("❌ Cancelled")
            return
        
        user = CustomUser.objects.get(username=username)
        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        user.role = 'discipline_officer'
        user.set_password(password)
        user.save()
        print(f"\n✅ Updated DO account: {username}")
    else:
        # Create new DO user
        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            role='discipline_officer'
        )
        print(f"\n✅ Created DO account: {username}")
    
    print("\n" + "="*60)
    print("📋 ACCOUNT DETAILS")
    print("="*60)
    print(f"Username: {user.username}")
    print(f"Password: {password}")
    print(f"Email: {user.email}")
    print(f"Name: {user.first_name} {user.last_name}")
    print(f"Role: {user.get_role_display()}")
    print("\n🔗 Login at: http://127.0.0.1:8000/login/")
    print("="*60 + "\n")

if __name__ == '__main__':
    create_do_account()
