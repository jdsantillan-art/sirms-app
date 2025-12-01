import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sirms_project.settings')
django.setup()

from incidents.models import IncidentType

total = IncidentType.objects.count()
prohibited = IncidentType.objects.filter(severity='prohibited').count()
school_policy = IncidentType.objects.filter(severity='school_policy').count()

print(f"\n📊 Violation Count:")
print(f"   Total: {total}")
print(f"   Prohibited Acts: {prohibited}")
print(f"   School Policies: {school_policy}")

if total == 0:
    print("\n❌ No violations found! Run: python load_violations.py")
else:
    print("\n✅ Violations are loaded!")
    print("\n📋 Sample violations:")
    for v in IncidentType.objects.all()[:5]:
        print(f"   - {v.name} ({v.severity})")
