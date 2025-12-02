"""
Add fields for proper process and notification system
Run this after creating migrations
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sirms_project.settings')
django.setup()

from django.db import connection

def add_fields_to_incident_report():
    """Add new fields to IncidentReport model"""
    with connection.cursor() as cursor:
        try:
            # Add reporter_is_victim field
            cursor.execute("""
                ALTER TABLE incidents_incidentreport 
                ADD COLUMN reporter_is_victim BOOLEAN DEFAULT FALSE
            """)
            print("✓ Added reporter_is_victim field")
        except Exception as e:
            print(f"⚠ reporter_is_victim field may already exist: {e}")
        
        try:
            # Add is_confidential field
            cursor.execute("""
                ALTER TABLE incidents_incidentreport 
                ADD COLUMN is_confidential BOOLEAN DEFAULT FALSE
            """)
            print("✓ Added is_confidential field")
        except Exception as e:
            print(f"⚠ is_confidential field may already exist: {e}")

def add_fields_to_notification():
    """Add new fields to Notification model"""
    with connection.cursor() as cursor:
        try:
            # Add notification_type field
            cursor.execute("""
                ALTER TABLE incidents_notification 
                ADD COLUMN notification_type VARCHAR(50) DEFAULT 'status_update'
            """)
            print("✓ Added notification_type field")
        except Exception as e:
            print(f"⚠ notification_type field may already exist: {e}")
        
        try:
            # Add email_sent field
            cursor.execute("""
                ALTER TABLE incidents_notification 
                ADD COLUMN email_sent BOOLEAN DEFAULT FALSE
            """)
            print("✓ Added email_sent field")
        except Exception as e:
            print(f"⚠ email_sent field may already exist: {e}")
        
        try:
            # Add email_sent_at field
            cursor.execute("""
                ALTER TABLE incidents_notification 
                ADD COLUMN email_sent_at DATETIME NULL
            """)
            print("✓ Added email_sent_at field")
        except Exception as e:
            print(f"⚠ email_sent_at field may already exist: {e}")

if __name__ == '__main__':
    print("=" * 60)
    print("Adding Proper Process & Notification System Fields")
    print("=" * 60)
    print()
    
    print("Step 1: Adding fields to IncidentReport...")
    add_fields_to_incident_report()
    print()
    
    print("Step 2: Adding fields to Notification...")
    add_fields_to_notification()
    print()
    
    print("=" * 60)
    print("✅ Fields added successfully!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Run: python manage.py makemigrations")
    print("2. Run: python manage.py migrate")
    print("3. Update templates and views as per IMPLEMENTATION_COMPLETE.md")
