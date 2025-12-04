"""
Verification script for Status Sync feature
Run this after deployment to verify everything works
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sirms_project.settings')
django.setup()

from incidents.models import IncidentReport, DOSchedule, CustomUser, Notification
from django.utils import timezone

def verify_status_sync():
    """Verify the status sync feature is working"""
    
    print("=" * 70)
    print("STATUS SYNC FEATURE VERIFICATION")
    print("=" * 70)
    print()
    
    # Check 1: Verify models exist
    print("✓ Check 1: Models")
    print("  - IncidentReport model:", "✅ OK" if IncidentReport else "❌ FAIL")
    print("  - DOSchedule model:", "✅ OK" if DOSchedule else "❌ FAIL")
    print("  - Notification model:", "✅ OK" if Notification else "❌ FAIL")
    print()
    
    # Check 2: Verify DO users exist
    print("✓ Check 2: DO Users")
    do_users = CustomUser.objects.filter(role='do')
    if do_users.exists():
        print(f"  ✅ Found {do_users.count()} DO user(s)")
        for do in do_users:
            print(f"     - {do.get_full_name()} ({do.username})")
    else:
        print("  ❌ No DO users found")
    print()
    
    # Check 3: Verify behavioral concerns exist
    print("✓ Check 3: Behavioral Concerns")
    reports = IncidentReport.objects.all()
    if reports.exists():
        print(f"  ✅ Found {reports.count()} report(s)")
        classified = reports.filter(status='classified').count()
        under_review = reports.filter(status='under_review').count()
        resolved = reports.filter(status='resolved').count()
        print(f"     - Classified: {classified}")
        print(f"     - Under Review (Scheduled): {under_review}")
        print(f"     - Resolved: {resolved}")
    else:
        print("  ⚠️  No reports found")
    print()
    
    # Check 4: Verify DO schedules exist
    print("✓ Check 4: DO Schedules")
    schedules = DOSchedule.objects.all()
    if schedules.exists():
        print(f"  ✅ Found {schedules.count()} schedule(s)")
        scheduled = schedules.filter(status='scheduled').count()
        completed = schedules.filter(status='completed').count()
        print(f"     - Scheduled: {scheduled}")
        print(f"     - Completed: {completed}")
        
        # Check for schedules with linked reports
        with_reports = schedules.filter(report__isnull=False).count()
        print(f"     - Linked to reports: {with_reports}")
    else:
        print("  ⚠️  No schedules found")
    print()
    
    # Check 5: Verify recent status changes
    print("✓ Check 5: Recent Activity")
    recent_reports = IncidentReport.objects.order_by('-updated_at')[:5]
    if recent_reports.exists():
        print("  Recent report updates:")
        for report in recent_reports:
            print(f"     - {report.case_id}: {report.get_status_display()} (Updated: {report.updated_at.strftime('%Y-%m-%d %H:%M')})")
    else:
        print("  ⚠️  No recent activity")
    print()
    
    # Check 6: Verify notifications
    print("✓ Check 6: Notifications")
    recent_notifications = Notification.objects.order_by('-created_at')[:5]
    if recent_notifications.exists():
        print("  Recent notifications:")
        for notif in recent_notifications:
            print(f"     - {notif.title} → {notif.user.get_full_name()} ({notif.created_at.strftime('%Y-%m-%d %H:%M')})")
    else:
        print("  ⚠️  No notifications found")
    print()
    
    # Check 7: Test data integrity
    print("✓ Check 7: Data Integrity")
    
    # Check for schedules with reports
    schedules_with_reports = DOSchedule.objects.filter(report__isnull=False)
    if schedules_with_reports.exists():
        print(f"  ✅ Found {schedules_with_reports.count()} schedule(s) linked to reports")
        
        # Check if statuses are in sync
        sync_issues = 0
        for schedule in schedules_with_reports:
            if schedule.status == 'scheduled' and schedule.report.status != 'under_review':
                print(f"     ⚠️  Sync issue: Schedule {schedule.id} is scheduled but report {schedule.report.case_id} is {schedule.report.status}")
                sync_issues += 1
            elif schedule.status == 'completed' and schedule.report.status != 'resolved':
                print(f"     ⚠️  Sync issue: Schedule {schedule.id} is completed but report {schedule.report.case_id} is {schedule.report.status}")
                sync_issues += 1
        
        if sync_issues == 0:
            print("     ✅ All statuses are in sync!")
        else:
            print(f"     ⚠️  Found {sync_issues} sync issue(s)")
    else:
        print("  ℹ️  No schedules linked to reports yet")
    print()
    
    # Summary
    print("=" * 70)
    print("VERIFICATION SUMMARY")
    print("=" * 70)
    print()
    
    if do_users.exists() and reports.exists():
        print("✅ System is ready for testing!")
        print()
        print("Next steps:")
        print("1. Login as DO user")
        print("2. Create a schedule for a behavioral concern")
        print("3. Verify status updates to 'Under Review'")
        print("4. Mark schedule as complete")
        print("5. Verify status updates to 'Resolved'")
    else:
        print("⚠️  System needs setup:")
        if not do_users.exists():
            print("   - Create DO user account")
        if not reports.exists():
            print("   - Create test behavioral concern")
    print()
    
    print("=" * 70)
    print("For detailed testing, run: python test_status_sync.py")
    print("=" * 70)

if __name__ == '__main__':
    verify_status_sync()
