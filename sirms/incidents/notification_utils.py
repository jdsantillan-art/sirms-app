"""
Smart Notification Utility for Proper Process System
Handles notifications based on involved party types
"""
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from .models import Notification, CustomUser
from .email_utils import send_notification_email


def send_smart_notifications(report, event_type='status_update'):
    """
    Send notifications based on involved party types and event
    
    Args:
        report: IncidentReport instance
        event_type: Type of notification (report_submitted, party_confirmed, etc.)
    """
    notifications_sent = []
    
    # Always notify all DOs
    dos = CustomUser.objects.filter(role='do')
    for do in dos:
        notification = create_notification(
            user=do,
            title=get_notification_title(event_type, report, 'do'),
            message=get_notification_message(event_type, report, 'do'),
            report=report,
            notification_type=event_type
        )
        notifications_sent.append(notification)
    
    # Notify reporter's adviser if reporter is a student
    if report.reporter and report.reporter.role == 'student':
        adviser = get_student_adviser(report.reporter)
        if adviser:
            notification = create_notification(
                user=adviser,
                title=f'Advisee Report - {report.case_id}',
                message=f'Your advisee {report.reporter.get_full_name()} submitted an incident report. Case ID: {report.case_id}',
                report=report,
                notification_type=event_type
            )
            notifications_sent.append(notification)
    
    # Notify based on involved party types
    if hasattr(report, 'involved_parties'):
        for party in report.involved_parties.all():
            if party.party_type == 'student':
                # Notify student
                if party.student:
                    notification = create_notification(
                        user=party.student,
                        title=get_notification_title(event_type, report, 'student'),
                        message=get_notification_message(event_type, report, 'student', party),
                        report=report,
                        notification_type=event_type
                    )
                    notifications_sent.append(notification)
                
                # Notify student's adviser
                if party.adviser:
                    notification = create_notification(
                        user=party.adviser,
                        title=f'Advisee Incident - {report.case_id}',
                        message=f'Your advisee {party.get_display_name()} is involved in an incident. Case ID: {report.case_id}',
                        report=report,
                        notification_type=event_type
                    )
                    notifications_sent.append(notification)
            
            elif party.party_type == 'teacher':
                # For teacher incidents, handle confidentially
                if report.is_confidential:
                    # Only notify Guidance
                    counselors = CustomUser.objects.filter(role='counselor')
                    for counselor in counselors:
                        notification = create_notification(
                            user=counselor,
                            title=f'Confidential Teacher Case - {report.case_id}',
                            message=f'A teacher is involved in a confidential incident. Case ID: {report.case_id}. Please handle with discretion.',
                            report=report,
                            notification_type=event_type
                        )
                        notifications_sent.append(notification)
                else:
                    # Non-confidential teacher case
                    if party.teacher:
                        notification = create_notification(
                            user=party.teacher,
                            title=f'Incident Report - {report.case_id}',
                            message=f'You have been mentioned in an incident report. Case ID: {report.case_id}',
                            report=report,
                            notification_type=event_type
                        )
                        notifications_sent.append(notification)
    
    return notifications_sent


def create_notification(user, title, message, report, notification_type):
    """Create notification and send email"""
    notification = Notification.objects.create(
        user=user,
        title=title,
        message=message,
        report=report,
        notification_type=notification_type
    )
    
    # Always attempt to send email notification
    try:
        email_sent = send_notification_email(user, title, message, report)
        if email_sent:
            notification.email_sent = True
            notification.email_sent_at = timezone.now()
            notification.save()
    except Exception as e:
        print(f"Email notification failed for {user.email}: {e}")
    
    return notification


def get_notification_title(event_type, report, recipient_role):
    """Get notification title based on event type and recipient"""
    titles = {
        'report_submitted': {
            'do': f'New Incident Report - {report.case_id}',
            'student': f'Incident Report - {report.case_id}',
            'teacher': f'Incident Report - {report.case_id}',
            'counselor': f'New Case - {report.case_id}',
        },
        'party_confirmed': {
            'do': f'Party Confirmed - {report.case_id}',
            'student': f'Case Confirmation - {report.case_id}',
            'teacher': f'Case Confirmation - {report.case_id}',
        },
        'do_classified': {
            'student': f'Case Update - {report.case_id}',
            'counselor': f'Case Classified - {report.case_id}',
        },
        'guidance_evaluation': {
            'student': f'Case Evaluation - {report.case_id}',
            'counselor': f'Evaluation Required - {report.case_id}',
        },
        'vrf_assigned': {
            'student': f'VRF Assignment - {report.case_id}',
            'esp_teacher': f'New VRF Case - {report.case_id}',
        },
        'counseling_scheduled': {
            'student': f'Counseling Scheduled - {report.case_id}',
        },
        'session_completed': {
            'student': f'Session Completed - {report.case_id}',
        },
    }
    
    return titles.get(event_type, {}).get(recipient_role, f'Case Update - {report.case_id}')


def get_notification_message(event_type, report, recipient_role, party=None):
    """Get notification message based on event type and recipient"""
    messages = {
        'report_submitted': {
            'do': f'New incident report requires fact-checking. Case ID: {report.case_id}',
            'student': f'You have been mentioned in an incident report. Case ID: {report.case_id}',
            'teacher': f'You have been mentioned in an incident report. Case ID: {report.case_id}',
        },
        'party_confirmed': {
            'student': f'You have been confirmed as involved in case {report.case_id}. The Discipline Office will contact you if needed.',
            'teacher': f'You have been confirmed as involved in case {report.case_id}. Please contact the Discipline Office.',
        },
        'do_classified': {
            'student': f'Your case is being handled by the Discipline Office. Case ID: {report.case_id}',
        },
    }
    
    return messages.get(event_type, {}).get(recipient_role, f'Case {report.case_id} has been updated.')


def get_student_adviser(student):
    """Get adviser for a student"""
    if hasattr(student, 'section') and student.section:
        from .models import TeacherAssignment
        assignments = TeacherAssignment.objects.filter(
            section_name=student.section
        ).first()
        if assignments:
            return assignments.teacher
    return None


def notify_party_confirmed(report, party):
    """Send notifications when DO confirms an involved party"""
    if party.party_type == 'student' and party.student:
        # Notify student
        create_notification(
            user=party.student,
            title=f'Case Confirmation - {report.case_id}',
            message=f'You have been confirmed as involved in case {report.case_id}.',
            report=report,
            notification_type='party_confirmed'
        )
        
        # Notify adviser
        if party.adviser:
            create_notification(
                user=party.adviser,
                title=f'Advisee Case Confirmed - {report.case_id}',
                message=f'Your advisee {party.get_display_name()} has been confirmed in case {report.case_id}.',
                report=report,
                notification_type='party_confirmed'
            )
    
    elif party.party_type == 'teacher' and party.teacher:
        # Notify teacher
        create_notification(
            user=party.teacher,
            title=f'Case Confirmation - {report.case_id}',
            message=f'You have been confirmed as involved in case {report.case_id}. Please contact the Discipline Office.',
            report=report,
            notification_type='party_confirmed'
        )
        
        # Notify Guidance
        counselors = CustomUser.objects.filter(role='counselor')
        for counselor in counselors:
            create_notification(
                user=counselor,
                title=f'Teacher Case Confirmed - {report.case_id}',
                message=f'Teacher {party.get_display_name()} confirmed in case {report.case_id}.',
                report=report,
                notification_type='party_confirmed'
            )


def notify_vrf_assigned(report, vpf_case):
    """Send notifications when VRF is assigned"""
    # Notify all ESP teachers
    esp_teachers = CustomUser.objects.filter(role='esp_teacher')
    for esp in esp_teachers:
        create_notification(
            user=esp,
            title=f'New VRF Case - {report.case_id}',
            message=f'A new Values Reflective Formation case has been assigned. Case ID: {report.case_id}',
            report=report,
            notification_type='vrf_assigned'
        )
    
    # Notify student
    if report.reported_student:
        create_notification(
            user=report.reported_student,
            title=f'VRF Assignment - {report.case_id}',
            message=f'You have been assigned to the Values Reflective Formation program. Case ID: {report.case_id}',
            report=report,
            notification_type='vrf_assigned'
        )
        
        # Notify adviser
        adviser = get_student_adviser(report.reported_student)
        if adviser:
            create_notification(
                user=adviser,
                title=f'Advisee VRF Assignment - {report.case_id}',
                message=f'Your advisee {report.reported_student.get_full_name()} has been assigned to VRF. Case ID: {report.case_id}',
                report=report,
                notification_type='vrf_assigned'
            )
