"""
Smart fix for student assignments - matches by name parts
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sirms_project.settings')
django.setup()

from incidents.models import IncidentReport, CustomUser

print("=" * 60)
print("SMART FIX STUDENT ASSIGNMENTS")
print("=" * 60)

reports_without_student = IncidentReport.objects.filter(reported_student__isnull=True)
print(f"\nFound {reports_without_student.count()} reports without assigned students\n")

fixed_count = 0

for report in reports_without_student:
    if not report.involved_students:
        continue
    
    name_text = report.involved_students.strip()
    name_parts = name_text.split()
    
    if len(name_parts) >= 2:
        # Try first and last name
        first_name = name_parts[0]
        last_name = name_parts[-1]
        
        student = CustomUser.objects.filter(
            role='student',
            first_name__icontains=first_name,
            last_name__icontains=last_name
        ).first()
        
        if student:
            report.reported_student = student
            report.save()
            print(f"✓ Case {report.case_id}: Assigned to {student.get_full_name()}")
            fixed_count += 1
            continue
    
    # Try single name match
    if len(name_parts) >= 1:
        name = name_parts[0]
        student = CustomUser.objects.filter(
            role='student',
            first_name__icontains=name
        ).first()
        
        if student:
            report.reported_student = student
            report.save()
            print(f"✓ Case {report.case_id}: Assigned to {student.get_full_name()} (partial match)")
            fixed_count += 1

print(f"\n{'=' * 60}")
print(f"Fixed {fixed_count} reports")
print("=" * 60)
