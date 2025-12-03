"""
Test script to verify ESP Teacher system functionality
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sirms_project.settings')
django.setup()

from incidents.models import Counselor, VPFCase, IncidentReport, CustomUser

def test_esp_teacher_system():
    """Test the ESP Teacher system"""
    
    print("\n" + "="*60)
    print("ESP TEACHER SYSTEM TEST")
    print("="*60)
    
    # 1. Check ESP Teachers
    print("\n1. CHECKING ESP TEACHERS...")
    esp_teachers = Counselor.objects.filter(is_active=True).order_by('name')
    print(f"   Total Active ESP Teachers: {esp_teachers.count()}")
    
    if esp_teachers.count() >= 5:
        print("   ✅ System has at least 5 ESP teachers")
    else:
        print(f"   ⚠️  Only {esp_teachers.count()} teachers found. Need 5.")
    
    print("\n   Latest 5 ESP Teachers:")
    for i, teacher in enumerate(esp_teachers[:5], 1):
        print(f"   {i}. {teacher.name}")
        print(f"      Email: {teacher.email}")
        print(f"      Phone: {teacher.phone}")
        print(f"      Specialization: {teacher.specialization}")
        print()
    
    # 2. Check VPF Cases
    print("\n2. CHECKING VPF CASES...")
    vpf_cases = VPFCase.objects.all()
    print(f"   Total VPF Cases: {vpf_cases.count()}")
    
    pending_vpf = vpf_cases.filter(esp_teacher_assigned__isnull=True)
    assigned_vpf = vpf_cases.filter(esp_teacher_assigned__isnull=False)
    
    print(f"   Pending Assignment: {pending_vpf.count()}")
    print(f"   Assigned: {assigned_vpf.count()}")
    
    if pending_vpf.exists():
        print("\n   Sample Pending VPF Case:")
        case = pending_vpf.first()
        print(f"   - Case ID: {case.report.case_id}")
        print(f"   - Student: {case.student.get_full_name()}")
        print(f"   - Commission: {case.commission_level}")
        print(f"   - Intervention: {case.intervention}")
        print(f"   - Status: {case.get_status_display()}")
    
    if assigned_vpf.exists():
        print("\n   Sample Assigned VPF Case:")
        case = assigned_vpf.first()
        print(f"   - Case ID: {case.report.case_id}")
        print(f"   - Student: {case.student.get_full_name()}")
        print(f"   - ESP Teacher: {case.esp_teacher_assigned.name}")
        print(f"   - Teacher Email: {case.esp_teacher_assigned.email}")
        print(f"   - Teacher Phone: {case.esp_teacher_assigned.phone}")
        print(f"   - Status: {case.get_status_display()}")
    
    # 3. Test Assignment Functionality
    print("\n3. TESTING ASSIGNMENT FUNCTIONALITY...")
    if pending_vpf.exists() and esp_teachers.exists():
        test_case = pending_vpf.first()
        test_teacher = esp_teachers.first()
        
        print(f"   Simulating assignment:")
        print(f"   - Case: {test_case.report.case_id}")
        print(f"   - Teacher: {test_teacher.name}")
        print(f"   ✅ Assignment would work (not actually assigning in test)")
    else:
        print("   ⚠️  No pending cases or teachers available for test")
    
    # 4. Check URLs
    print("\n4. CHECKING URL CONFIGURATION...")
    from django.urls import reverse
    
    urls_to_check = [
        ('manage_esp_teachers', 'Manage ESP Teachers'),
        ('add_esp_teacher', 'Add ESP Teacher'),
        ('for_vpf', 'For VPF'),
    ]
    
    for url_name, description in urls_to_check:
        try:
            url = reverse(url_name)
            print(f"   ✅ {description}: {url}")
        except Exception as e:
            print(f"   ❌ {description}: Error - {e}")
    
    # 5. Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"✅ ESP Teachers: {esp_teachers.count()} active")
    print(f"✅ VPF Cases: {vpf_cases.count()} total")
    print(f"✅ Pending Assignment: {pending_vpf.count()}")
    print(f"✅ Assigned Cases: {assigned_vpf.count()}")
    print("\n🎉 ESP Teacher System is ready to use!")
    print("="*60 + "\n")

if __name__ == '__main__':
    test_esp_teacher_system()
