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

from incidents.models import CustomUser, Curriculum, Track, Grade, Section, IncidentType, LegalReference, TeacherAssignment

def setup_all_data():
    """Run all setup functions"""
    print("\n" + "="*80)
    print("🚀 SETTING UP RENDER DATABASE")
    print("="*80)
    
    # Quick check if data already exists
    existing_violations = IncidentType.objects.count()
    existing_teachers = TeacherAssignment.objects.count()
    existing_users = CustomUser.objects.count()
    
    if existing_violations >= 40 and existing_teachers >= 30 and existing_users >= 40:
        print(f"\n✅ Data already loaded:")
        print(f"   - {existing_violations} violations")
        print(f"   - {existing_teachers} teacher assignments")
        print(f"   - {existing_users} users")
        print("   Skipping data load to speed up deployment...")
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
    
    # Import and run load_teacher_assignments
    print("\n📦 Step 3: Loading teacher assignments...")
    try:
        from load_teacher_assignments import create_teacher_assignments
        create_teacher_assignments()
        print("✅ Teacher assignments loaded successfully")
    except Exception as e:
        print(f"⚠️  Teacher assignments error: {e}")
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
    print(f"   Teacher Assignments: {TeacherAssignment.objects.count()}")
    
    if IncidentType.objects.count() < 47:
        print(f"\n⚠️  WARNING: Expected 47 violations, found {IncidentType.objects.count()}")
        print("   Data may not have loaded correctly!")
    else:
        print(f"\n🎉 SUCCESS: All {IncidentType.objects.count()} violations loaded!")
    
    if TeacherAssignment.objects.count() < 32:
        print(f"⚠️  WARNING: Expected 32 teacher assignments, found {TeacherAssignment.objects.count()}")
    else:
        print(f"🎉 SUCCESS: All {TeacherAssignment.objects.count()} teacher assignments loaded!")
    print()

if __name__ == '__main__':
    setup_all_data()
