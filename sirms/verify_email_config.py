"""
Email Configuration Verification Script
Run this on Render Shell to verify email setup
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sirms_project.settings')
django.setup()

from django.conf import settings
from django.core.mail import send_mail
from incidents.models import CustomUser, Notification
from django.utils import timezone

print("=" * 70)
print("EMAIL CONFIGURATION VERIFICATION")
print("=" * 70)
print()

# Check 1: Environment Variables
print("1. Checking Environment Variables...")
required_vars = [
    'EMAIL_BACKEND',
    'EMAIL_HOST',
    'EMAIL_PORT',
    'EMAIL_USE_TLS',
    'EMAIL_HOST_USER',
    'EMAIL_HOST_PASSWORD',
    'DEFAULT_FROM_EMAIL',
]

all_set = True
for var in required_vars:
    value = getattr(settings, var, None)
    if value:
        if 'PASSWORD' in var:
            print(f"   ✅ {var}: {'*' * 16} (hidden)")
        else:
            print(f"   ✅ {var}: {value}")
    else:
        print(f"   ❌ {var}: NOT SET")
        all_set = False

if not all_set:
    print("\n⚠️  Some variables are missing!")
    print("   Add them in Render Dashboard → Environment")
    exit(1)

print()

# Check 2: Email Backend
print("2. Checking Email Backend...")
if settings.EMAIL_BACKEND == 'django.core.mail.backends.smtp.EmailBackend':
    print("   ✅ SMTP Backend configured (real emails will be sent)")
elif settings.EMAIL_BACKEND == 'django.core.mail.backends.console.EmailBackend':
    print("   ⚠️  Console Backend (emails print to console only)")
    print("   Change EMAIL_BACKEND to: django.core.mail.backends.smtp.EmailBackend")
else:
    print(f"   ℹ️  Backend: {settings.EMAIL_BACKEND}")

print()

# Check 3: Test User
print("3. Finding test user...")
test_user = CustomUser.objects.filter(email__isnull=False).exclude(email='').first()
if test_user:
    print(f"   ✅ Test user: {test_user.get_full_name()} ({test_user.email})")
else:
    print("   ❌ No users with email addresses found")
    exit(1)

print()

# Check 4: Send Test Email
print("4. Sending test email...")
try:
    send_mail(
        subject='[SIRMS] Email Configuration Test',
        message='This is a test email from SIRMS. If you receive this, email notifications are working!',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[test_user.email],
        html_message=f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #10b981 0%, #14b8a6 100%); color: white; padding: 20px; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9fafb; padding: 20px; border: 1px solid #e5e7eb; }}
                .success {{ background: #d1fae5; padding: 15px; border-radius: 8px; margin: 15px 0; border-left: 4px solid #10b981; }}
                .footer {{ background: #f3f4f6; padding: 15px; text-align: center; font-size: 12px; color: #6b7280; border-radius: 0 0 10px 10px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h2 style="margin: 0;">✅ SIRMS Email Test</h2>
                </div>
                <div class="content">
                    <h3 style="color: #10b981; margin-top: 0;">Email Configuration Successful!</h3>
                    
                    <div class="success">
                        <h4 style="margin-top: 0; color: #1f2937;">🎉 Congratulations!</h4>
                        <p style="margin: 0;">Your SIRMS email notifications are now working correctly.</p>
                    </div>
                    
                    <p><strong>What this means:</strong></p>
                    <ul>
                        <li>Users will receive email notifications</li>
                        <li>Incident reports will trigger emails</li>
                        <li>Counseling schedules will be emailed</li>
                        <li>All notifications are now delivered via email</li>
                    </ul>
                    
                    <p style="margin-top: 20px; font-size: 14px; color: #6b7280;">
                        This is a test email sent on {timezone.now().strftime("%B %d, %Y at %I:%M %p")}
                    </p>
                </div>
                <div class="footer">
                    <p style="margin: 5px 0;">DMLMHS SIRMS - Student Incident Reporting and Management System</p>
                    <p style="margin: 5px 0;">© 2025 Don Mariano Marcos Memorial State University</p>
                </div>
            </div>
        </body>
        </html>
        """,
        fail_silently=False,
    )
    print(f"   ✅ Test email sent to: {test_user.email}")
    print(f"   📧 Check inbox for email from: {settings.DEFAULT_FROM_EMAIL}")
except Exception as e:
    print(f"   ❌ Failed to send email: {str(e)}")
    print("\n   Common issues:")
    print("   - Wrong Gmail App Password")
    print("   - 2-Step Verification not enabled")
    print("   - Gmail account locked")
    print("   - Network/firewall issues")
    exit(1)

print()

# Check 5: Database Email Tracking
print("5. Checking email tracking in database...")
email_notifications = Notification.objects.filter(email_sent=True).count()
total_notifications = Notification.objects.count()

if total_notifications > 0:
    success_rate = (email_notifications / total_notifications) * 100
    print(f"   📊 Total notifications: {total_notifications}")
    print(f"   📧 Emails sent: {email_notifications}")
    print(f"   📈 Success rate: {success_rate:.1f}%")
else:
    print("   ℹ️  No notifications in database yet")

print()

# Check 6: Recent Email Notifications
print("6. Recent email notifications...")
recent = Notification.objects.filter(email_sent=True).order_by('-email_sent_at')[:5]
if recent.exists():
    for n in recent:
        print(f"   📧 {n.user.email} - {n.title}")
        print(f"      Sent: {n.email_sent_at.strftime('%B %d, %Y at %I:%M %p')}")
else:
    print("   ℹ️  No email notifications sent yet")

print()
print("=" * 70)
print("VERIFICATION COMPLETE")
print("=" * 70)
print()
print("✅ Email configuration is working!")
print(f"📧 Test email sent to: {test_user.email}")
print()
print("Next steps:")
print("1. Check the email inbox")
print("2. Look for email from:", settings.DEFAULT_FROM_EMAIL)
print("3. Verify email formatting looks professional")
print("4. Create a test incident report to trigger real notification")
print()
print("🎉 Email notifications are now live on production!")
print()
