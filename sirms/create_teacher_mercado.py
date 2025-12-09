"""
Create teacher account for Ms. Stephanie Mercado
JHS Grade 8 Section 2 (ICT)
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sirms_project.settings')
django.setup()

from django.contrib.auth.models import User
from incidents.models import Teacher, TeacherAssignment

def create_teacher_account():
    # Create user account
    username = 'stephanie.mercado'
    email = 'stephanie.mercado@school.edu'
    password = 'Teacher2024!'
    
    # Check if user already exists
    if User.objects.filter(username=username).exists():
        print(f"User '{username}' already exists. Updating...")
        user = User.objects.get(username=username)
        user.email = email
        user.set_password(password)
        user.save()
    else:
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name='Stephanie',
            last_name='Mercado'
        )
        print(f"✓ Created user account: {username}")
    
    # Create or update Teacher profile
    teacher, created = Teacher.objects.get_or_create(
        user=user,
        defaults={
            'employee_id': 'TCH-2024-008',
            'department': 'Junior High School',
            'contact_number': '09XX-XXX-XXXX',
            'email_notifications_enabled': True
        }
    )
    
    if not created:
        teacher.employee_id = 'TCH-2024-008'
        teacher.department = 'Junior High School'
        teacher.email_notifications_enabled = True
        teacher.save()
        print(f"✓ Updated teacher profile for {user.get_full_name()}")
    else:
        print(f"✓ Created teacher profile for {user.get_full_name()}")
    
    # Create teacher assignment for Grade 8 Section 2 (ICT)
    assignment, created = TeacherAssignment.objects.get_or_create(
        teacher=teacher,
        grade_level='Grade 8',
        section='Section 2',
        defaults={
            'subject': 'ICT',
            'is_adviser': True,
            'school_year': '2024-2025'
        }
    )
    
    if not created:
        assignment.subject = 'ICT'
        assignment.is_adviser = True
        assignment.school_year = '2024-2025'
        assignment.save()
        print(f"✓ Updated assignment: Grade 8 Section 2 (ICT)")
    else:
        print(f"✓ Created assignment: Grade 8 Section 2 (ICT)")
    
    print("\n" + "="*60)
    print("TEACHER ACCOUNT CREATED SUCCESSFULLY")
    print("="*60)
    print(f"Name: Ms. Stephanie Mercado")
    print(f"Username: {username}")
    print(f"Password: {password}")
    print(f"Email: {email}")
    print(f"Employee ID: TCH-2024-008")
    print(f"Department: Junior High School")
    print(f"Assignment: Grade 8 Section 2 (ICT)")
    print(f"Role: Class Adviser")
    print(f"Email Notifications: ENABLED")
    print("="*60)
    print("\nNOTIFICATION FEATURES:")
    print("✓ Receives email when students from her class report incidents")
    print("✓ Gets updates when Guidance processes the report")
    print("✓ Notified when DO schedules counseling sessions")
    print("✓ Receives updates from ESP Teacher assignments")
    print("✓ Can view all reports from her students on dashboard")
    print("="*60)
    print("\nLOGIN INSTRUCTIONS:")
    print("1. Go to the SIRMS login page")
    print("2. Enter username: stephanie.mercado")
    print("3. Enter password: Teacher2024!")
    print("4. Access teacher dashboard to view student reports")
    print("="*60)

if __name__ == '__main__':
    create_teacher_account()
