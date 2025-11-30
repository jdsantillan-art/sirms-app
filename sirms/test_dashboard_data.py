"""
Quick script to test dashboard data for counselor
Run this to verify the data is being calculated correctly
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sirms.settings')
django.setup()

from incidents.models import IncidentReport, CustomUser

# Find a counselor user
counselors = CustomUser.objects.filter(role='counselor')
if counselors.exists():
    counselor = counselors.first()
    print(f"Testing with counselor: {counselor.username}")
    
    # Test prohibited acts count
    prohibited_acts = IncidentReport.objects.filter(
        incident_type__severity='prohibited'
    ).count()
    print(f"Total Prohibited Acts: {prohibited_acts}")
    
    # Test OSP count
    osp = IncidentReport.objects.filter(
        incident_type__severity='school_policy'
    ).count()
    print(f"Total OSP: {osp}")
    
    if prohibited_acts == 0 and osp == 0:
        print("\n⚠️  WARNING: Both counts are 0!")
        print("This means either:")
        print("1. No incident reports exist in the database")
        print("2. The incident_type__severity field doesn't match 'prohibited' or 'school_policy'")
        
        # Check what severities exist
        from incidents.models import IncidentType
        severities = IncidentType.objects.values_list('severity', flat=True).distinct()
        print(f"\nExisting severity values: {list(severities)}")
        
        # Check total reports
        total_reports = IncidentReport.objects.count()
        print(f"Total incident reports: {total_reports}")
else:
    print("No counselor users found in database")
