"""
Test script to verify adviser notification feature
Run this after creating a counseling schedule to check if notifications are sent
"""
from incidents.models import Notification, CustomUser, IncidentReport, CounselingSchedule, VPFSchedule, DOSchedule
from django.utils import timezone

def test_adviser_notifications():
    """Check recent notifications sent to teachers"""
    print("\n=== Testing Adviser Notification Feature ===\n")
    
    # Get all teachers
    teachers = CustomUser.objects.filter(role='teacher')
    print(f"Total teachers in system: {teachers.count()}")
    
    # Check recent notifications to teachers (last 24 hours)
    recent_time = timezone.now() - timezone.timedelta(hours=24)
    recent_notifications = Notification.objects.filter(
        user__role='teacher',
        created_at__gte=recent_time
    ).order_by('-created_at')
    
    print(f"\nRecent notifications to teachers (last 24 hours): {recent_notifications.count()}")
    
    if recent_notifications.exists():
        print("\n--- Recent Teacher Notifications ---")
        for notif in recent_notifications[:10]:  # Show last 10
            print(f"\nTeacher: {notif.user.get_full_name()}")
            print(f"Title: {notif.title}")
            print(f"Message: {notif.message[:100]}...")
            print(f"Time: {notif.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"Read: {notif.is_read}")
    
    # Check recent counseling schedules
    recent_counseling = CounselingSchedule.objects.filter(
        created_at__gte=recent_time
    ).order_by('-created_at')
    
    print(f"\n\nRecent Counseling Schedules: {recent_counseling.count()}")
    for schedule in recent_counseling[:5]:
        print(f"\n- Student: {schedule.student.get_full_name()}")
        print(f"  Counselor: {schedule.counselor.get_full_name()}")
        print(f"  Date: {schedule.scheduled_date.strftime('%Y-%m-%d %H:%M')}")
        print(f"  Case: {schedule.evaluation.report.case_id}")
        
        # Check if report has teacher info
        report = schedule.evaluation.report
        print(f"  Report Teacher: {report.teacher_name}")
        print(f"  Report Grade: {report.grade_level}")
        print(f"  Report Section: {report.section_name}")
    
    # Check recent VPF schedules
    recent_vpf = VPFSchedule.objects.filter(
        created_at__gte=recent_time
    ).order_by('-created_at')
    
    print(f"\n\nRecent VPF Schedules: {recent_vpf.count()}")
    for schedule in recent_vpf[:5]:
        print(f"\n- Student: {schedule.vpf_case.student.get_full_name()}")
        print(f"  ESP Teacher: {schedule.esp_teacher.get_full_name()}")
        print(f"  Date: {schedule.scheduled_date.strftime('%Y-%m-%d %H:%M')}")
        print(f"  Case: {schedule.vpf_case.report.case_id}")
        
        # Check if report has teacher info
        report = schedule.vpf_case.report
        print(f"  Report Teacher: {report.teacher_name}")
        print(f"  Report Grade: {report.grade_level}")
        print(f"  Report Section: {report.section_name}")
    
    # Check recent DO schedules
    recent_do = DOSchedule.objects.filter(
        created_at__gte=recent_time
    ).order_by('-created_at')
    
    print(f"\n\nRecent DO Schedules: {recent_do.count()}")
    for schedule in recent_do[:5]:
        if schedule.student:
            print(f"\n- Student: {schedule.student.get_full_name()}")
            print(f"  DO: {schedule.discipline_officer.get_full_name()}")
            print(f"  Type: {schedule.get_schedule_type_display()}")
            print(f"  Date: {schedule.scheduled_date.strftime('%Y-%m-%d %H:%M')}")
            if schedule.report:
                print(f"  Case: {schedule.report.case_id}")
                print(f"  Report Teacher: {schedule.report.teacher_name}")
                print(f"  Report Grade: {schedule.report.grade_level}")
                print(f"  Report Section: {schedule.report.section_name}")
    
    print("\n\n=== Test Complete ===\n")

if __name__ == '__main__':
    # Run in Django shell: python manage.py shell < test_adviser_notifications.py
    test_adviser_notifications()
