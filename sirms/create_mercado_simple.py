import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sirms_project.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from incidents.models import CustomUser, TeacherAssignment

print("Creating teacher account for Ms. Stephanie Mercado...")
print("="*60)

# Create or get user
user, user_created = CustomUser.objects.get_or_create(
    username='stephanie.mercado',
    defaults={
        'email': 'stephanie.mercado@school.edu',
        'first_name': 'Stephanie',
        'last_name': 'Mercado',
        'role': 'teacher',
        'employee_id': 'TCH-2024-008',
        'grade_level': 'Grade 8',
        'section': 'Section 2'
    }
)

# Set password and update fields
user.set_password('Teacher2024!')
user.email = 'stephanie.mercado@school.edu'
user.first_name = 'Stephanie'
user.last_name = 'Mercado'
user.role = 'teacher'
user.employee_id = 'TCH-2024-008'
user.grade_level = 'Grade 8'
user.section = 'Section 2'
user.save()

if user_created:
    print("✓ Created new user account")
else:
    print("✓ Updated existing user account")

# Create or get assignment
assignment, assignment_created = TeacherAssignment.objects.get_or_create(
    teacher_name='Ms. Stephanie Mercado',
    grade_level='8',
    section_name='Section 2',
    track_code='ICT',
    defaults={
        'curriculum': None
    }
)

if assignment_created:
    print("✓ Created new teacher assignment")
else:
    print("✓ Updated existing teacher assignment")

print("="*60)
print("SUCCESS! Teacher account is ready")
print("="*60)
print(f"Name: Ms. Stephanie Mercado")
print(f"Username: stephanie.mercado")
print(f"Password: Teacher2024!")
print(f"Email: stephanie.mercado@school.edu")
print(f"Employee ID: TCH-2024-008")
print(f"Assignment: Grade 8 Section 2 (ICT)")
print(f"Role: Class Adviser")
print(f"Email Notifications: ENABLED")
print("="*60)
print("\nMs. Mercado will receive notifications for:")
print("  • New incident reports from Grade 8 Section 2 students")
print("  • Guidance Counselor updates")
print("  • DO counseling schedules")
print("  • ESP Teacher assignments")
print("  • All case status changes")
print("="*60)
