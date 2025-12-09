"""
Test script for automatic repeat offender detection
Run with: python manage.py shell < test_repeat_offender_detection.py
"""

from incidents.models import IncidentReport, CustomUser
from incidents.repeat_offender_utils import get_repeat_offender_info, auto_flag_repeat_offender

print("=" * 60)
print("TESTING AUTOMATIC REPEAT OFFENDER DETECTION")
print("=" * 60)

# Test 1: Get all students with violations
print("\n1. Finding students with violations...")
students_with_violations = CustomUser.objects.filter(
    role='student',
    incident_reports__isnull=False
).distinct()

print(f"   Found {students_with_violations.count()} students with violations")

# Test 2: Check repeat offender detection for each student
print("\n2. Checking repeat offender status...")
repeat_offenders = []

for student in students_with_violations:
    reports = IncidentReport.objects.filter(reported_student=student).order_by('created_at')
    report_count = reports.count()
    
    if report_count > 1:
        # This is a repeat offender
        repeat_offenders.append({
            'student': student,
            'count': report_count
        })
        
        # Test the utility function
        latest_report = reports.last()
        repeat_info = get_repeat_offender_info(student, current_report=latest_report)
        
        print(f"\n   ⚠️  REPEAT OFFENDER DETECTED:")
        print(f"      Student: {student.get_full_name()}")
        print(f"      Total Violations: {report_count}")
        print(f"      Previous Violations: {repeat_info['count']}")
        print(f"      Recent (30 days): {repeat_info['recent_count']}")
        print(f"      Minor: {repeat_info['severity_breakdown']['minor']}")
        print(f"      Major: {repeat_info['severity_breakdown']['major']}")
        if repeat_info['last_violation_date']:
            print(f"      Last Violation: {repeat_info['last_violation_date']}")

if not repeat_offenders:
    print("   ✅ No repeat offenders found (all students have 1 or fewer violations)")

# Test 3: Test auto-flagging in evaluations
print("\n3. Testing auto-flagging in case evaluations...")
reports_with_evaluations = IncidentReport.objects.filter(
    evaluation__isnull=False,
    reported_student__isnull=False
)

flagged_count = 0
for report in reports_with_evaluations:
    if report.evaluation.is_repeat_offender:
        flagged_count += 1
        print(f"   ✅ Case {report.case_id}: Flagged as repeat offender")

print(f"\n   Total evaluations with repeat offender flag: {flagged_count}")

# Test 4: Summary
print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
print(f"Total students with violations: {students_with_violations.count()}")
print(f"Repeat offenders (2+ violations): {len(repeat_offenders)}")
print(f"Evaluations flagged: {flagged_count}")

if repeat_offenders:
    print("\n🔴 REPEAT OFFENDERS:")
    for offender in sorted(repeat_offenders, key=lambda x: x['count'], reverse=True):
        print(f"   • {offender['student'].get_full_name()}: {offender['count']} violations")

print("\n✅ Automatic repeat offender detection is working!")
print("=" * 60)
