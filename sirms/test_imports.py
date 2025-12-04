#!/usr/bin/env python
"""
Test imports to identify issues
"""
import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sirms_project.settings')
django.setup()

print("Testing imports...")

try:
    from incidents import views
    print("✅ Main views imported successfully")
except Exception as e:
    print(f"❌ Main views import error: {e}")

try:
    from incidents import oauth_views
    print("✅ OAuth views imported successfully")
except Exception as e:
    print(f"❌ OAuth views import error: {e}")

try:
    from incidents import direct_report_views
    print("✅ Direct report views imported successfully")
except Exception as e:
    print(f"❌ Direct report views import error: {e}")

try:
    from incidents import export_views
    print("✅ Export views imported successfully")
except Exception as e:
    print(f"❌ Export views import error: {e}")

try:
    from incidents import completed_sessions_views
    print("✅ Completed sessions views imported successfully")
except Exception as e:
    print(f"❌ Completed sessions views import error: {e}")

try:
    from incidents import completed_reports_views
    print("✅ Completed reports views imported successfully")
except Exception as e:
    print(f"❌ Completed reports views import error: {e}")

try:
    from incidents import incident_type_views
    print("✅ Incident type views imported successfully")
except Exception as e:
    print(f"❌ Incident type views import error: {e}")

try:
    from incidents import do_schedule_views
    print("✅ DO schedule views imported successfully")
except Exception as e:
    print(f"❌ DO schedule views import error: {e}")

try:
    from incidents import behavior_concerns_views
    print("✅ Behavior concerns views imported successfully")
except Exception as e:
    print(f"❌ Behavior concerns views import error: {e}")

try:
    from incidents import esp_teacher_views
    print("✅ ESP teacher views imported successfully")
except Exception as e:
    print(f"❌ ESP teacher views import error: {e}")

print("\nTesting specific functions...")

try:
    from incidents.views import dashboard
    print("✅ Dashboard function exists")
except Exception as e:
    print(f"❌ Dashboard function error: {e}")

try:
    from incidents.views import report_incident
    print("✅ Report incident function exists")
except Exception as e:
    print(f"❌ Report incident function error: {e}")

try:
    from incidents.views import analytics_dashboard
    print("✅ Analytics dashboard function exists")
except Exception as e:
    print(f"❌ Analytics dashboard function error: {e}")