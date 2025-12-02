"""
Script to create staff accounts for DMLMHS SIRMS
Run this script to create Guidance, DO, and ESP Teacher accounts
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sirms_project.settings')
django.setup()

from incidents.models import CustomUser

def create_staff_accounts():
    """Create staff accounts for the system"""
    
    accounts_created = []
    accounts_existing = []
    
    # 1. Create Guidance Counselor Account
    guidance_email = 'dmlmhs.guidance@gmail.com'
    if not CustomUser.objects.filter(email=guidance_email).exists():
        guidance = CustomUser.objects.create_user(
            username='guidance_counselor',
            email=guidance_email,
            password='dmlmhsguidance000',
            first_name='Guidance',
            last_name='Counselor',
            role='counselor'
        )
        accounts_created.append(f"✅ Guidance Counselor: {guidance_email}")
    else:
        accounts_existing.append(f"⚠️  Guidance Counselor already exists: {guidance_email}")
    
    # 2. Create Discipline Officer Account
    do_email = 'dmlmhs.do@gmail.com'
    if not CustomUser.objects.filter(email=do_email).exists():
        do_user = CustomUser.objects.create_user(
            username='discipline_officer',
            email=do_email,
            password='dmlmhsdo000',
            first_name='Discipline',
            last_name='Officer',
            role='do'
        )
        accounts_created.append(f"✅ Discipline Officer: {do_email}")
    else:
        accounts_existing.append(f"⚠️  Discipline Officer already exists: {do_email}")
    
    # 3. Create 5 ESP Teacher Accounts
    esp_teachers = [
        {'last_name': 'Garcia', 'first_name': 'Maria', 'middle_name': 'Santos'},
        {'last_name': 'Reyes', 'first_name': 'Juan', 'middle_name': 'Dela Cruz'},
        {'last_name': 'Santos', 'first_name': 'Ana', 'middle_name': 'Lopez'},
        {'last_name': 'Cruz', 'first_name': 'Pedro', 'middle_name': 'Ramos'},
        {'last_name': 'Lopez', 'first_name': 'Rosa', 'middle_name': 'Mendoza'},
    ]
    
    for teacher in esp_teachers:
        email = f"{teacher['last_name'].lower()}.espteacher@gmail.com"
        username = f"{teacher['last_name'].lower()}_esp"
        
        if not CustomUser.objects.filter(email=email).exists():
            esp_user = CustomUser.objects.create_user(
                username=username,
                email=email,
                password='dmlmhsesp000',  # Default password for all ESP teachers
                first_name=teacher['first_name'],
                middle_name=teacher['middle_name'],
                last_name=teacher['last_name'],
                role='esp_teacher'
            )
            accounts_created.append(f"✅ ESP Teacher: {email} ({teacher['first_name']} {teacher['last_name']})")
        else:
            accounts_existing.append(f"⚠️  ESP Teacher already exists: {email}")
    
    # Print results
    print("\n" + "="*70)
    print("DMLMHS SIRMS - Staff Accounts Creation")
    print("="*70)
    
    if accounts_created:
        print("\n✅ ACCOUNTS CREATED:")
        for account in accounts_created:
            print(f"   {account}")
    
    if accounts_existing:
        print("\n⚠️  ACCOUNTS ALREADY EXIST:")
        for account in accounts_existing:
            print(f"   {account}")
    
    print("\n" + "="*70)
    print("ACCOUNT CREDENTIALS:")
    print("="*70)
    print("\n📧 GUIDANCE COUNSELOR:")
    print(f"   Email: dmlmhs.guidance@gmail.com")
    print(f"   Password: dmlmhsguidance000")
    
    print("\n👮 DISCIPLINE OFFICER:")
    print(f"   Email: dmlmhs.do@gmail.com")
    print(f"   Password: dmlmhsdo000")
    
    print("\n👨‍🏫 ESP TEACHERS (All 5):")
    print(f"   Password: dmlmhsesp000 (same for all)")
    print(f"   Emails:")
    for teacher in esp_teachers:
        email = f"{teacher['last_name'].lower()}.espteacher@gmail.com"
        print(f"      - {email} ({teacher['first_name']} {teacher['last_name']})")
    
    print("\n" + "="*70)
    print(f"Total accounts created: {len(accounts_created)}")
    print(f"Total accounts existing: {len(accounts_existing)}")
    print("="*70 + "\n")

if __name__ == '__main__':
    create_staff_accounts()
