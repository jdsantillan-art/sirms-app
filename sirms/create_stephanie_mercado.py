"""
Create ESP Teacher account for Ms. Stephanie Mercado
Grade 8 Section 2 (ICT)
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sirms_project.settings')
django.setup()

from django.contrib.auth.models import User
from incidents.models import Counselor, TeacherAssignment

def create_stephanie_mercado():
    """Create ESP Teacher account for Ms. Stephanie Mercado"""
    
    # Account details
    username = "stephanie.mercado"
    email = "stephanie.mercado@school.edu"
    password = "StephMercado2025!"
    first_name = "Stephanie"
    last_name = "Mercado"
    
    # Check if user already exists
    if User.objects.filter(username=username).exists():
        print(f"❌ User '{username}' already exists!")
        user = User.objects.get(username=username)
        print(f"✓ Using existing user: {user.get_full_name()}")
    else:
        # Create user account
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        print(f"✓ Created user account: {username}")
    
    # Check if counselor profile exists
    if Counselor.objects.filter(user=user).exists():
        counselor = Counselor.objects.get(user=user)
        print(f"✓ Using existing ESP Teacher profile")
    else:
        # Create ESP Teacher (Counselor) profile
        counselor = Counselor.objects.create(
            user=user,
            role='esp_teacher',
            department='Guidance',
            contact_number='09XX-XXX-XXXX'  # Update with actual number
        )
        print(f"✓ Created ESP Teacher profile")
    
    # Assign to Grade 8 Section 2
    grade_level = "Grade 8"
    section = "Section 2"
    subject = "ICT"
    
    # Check if assignment already exists
    assignment, created = TeacherAssignment.objects.get_or_create(
        teacher=counselor,
        grade_level=grade_level,
        section=section,
        defaults={'subject': subject}
    )
    
    if created:
        print(f"✓ Assigned to {grade_level} {section} ({subject})")
    else:
        print(f"✓ Already assigned to {grade_level} {section}")
    
    print("\n" + "="*60)
    print("ESP TEACHER ACCOUNT CREATED SUCCESSFULLY")
    print("="*60)
    print(f"Name: {first_name} {last_name}")
    print(f"Username: {username}")
    print(f"Password: {password}")
    print(f"Email: {email}")
    print(f"Role: ESP Teacher")
    print(f"Assignment: {grade_level} {section} - {subject}")
    print("="*60)
    print("\nNOTIFICATIONS:")
    print("✓ Will receive notifications when students from Grade 8 Section 2 report incidents")
    print("✓ Will receive updates from Guidance Counselors")
    print("✓ Will receive updates from Discipline Office (DO)")
    print("✓ Will receive case assignments and status updates")
    print("="*60)
    print("\nLOGIN URL: http://your-domain.com/login")
    print(f"Username: {username}")
    print(f"Password: {password}")
    print("="*60)
    
    return user, counselor

if __name__ == "__main__":
    try:
        user, counselor = create_stephanie_mercado()
        print("\n✅ Account setup complete!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
