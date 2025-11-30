"""
Add sample VPF teachers/counselors to the database
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sirms_project.settings')
django.setup()

from incidents.models import Counselor

print("=" * 60)
print("ADDING SAMPLE VPF TEACHERS/COUNSELORS")
print("=" * 60)

sample_counselors = [
    {
        'name': 'Ms. Maria Santos',
        'email': 'maria.santos@school.edu',
        'phone': '09171234567',
        'specialization': 'Behavioral Counseling',
        'is_active': True
    },
    {
        'name': 'Mr. Juan Dela Cruz',
        'email': 'juan.delacruz@school.edu',
        'phone': '09187654321',
        'specialization': 'Values Formation',
        'is_active': True
    },
    {
        'name': 'Ms. Ana Reyes',
        'email': 'ana.reyes@school.edu',
        'phone': '09191234567',
        'specialization': 'Academic Counseling',
        'is_active': True
    },
]

added_count = 0
skipped_count = 0

for counselor_data in sample_counselors:
    # Check if counselor already exists
    existing = Counselor.objects.filter(name=counselor_data['name']).first()
    
    if existing:
        print(f"⊘ Skipped: {counselor_data['name']} (already exists)")
        skipped_count += 1
    else:
        counselor = Counselor.objects.create(**counselor_data)
        print(f"✓ Added: {counselor.name} - {counselor.specialization}")
        added_count += 1

print("\n" + "=" * 60)
print(f"Summary: {added_count} added, {skipped_count} skipped")
print(f"Total counselors in database: {Counselor.objects.count()}")
print("=" * 60)
