"""
Setup script for Render deployment
Loads all initial data including violations
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sirms_project.settings')
django.setup()

from incidents.models import CustomUser, Curriculum, Track, Grade, Section, IncidentType, LegalReference

def setup_all_data():
    """Run all setup functions"""
    print("\n" + "="*80)
    print("🚀 SETTING UP RENDER DATABASE")
    print("="*80)
    
    # Check if data already exists
    existing_violations = IncidentType.objects.count()
    if existing_violations >= 47:
        print(f"\n✅ Data already loaded ({existing_violations} violations found)")
        print("   Skipping data load...")
        return
    
    # Import and run setup_initial_data
    print("\n📦 Step 1: Loading initial data (curriculums, grades, users)...")
    try:
        from setup_initial_data import main as setup_initial
        setup_initial()
        print("✅ Initial data loaded successfully")
    except Exception as e:
        print(f"⚠️  Initial data error: {e}")
        import traceback
        traceback.print_exc()
    
    # Import and run load_violations
    print("\n📦 Step 2: Loading violations and policies...")
    try:
        from load_violations import main as load_violations
        load_violations()
        print("✅ Violations loaded successfully")
    except Exception as e:
        print(f"⚠️  Violations error: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "="*80)
    print("✅ RENDER DATABASE SETUP COMPLETE!")
    print("="*80)
    
    # Print summary
    print(f"\n📊 Database Summary:")
    print(f"   Users: {CustomUser.objects.count()}")
    print(f"   Curriculums: {Curriculum.objects.count()}")
    print(f"   Violations: {IncidentType.objects.count()}")
    print(f"   Legal References: {LegalReference.objects.count()}")
    
    if IncidentType.objects.count() < 47:
        print(f"\n⚠️  WARNING: Expected 47 violations, found {IncidentType.objects.count()}")
        print("   Data may not have loaded correctly!")
    else:
        print(f"\n🎉 SUCCESS: All {IncidentType.objects.count()} violations loaded!")
    print()

if __name__ == '__main__':
    setup_all_data()
