"""
Fix DOSchedule migration by handling existing records
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sirms_project.settings')
django.setup()

from incidents.models import DOSchedule, CustomUser

print("Checking DOSchedule model...")

# Check if DOSchedule table exists
try:
    count = DOSchedule.objects.count()
    print(f"✓ DOSchedule table exists with {count} records")
    
    # Check if any records have null discipline_officer
    null_dos = DOSchedule.objects.filter(discipline_officer__isnull=True).count()
    if null_dos > 0:
        print(f"⚠ Found {null_dos} records with null discipline_officer")
        
        # Get first DO user as default
        first_do = CustomUser.objects.filter(role='do').first()
        if first_do:
            print(f"Setting default DO to: {first_do.get_full_name()}")
            DOSchedule.objects.filter(discipline_officer__isnull=True).update(
                discipline_officer=first_do
            )
            print("✓ Updated null records")
        else:
            print("✗ No DO users found to set as default")
    else:
        print("✓ All records have discipline_officer set")
    
except Exception as e:
    print(f"✗ Error: {e}")
    print("DOSchedule table may not exist yet - migrations needed")

print("\nReady to run migrations!")
