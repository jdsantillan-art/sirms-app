from incidents.models import CustomUser, IncidentReport, Classification

print("=== DO Users ===")
dos = CustomUser.objects.filter(role='do')
print(f"Found {dos.count()} DO users:")
for u in dos:
    print(f"  - {u.username} ({u.get_full_name()})")

print("\n=== Behavior Concerns (Minor Cases) ===")
minor_cases = IncidentReport.objects.filter(classification__severity='minor')
print(f"Found {minor_cases.count()} behavior concern cases")
for c in minor_cases[:5]:
    incident_name = c.incident_type.name if c.incident_type else "No type"
    print(f"  - {c.case_id}: {incident_name} - Status: {c.status}")

print("\n=== All Classified Cases ===")
all_classified = IncidentReport.objects.filter(status='classified')
print(f"Found {all_classified.count()} classified cases total")
