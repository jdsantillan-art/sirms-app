"""
Fix student assignments for existing reports
"""
import os
import django
import re

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sirms_project.settings')
django.setup()

from incidents.models import IncidentReport, CustomUser

print("=" * 60)
print("FIX STUDENT ASSIGNMENTS")
print("=" * 60)

# Get all reports without a reported_student
reports_without_student = IncidentReport.objects.filter(reported_student__isnull=True)

print(f"\nFound {reports_without_student.count()} reports without assigned students")
print("-" * 60)

fixed_count = 0
not_fixed_count = 0

for report in reports_without_student:
    print(f"\nCase {report.case_id}:")
    print(f"  Involved Students: {report.involved_students or 'None'}")
    
    if report.involved_students:
        # Try to find student
        potential_identifiers = re.split(r'[,;\n]+', report.involved_students)
        
        student_found = False
        for identifier in potential_identifiers:
            identifier = identifier.strip()
            if identifier:
                # Try email
                student = CustomUser.objects.filter(
                    role='student',
                    email__iexact=identifier
                ).first()
                
                # Try username
                if not student:
                    student = CustomUser.objects.filter(
                        role='student',
                        username__iexact=identifier
                    ).first()
                
                # Try partial name match
                if not student and len(identifier) > 3:
                    student = CustomUser.objects.filter(
                        role='student',
                        first_name__icontains=identifier
                    ).first() or CustomUser.objects.filter(
                        role='student',
                        last_name__icontains=identifier
                    ).first()
                
                if student:
                    report.reported_student = student
                    report.save()
                    print(f"  ✓ Assigned to: {student.get_full_name()} ({student.email})")
                    fixed_count += 1
                    student_found = True
                    break
        
        if not student_found:
            print(f"  ✗ Could not find matching student")
            not_fixed_count += 1
    else:
        print(f"  ✗ No involved students text")
        not_fixed_count += 1

print("\n" + "=" * 60)
print(f"Summary: {fixed_count} fixed, {not_fixed_count} not fixed")
print("=" * 60)
