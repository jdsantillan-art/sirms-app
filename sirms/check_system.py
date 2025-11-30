import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sirms_project.settings')
django.setup()

from incidents.models import CustomUser, IncidentReport, Classification

print("=== DO Users ===")
dos = CustomUser.objects.filter(role='do')
print(f"Found {dos.count()} DO users:")
for u in dos:
    print(f"  - Username: {u.username}, Name: {u.get_full_name()}, Email: {u.email}")

print("\n=== Behavior Concerns (Minor Cases) ===")
minor_cases = IncidentReport.objects.filter(classification__severity='minor')
print(f"Found {minor_cases.count()} behavior concern cases")
for c in minor_cases[:10]:
    incident_name = c.incident_type.name if c.incident_type else "No type"
    print(f"  - {c.case_id}: {incident_name} - Status: {c.status}")

print("\n=== All Classified Cases ===")
all_classified = IncidentReport.objects.filter(status='classified')
print(f"Found {all_classified.count()} classified cases total")

print("\n=== All Reports ===")
all_reports = IncidentReport.objects.all()
print(f"Total reports in system: {all_reports.count()}")
