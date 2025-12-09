"""
Check specific report evidence and Cloudinary configuration
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sirms_project.settings')
django.setup()

from incidents.models import IncidentReport

def check_report(case_id):
    print("=" * 60)
    print(f"CHECKING REPORT: {case_id}")
    print("=" * 60)
    print()
    
    try:
        report = IncidentReport.objects.get(case_id=case_id)
        
        print(f"Case ID: {report.case_id}")
        print(f"Created: {report.created_at}")
        print(f"Status: {report.status}")
        print()
        
        print("Evidence Information:")
        print("-" * 60)
        
        if report.evidence:
            print(f"✅ Evidence field has value: {report.evidence.name}")
            print(f"Evidence URL: {report.evidence.url}")
            print()
            
            # Check if file exists
            try:
                # Try to get file size (this will fail if file doesn't exist)
                size = report.evidence.size
                print(f"✅ File exists, size: {size} bytes")
            except Exception as e:
                print(f"❌ File does NOT exist: {e}")
                print()
                print("This is an OLD file uploaded before Cloudinary.")
                print("The file was deleted by Render's ephemeral filesystem.")
                print()
                print("SOLUTION:")
                print("1. Edit the report")
                print("2. Re-upload the evidence file")
                print("3. Save the report")
                print("4. New file will be stored in Cloudinary permanently")
        else:
            print("❌ No evidence attached to this report")
        
        print()
        
    except IncidentReport.DoesNotExist:
        print(f"❌ Report {case_id} not found")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print()
    print("=" * 60)
    print("CLOUDINARY CONFIGURATION")
    print("=" * 60)
    
    from django.conf import settings
    
    cloud_name = os.environ.get('CLOUDINARY_CLOUD_NAME', '')
    
    if cloud_name:
        print(f"✅ Cloudinary is ACTIVE")
        print(f"Cloud Name: {cloud_name}")
        print()
        print("NEW uploads will go to Cloudinary.")
        print("OLD uploads (before Cloudinary) are lost.")
    else:
        print("❌ Cloudinary is NOT configured")
        print()
        print("Environment variables missing:")
        print("- CLOUDINARY_CLOUD_NAME")
        print("- CLOUDINARY_API_KEY")
        print("- CLOUDINARY_API_SECRET")
    
    print("=" * 60)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        case_id = sys.argv[1]
    else:
        case_id = '2025-0017'  # Default to the reported case
    
    check_report(case_id)
