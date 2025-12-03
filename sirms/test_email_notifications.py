"""
Test Email Notifications
Run this to verify email notifications are working
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sirms_project.settings')
django.setup()

from incidents.models import CustomUser, Notification, IncidentReport
from django.utils import timezone

print("\n" + "="*70)
print("TESTING EMAIL NOTIFICATIONS")
print("="*70)

# Check if email fields exist
print("\n1. Checking Notification model fields...")
fields = [f.name for f in Notification._meta.get_fields()]
if 'email_sent' in fields and 'email_sent_at' in fields:
    print("   ✅ Email tracking fields exist: email_sent, email_sent_at")
else:
    print("   ❌ Email tracking fields missing!")
    exit(1)

# Check email configuration
from django.conf import settings
print("\n2. Checking email configuration...")
print(f"   EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
print(f"   EMAIL_HOST: {settings.EMAIL_HOST}")
print(f"   DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")

if settings.EMAIL_BACKEND == 'django.core.mail.backends.console.EmailBackend':
    print("   ℹ️  Using console backend (emails will print to console)")
elif settings.EMAIL_BACKEND == 'django.core.mail.backends.smtp.EmailBackend':
    print("   ✅ Using SMTP backend (emails will be sent)")
    if not settings.EMAIL_HOST_USER:
        print("   ⚠️  EMAIL_HOST_USER not configured!")
    if not settings.EMAIL_HOST_PASSWORD:
        print("   ⚠️  EMAIL_HOST_PASSWORD not configured!")

# Get a test user
print("\n3. Finding test user...")
user = CustomUser.objects.filter(email__isnull=False).exclude(email='').first()
if user:
    print(f"   ✅ Test user found: {user.get_full_name()} ({user.email})")
else:
    print("   ❌ No user with email found!")
    exit(1)

# Create test notification
print("\n4. Creating test notification...")
try:
    notification = Notification.objects.create(
        user=user,
        title="🧪 Test Email Notification",
        message="This is a test notification to verify email functionality. If you receive this email, the system is working correctly!",
        notification_type='status_update'
    )
    print(f"   ✅ Notification created: ID {notification.id}")
    
    # Check if email was sent
    notification.refresh_from_db()
    if notification.email_sent:
        print(f"   ✅ Email sent successfully at {notification.email_sent_at}")
    else:
        print(f"   ℹ️  Email not sent (check email configuration)")
    
except Exception as e:
    print(f"   ❌ Error creating notification: {e}")
    exit(1)

print("\n5. Checking recent email notifications...")
recent_emails = Notification.objects.filter(
    email_sent=True
).order_by('-email_sent_at')[:5]

if recent_emails.exists():
    print(f"   ✅ Found {recent_emails.count()} recent email notifications:")
    for notif in recent_emails:
        print(f"      - {notif.user.email}: {notif.title} ({notif.email_sent_at})")
else:
    print("   ℹ️  No email notifications sent yet")

print("\n" + "="*70)
print("TEST COMPLETE")
print("="*70)

if settings.EMAIL_BACKEND == 'django.core.mail.backends.console.EmailBackend':
    print("\n📧 Check console output above for email content")
else:
    print(f"\n📧 Check email inbox for: {user.email}")

print("\nTo enable real email sending:")
print("1. Configure EMAIL_HOST_USER and EMAIL_HOST_PASSWORD")
print("2. Set EMAIL_BACKEND to django.core.mail.backends.smtp.EmailBackend")
print("3. Restart the server")
print("\n")
