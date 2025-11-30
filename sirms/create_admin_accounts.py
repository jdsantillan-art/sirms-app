"""
Create Discipline Officer and Counselor accounts (Admin only)
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sirms_project.settings')
django.setup()

from incidents.models import CustomUser

print("=" * 60)
print("CREATE ADMIN ACCOUNTS (DO & COUNSELOR)")
print("=" * 60)

accounts = [
    {
        'username': 'do_admin',
        'email': 'do@school.edu',
        'password': 'do123',
        'first_name': 'Discipline',
        'last_name': 'Officer',
        'role': 'do'
    },
    {
        'username': 'counselor_admin',
        'email': 'counselor@school.edu',
        'password': 'counselor123',
        'first_name': 'Guidance',
        'last_name': 'Counselor',
        'role': 'counselor'
    },
]

created = []
existing = []

for account in accounts:
    username = account['username']
    
    if CustomUser.objects.filter(username=username).exists():
        existing.append(username)
        print(f"⊘ {username} already exists")
    else:
        user = CustomUser.objects.create_user(
            username=account['username'],
            email=account['email'],
            password=account['password'],
            first_name=account['first_name'],
            last_name=account['last_name'],
            role=account['role']
        )
        created.append(username)
        print(f"\n✓ Created: {username}")
        print(f"  Name: {user.get_full_name()}")
        print(f"  Email: {user.email}")
        print(f"  Role: {user.get_role_display()}")
        print(f"  Password: {account['password']}")

print("\n" + "=" * 60)
print(f"Summary: {len(created)} created, {len(existing)} already existed")
print("=" * 60)

if created:
    print("\n⚠️  IMPORTANT: Change these default passwords after first login!")
