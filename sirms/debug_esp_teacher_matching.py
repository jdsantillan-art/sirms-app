"""
Debug script to check ESP Teacher matching
Run: python debug_esp_teacher_matching.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sirms_project.settings')
django.setup()

from incidents.models import CustomUser, Counselor, VPFCase
from django.db.models import Q

def debug_esp_teacher_matching():
    """Debug ESP teacher to Counselor matching"""
    
    print("\n" + "="*60)
    print("ESP TEACHER MATCHING DEBUG")
    print("="*60)
    
    # Get all ESP teacher users
    esp_teachers = CustomUser.objects.filter(role='esp_teacher')
    print(f"\n1. ESP Teacher User Accounts: {esp_teachers.count()}")
    
    for user in esp_teachers:
        print(f"\n   User: {user.username}")
        print(f"   - Full Name: {user.get_full_name()}")
        print(f"   - Email: {user.email}")
        
        # Try to find matching Counselor
        matching_counselors = Counselor.objects.filter(
            Q(email__iexact=user.email) |
            Q(name__icontains=user.get_full_name())
        ).filter(is_active=True)
        
        if matching_counselors.exists():
            print(f"   ✅ MATCHED to Counselor(s):")
            for counselor in matching_counselors:
                print(f"      - {counselor.name} ({counselor.email})")
                
                # Check VPF cases
                vpf_cases = VPFCase.objects.filter(esp_teacher_assigned=counselor)
                print(f"      - VPF Cases: {vpf_cases.count()}")
                for case in vpf_cases:
                    print(f"        • {case.report.case_id} - {case.student.get_full_name()} ({case.status})")
        else:
            print(f"   ❌ NO MATCH FOUND")
            print(f"   Suggestion: Create Counselor with:")
            print(f"      - Name: {user.get_full_name()}")
            print(f"      - Email: {user.email}")
    
    # Get all Counselors
    print(f"\n2. Counselor Records (ESP Teachers): {Counselor.objects.filter(is_active=True).count()}")
    
    for counselor in Counselor.objects.filter(is_active=True):
        print(f"\n   Counselor: {counselor.name}")
        print(f"   - Email: {counselor.email}")
        print(f"   - Phone: {counselor.phone}")
        print(f"   - Specialization: {counselor.specialization}")
        
        # Check if user account exists
        matching_users = CustomUser.objects.filter(
            Q(email__iexact=counselor.email) |
            Q(first_name__icontains=counselor.name.split()[0]) &
            Q(last_name__icontains=counselor.name.split()[-1])
        ).filter(role='esp_teacher')
        
        if matching_users.exists():
            print(f"   ✅ MATCHED to User(s):")
            for user in matching_users:
                print(f"      - {user.username} ({user.get_full_name()})")
        else:
            print(f"   ❌ NO USER ACCOUNT FOUND")
            print(f"   Suggestion: Create user with:")
            print(f"      - Email: {counselor.email}")
            print(f"      - Name matching: {counselor.name}")
        
        # Check VPF cases
        vpf_cases = VPFCase.objects.filter(esp_teacher_assigned=counselor)
        print(f"   - VPF Cases Assigned: {vpf_cases.count()}")
        for case in vpf_cases:
            print(f"     • {case.report.case_id} - {case.student.get_full_name()} ({case.status})")
    
    # Get all VPF cases
    print(f"\n3. VPF Cases: {VPFCase.objects.count()}")
    
    for vpf in VPFCase.objects.all():
        print(f"\n   Case: {vpf.report.case_id}")
        print(f"   - Student: {vpf.student.get_full_name()}")
        print(f"   - Status: {vpf.status}")
        if vpf.esp_teacher_assigned:
            print(f"   - ESP Teacher: {vpf.esp_teacher_assigned.name}")
            print(f"   - ESP Email: {vpf.esp_teacher_assigned.email}")
        else:
            print(f"   - ESP Teacher: NOT ASSIGNED")
    
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"ESP Teacher Users: {esp_teachers.count()}")
    print(f"Counselor Records: {Counselor.objects.filter(is_active=True).count()}")
    print(f"VPF Cases: {VPFCase.objects.count()}")
    print(f"Assigned VPF Cases: {VPFCase.objects.filter(esp_teacher_assigned__isnull=False).count()}")
    print(f"Unassigned VPF Cases: {VPFCase.objects.filter(esp_teacher_assigned__isnull=True).count()}")
    print("="*60 + "\n")

if __name__ == '__main__':
    debug_esp_teacher_matching()
