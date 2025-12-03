"""
Test script to verify automatic status synchronization between
Behavioral Concerns (IncidentReport) and DO Schedule
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sirms_project.settings')
django.setup()

from incidents.models import IncidentReport, DOSchedule, CustomUser
from django.utils import timezone
from datetime import timedelta

def test_status_sync():
    """Test the automatic status synchronization"""
    
    print("=" * 60)
    print("TESTING BEHAVIORAL CONCERN <-> DO SCHEDULE STATUS SYNC")
    print("=" * 60)
    
    # Find a DO user
    do_user = CustomUser.objects.filter(role='do').first()
    if not do_user:
        print("❌ No DO user found. Please create a DO account first.")
        return
    
    print(f"\n✓ Found DO user: {do_user.get_full_name()}")
    
    # Find a behavioral concern (classified case)
    report = IncidentReport.objects.filter(status='classified').first()
    if not report:
        print("❌ No classified behavioral concern found.")
        return
    
    print(f"✓ Found behavioral concern: {report.case_id}")
    print(f"  Current status: {report.get_status_display()}")
    
    # Find a student
    student = report.reported_student
    if not student:
        student = CustomUser.objects.filter(role='student').first()
    
    if not student:
        print("❌ No student found.")
        return
    
    print(f"✓ Student: {student.get_full_name()}")
    
    # TEST 1: Create DO Schedule and check if Behavioral Concern status updates
    print("\n" + "=" * 60)
    print("TEST 1: Creating DO Schedule")
    print("=" * 60)
    
    scheduled_date = timezone.now() + timedelta(days=2)
    
    schedule = DOSchedule.objects.create(
        report=report,
        discipline_officer=do_user,
        student=student,
        schedule_type='parent_conference',
        scheduled_date=scheduled_date,
        location='Discipline Office',
        purpose=f'Parent conference for case {report.case_id}',
        status='scheduled'
    )
    
    print(f"✓ Created DO Schedule: {schedule}")
    print(f"  Schedule status: {schedule.get_status_display()}")
    
    # Refresh report from database
    report.refresh_from_db()
    
    print(f"\n📊 RESULT:")
    print(f"  Behavioral Concern status: {report.get_status_display()}")
    
    if report.status == 'under_review':
        print("  ✅ SUCCESS! Status automatically updated to 'Under Review' (Scheduled)")
    else:
        print(f"  ❌ FAILED! Expected 'under_review', got '{report.status}'")
    
    # TEST 2: Mark DO Schedule as completed and check if Behavioral Concern updates
    print("\n" + "=" * 60)
    print("TEST 2: Marking DO Schedule as Completed")
    print("=" * 60)
    
    schedule.status = 'completed'
    schedule.notes = 'Meeting completed successfully'
    schedule.save()
    
    print(f"✓ Updated DO Schedule status to: {schedule.get_status_display()}")
    
    # Refresh report from database
    report.refresh_from_db()
    
    print(f"\n📊 RESULT:")
    print(f"  Behavioral Concern status: {report.get_status_display()}")
    
    if report.status == 'resolved':
        print("  ✅ SUCCESS! Status automatically updated to 'Resolved' (Completed)")
    else:
        print(f"  ❌ FAILED! Expected 'resolved', got '{report.status}'")
    
    # Cleanup
    print("\n" + "=" * 60)
    print("CLEANUP")
    print("=" * 60)
    
    cleanup = input("\nDelete test schedule? (y/n): ").lower()
    if cleanup == 'y':
        schedule.delete()
        print("✓ Test schedule deleted")
        # Reset report status
        report.status = 'classified'
        report.save()
        print("✓ Report status reset to 'classified'")
    else:
        print("Test schedule kept for manual inspection")
    
    print("\n" + "=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)

if __name__ == '__main__':
    test_status_sync()
