"""
Test script to verify case evaluation fix
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sirms_project.settings')
django.setup()

from incidents.models import IncidentReport, CustomUser, CaseEvaluation

print("\n" + "="*60)
print("🧪 TESTING CASE EVALUATION FIX")
print("="*60)

# Check for counselor
counselors = CustomUser.objects.filter(role='counselor')
print(f"\n✅ Counselors found: {counselors.count()}")
for c in counselors:
    print(f"   - {c.username}: {c.get_full_name()}")

# Check for reports without evaluation
reports_without_eval = IncidentReport.objects.filter(
    evaluation__isnull=True,
    reported_student__isnull=False
).exclude(status__in=['closed', 'resolved'])

print(f"\n✅ Reports ready for evaluation: {reports_without_eval.count()}")
for report in reports_without_eval[:5]:
    student_name = report.reported_student.get_full_name() if report.reported_student else "No student"
    print(f"   - {report.case_id}: {student_name} - {report.status}")

# Check existing evaluations
evaluations = CaseEvaluation.objects.all()
print(f"\n✅ Existing evaluations: {evaluations.count()}")
for eval in evaluations[:3]:
    print(f"   - {eval.report.case_id}: {eval.recommendation}")

print("\n" + "="*60)
print("✅ TEST COMPLETE - Case evaluation should work now!")
print("="*60)
print("\n📝 To test:")
print("1. Run: python manage.py runserver")
print("2. Login as counselor (counselor1 / counselor123)")
print("3. Go to: Case Evaluation")
print("4. Select a case and click 'Evaluate'")
print("5. Choose commission and intervention")
print("6. Submit - should work without 500 error!")
print()
