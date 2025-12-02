"""
Add email notification tracking fields to Notification model
Run this to create the migration
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sirms_project.settings')
django.setup()

from django.core.management import call_command

print("Creating migration for email notification fields...")
call_command('makemigrations', 'incidents', '--name', 'add_email_notification_fields')
print("\nMigration created! Now run:")
print("python manage.py migrate")
