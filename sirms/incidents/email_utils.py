"""
Email Notification Utilities for SIRMS
Sends email notifications when web notifications are created
"""
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_notification_email(user, title, message, report=None):
    """
    Send email notification to user
    
    Args:
        user: CustomUser object
        title: Notification title
        message: Notification message
        report: IncidentReport object (optional)
    """
    if not user.email:
        return False
    
    try:
        # Prepare email context
        context = {
            'user': user,
            'title': title,
            'message': message,
            'report': report,
            'site_url': settings.SITE_URL if hasattr(settings, 'SITE_URL') else 'http://localhost:8000',
        }
        
        # Create HTML email
        html_message = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #10b981 0%, #14b8a6 100%); color: white; padding: 20px; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9fafb; padding: 20px; border: 1px solid #e5e7eb; }}
                .message {{ background: white; padding: 15px; border-radius: 8px; margin: 15px 0; border-left: 4px solid #10b981; }}
                .footer {{ background: #f3f4f6; padding: 15px; text-align: center; font-size: 12px; color: #6b7280; border-radius: 0 0 10px 10px; }}
                .button {{ display: inline-block; padding: 12px 24px; background: #10b981; color: white; text-decoration: none; border-radius: 6px; margin: 10px 0; }}
                .report-info {{ background: #eff6ff; padding: 10px; border-radius: 6px; margin: 10px 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h2 style="margin: 0;">🔔 DMLMHS SIRMS Notification</h2>
                </div>
                <div class="content">
                    <h3 style="color: #10b981; margin-top: 0;">Hello, {user.get_full_name()}!</h3>
                    
                    <div class="message">
                        <h4 style="margin-top: 0; color: #1f2937;">{title}</h4>
                        <p style="margin: 0;">{message}</p>
                    </div>
                    
                    {f'''
                    <div class="report-info">
                        <strong>📋 Report Details:</strong><br>
                        Case ID: {report.case_id}<br>
                        Status: {report.get_status_display()}<br>
                        Date: {report.created_at.strftime("%B %d, %Y")}
                    </div>
                    ''' if report else ''}
                    
                    <a href="{context['site_url']}/notifications/" class="button">
                        View in SIRMS Dashboard
                    </a>
                    
                    <p style="margin-top: 20px; font-size: 14px; color: #6b7280;">
                        This is an automated notification from the DMLMHS Student Incident Reporting and Management System.
                    </p>
                </div>
                <div class="footer">
                    <p style="margin: 5px 0;">DMLMHS SIRMS - Student Incident Reporting and Management System</p>
                    <p style="margin: 5px 0;">© 2025 Don Mariano Marcos Memorial State University</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Plain text version
        plain_message = f"""
DMLMHS SIRMS Notification

Hello, {user.get_full_name()}!

{title}

{message}

{f'''
Report Details:
Case ID: {report.case_id}
Status: {report.get_status_display()}
Date: {report.created_at.strftime("%B %d, %Y")}
''' if report else ''}

View in SIRMS Dashboard: {context['site_url']}/notifications/

---
This is an automated notification from the DMLMHS Student Incident Reporting and Management System.
DMLMHS SIRMS © 2025
        """
        
        # Send email
        send_mail(
            subject=f'[SIRMS] {title}',
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=True,  # Don't raise errors if email fails
        )
        
        return True
        
    except Exception as e:
        # Log error but don't break the application
        print(f"Email notification error: {str(e)}")
        return False


def send_bulk_notification_emails(users, title, message, report=None):
    """
    Send email notifications to multiple users
    
    Args:
        users: List of CustomUser objects
        title: Notification title
        message: Notification message
        report: IncidentReport object (optional)
    """
    success_count = 0
    for user in users:
        if send_notification_email(user, title, message, report):
            success_count += 1
    
    return success_count
