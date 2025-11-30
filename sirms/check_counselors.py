"""
Check and display counselors in the database
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sirms_project.settings')
django.setup()

from incidents.models import Counselor

print("=" * 60)
print("COUNSELORS IN DATABASE")
print("=" * 60)

counselors = Counselor.objects.all()
print(f"\nTotal counselors: {counselors.count()}")

if counselors.exists():
    print("\nCounselor List:")
    print("-" * 60)
    for counselor in counselors:
        status = "✓ Active" if counselor.is_active else "✗ Inactive"
        print(f"  {status} | {counselor.name}")
        if counselor.specialization:
            print(f"           Specialization: {counselor.specialization}")
        if counselor.email:
            print(f"           Email: {counselor.email}")
        print()
else:
    print("\n⚠ No counselors found in database!")
    print("\nTo add counselors:")
    print("1. Go to the SIRMS web interface")
    print("2. Navigate to 'Manage Counselors'")
    print("3. Add VPF teachers/counselors there")
    print("\nOr run: python add_sample_counselors.py")

print("=" * 60)
