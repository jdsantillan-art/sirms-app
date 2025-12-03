"""
Add ESP Teachers to Counselor Model
This makes them available in Manage ESP Teachers and For VRF assignment
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sirms_project.settings')
django.setup()

from incidents.models import Counselor, CustomUser

print("=" * 70)
print("ADDING ESP TEACHERS TO COUNSELOR MODEL")
print("=" * 70)
print()

# ESP Teacher data
esp_teachers = [
    {
        'name': 'Maria Santos Garcia',
        'email': 'garcia.espteacher@gmail.com',
        'phone': '0912 345 6789',
        'specialization': 'ESP Teacher/VPF Coordinator'
    },
    {
        'name': 'Juan Dela Cruz Reyes',
        'email': 'reyes.espteacher@gmail.com',
        'phone': '0923 456 7890',
        'specialization': 'ESP Teacher/VPF Coordinator'
    },
    {
        'name': 'Ana Lopez Santos',
        'email': 'santos.espteacher@gmail.com',
        'phone': '0934 567 8901',
        'specialization': 'ESP Teacher/VPF Coordinator'
    },
    {
        'name': 'Pedro Ramos Cruz',
        'email': 'cruz.espteacher@gmail.com',
        'phone': '0945 678 9012',
        'specialization': 'ESP Teacher/VPF Coordinator'
    },
    {
        'name': 'Rosa Mendoza Lopez',
        'email': 'lopez.espteacher@gmail.com',
        'phone': '0956 789 0123',
        'specialization': 'ESP Teacher/VPF Coordinator'
    }
]

print("Adding ESP Teachers to Counselor model...")
print()

added_count = 0
updated_count = 0

for teacher_data in esp_teachers:
    # Check if counselor entry already exists
    counselor, created = Counselor.objects.get_or_create(
        email=teacher_data['email'],
        defaults={
            'name': teacher_data['name'],
            'phone': teacher_data['phone'],
            'specialization': teacher_data['specialization'],
            'is_active': True
        }
    )
    
    if created:
        print(f"✅ Added: {teacher_data['name']}")
        print(f"   Email: {teacher_data['email']}")
        print(f"   Phone: {teacher_data['phone']}")
        print(f"   Specialization: {teacher_data['specialization']}")
        added_count += 1
    else:
        # Update existing entry
        counselor.name = teacher_data['name']
        counselor.phone = teacher_data['phone']
        counselor.specialization = teacher_data['specialization']
        counselor.is_active = True
        counselor.save()
        print(f"✅ Updated: {teacher_data['name']}")
        updated_count += 1
    print()

print("=" * 70)
print("SUMMARY")
print("=" * 70)
print(f"✅ Added: {added_count} ESP Teachers")
print(f"✅ Updated: {updated_count} ESP Teachers")
print(f"✅ Total: {Counselor.objects.filter(specialization='ESP Teacher/VPF Coordinator').count()} ESP Teachers in system")
print()
print("ESP Teachers are now available in:")
print("  - Manage ESP Teachers page")
print("  - For VRF assignment dropdown")
print()
print("=" * 70)
