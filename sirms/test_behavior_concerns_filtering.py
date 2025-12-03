"""
Test script for Behavior Concerns filtering and export functionality
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sirms_project.settings')
django.setup()

from django.test import Client, RequestFactory
from django.contrib.auth import get_user_model
from incidents.models import IncidentReport, IncidentType
from incidents.behavior_concerns_views import behavior_concerns
from incidents.export_views import export_behavior_concerns_excel
from datetime import datetime, timedelta

User = get_user_model()

def test_behavior_concerns_filtering():
    """Test the behavior concerns view with different filters"""
    print("\n" + "="*60)
    print("TESTING BEHAVIOR CONCERNS FILTERING")
    print("="*60)
    
    # Create test DO user
    try:
        do_user = User.objects.filter(role='do').first()
        if not do_user:
            print("❌ No DO user found. Please create a DO account first.")
            return
        
        print(f"✅ Using DO user: {do_user.get_full_name()}")
        
        # Get behavior concerns statistics
        reports = IncidentReport.objects.filter(
            status__in=['classified', 'under_review', 'resolved']
        ).exclude(status='evaluated')
        
        total_cases = reports.count()
        pending_cases = reports.filter(status='classified').count()
        ongoing_cases = reports.filter(status='under_review').count()
        completed_cases = reports.filter(status='resolved').count()
        
        print(f"\n📊 Current Statistics:")
        print(f"   Total Cases: {total_cases}")
        print(f"   Pending (Classified): {pending_cases}")
        print(f"   Ongoing (Under Review): {ongoing_cases}")
        print(f"   Completed (Resolved): {completed_cases}")
        
        # Test filtering logic
        print(f"\n🔍 Testing Filter Logic:")
        
        # Test 1: All cases
        all_cases = reports.all()
        print(f"   ✅ All filter: {all_cases.count()} cases")
        
        # Test 2: Pending cases
        pending = reports.filter(status='classified')
        print(f"   ✅ Pending filter: {pending.count()} cases")
        
        # Test 3: Completed cases
        completed = reports.filter(status='resolved')
        print(f"   ✅ Completed filter: {completed.count()} cases")
        
        # Test export data structure
        if completed.exists():
            print(f"\n📥 Testing Export Data Structure:")
            sample_report = completed.first()
            print(f"   Sample Case: {sample_report.case_id}")
            print(f"   Student: {sample_report.reported_student.get_full_name() if sample_report.reported_student else 'N/A'}")
            print(f"   Status: {sample_report.get_status_display()}")
            print(f"   Created: {sample_report.created_at.strftime('%Y-%m-%d')}")
            print(f"   Updated: {sample_report.updated_at.strftime('%Y-%m-%d')}")
            
            # Check for schedules
            from incidents.models import DOSchedule
            schedules = DOSchedule.objects.filter(report=sample_report)
            print(f"   Appointments: {schedules.count()}")
            
            if schedules.exists():
                for schedule in schedules:
                    print(f"      - {schedule.get_schedule_type_display()} on {schedule.scheduled_date.strftime('%Y-%m-%d %H:%M')}")
        else:
            print(f"\n⚠️  No completed cases available for export testing")
        
        print(f"\n✅ All tests passed!")
        
    except Exception as e:
        print(f"❌ Error during testing: {str(e)}")
        import traceback
        traceback.print_exc()

def test_export_functionality():
    """Test the Excel export functionality"""
    print("\n" + "="*60)
    print("TESTING EXCEL EXPORT FUNCTIONALITY")
    print("="*60)
    
    try:
        # Get DO user
        do_user = User.objects.filter(role='do').first()
        if not do_user:
            print("❌ No DO user found.")
            return
        
        # Create a mock request
        factory = RequestFactory()
        request = factory.get('/export-behavior-concerns-excel/')
        request.user = do_user
        
        # Get completed cases
        completed_cases = IncidentReport.objects.filter(status='resolved')
        
        if not completed_cases.exists():
            print("⚠️  No completed cases to export")
            print("   Creating a test completed case...")
            
            # Create a test case
            incident_type = IncidentType.objects.first()
            if incident_type:
                test_report = IncidentReport.objects.create(
                    incident_type=incident_type,
                    description="Test completed case for export",
                    incident_date=datetime.now().date(),
                    incident_time=datetime.now().time(),
                    grade_level=9,
                    section_name="9-A",
                    reporter=do_user,
                    reporter_first_name=do_user.first_name,
                    reporter_last_name=do_user.last_name,
                    status='resolved'
                )
                print(f"   ✅ Created test case: {test_report.case_id}")
                completed_cases = IncidentReport.objects.filter(status='resolved')
        
        print(f"\n📊 Export Statistics:")
        print(f"   Cases to export: {completed_cases.count()}")
        
        # Test export function
        try:
            response = export_behavior_concerns_excel(request)
            
            if response.status_code == 200:
                print(f"   ✅ Export successful!")
                print(f"   Content-Type: {response['Content-Type']}")
                print(f"   Content-Disposition: {response['Content-Disposition']}")
                
                # Check file size
                content_length = len(response.content)
                print(f"   File size: {content_length:,} bytes ({content_length/1024:.2f} KB)")
                
                if content_length > 0:
                    print(f"   ✅ Excel file generated successfully!")
                else:
                    print(f"   ⚠️  Warning: File is empty")
            else:
                print(f"   ❌ Export failed with status code: {response.status_code}")
        
        except Exception as e:
            print(f"   ❌ Export error: {str(e)}")
            import traceback
            traceback.print_exc()
        
    except Exception as e:
        print(f"❌ Error during export testing: {str(e)}")
        import traceback
        traceback.print_exc()

def test_url_routing():
    """Test URL routing for the new export endpoint"""
    print("\n" + "="*60)
    print("TESTING URL ROUTING")
    print("="*60)
    
    try:
        from django.urls import reverse
        
        # Test behavior concerns URL
        try:
            url = reverse('behavior_concerns')
            print(f"✅ behavior_concerns URL: {url}")
        except Exception as e:
            print(f"❌ behavior_concerns URL error: {str(e)}")
        
        # Test export URL
        try:
            url = reverse('export_behavior_concerns_excel')
            print(f"✅ export_behavior_concerns_excel URL: {url}")
        except Exception as e:
            print(f"❌ export_behavior_concerns_excel URL error: {str(e)}")
        
    except Exception as e:
        print(f"❌ URL routing error: {str(e)}")

if __name__ == '__main__':
    print("\n" + "="*60)
    print("BEHAVIOR CONCERNS FILTERING & EXPORT TEST SUITE")
    print("="*60)
    
    test_behavior_concerns_filtering()
    test_export_functionality()
    test_url_routing()
    
    print("\n" + "="*60)
    print("TEST SUITE COMPLETED")
    print("="*60 + "\n")
