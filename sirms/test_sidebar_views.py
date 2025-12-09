"""
Test script to check if sidebar views are working
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sirms_project.settings')
django.setup()

from django.test import RequestFactory
from django.contrib.auth import get_user_model
from incidents.views import case_evaluation, counselor_schedule, vrf_schedule, vrf_cases

User = get_user_model()

def test_views():
    factory = RequestFactory()
    
    # Test 1: Check if guidance user can access case_evaluation
    print("\n=== Testing Guidance Sidebar Views ===")
    try:
        guidance_user = User.objects.filter(role='guidance').first()
        if guidance_user:
            print(f"✓ Found guidance user: {guidance_user.username}")
            
            # Test case_evaluation
            request = factory.get('/case-evaluation/')
            request.user = guidance_user
            response = case_evaluation(request)
            print(f"✓ case_evaluation view: Status {response.status_code}")
            
            # Test counselor_schedule
            request = factory.get('/counselor-schedule/')
            request.user = guidance_user
            response = counselor_schedule(request)
            print(f"✓ counselor_schedule view: Status {response.status_code}")
        else:
            print("✗ No guidance user found")
    except Exception as e:
        print(f"✗ Error testing guidance views: {str(e)}")
        import traceback
        traceback.print_exc()
    
    # Test 2: Check if ESP teacher can access VRF views
    print("\n=== Testing ESP Teacher Sidebar Views ===")
    try:
        esp_user = User.objects.filter(role='esp_teacher').first()
        if esp_user:
            print(f"✓ Found ESP teacher: {esp_user.username}")
            
            # Test vrf_schedule
            request = factory.get('/vrf-schedule/')
            request.user = esp_user
            response = vrf_schedule(request)
            print(f"✓ vrf_schedule view: Status {response.status_code}")
            
            # Test vrf_cases
            request = factory.get('/vrf-cases/')
            request.user = esp_user
            response = vrf_cases(request)
            print(f"✓ vrf_cases view: Status {response.status_code}")
        else:
            print("✗ No ESP teacher found")
    except Exception as e:
        print(f"✗ Error testing ESP teacher views: {str(e)}")
        import traceback
        traceback.print_exc()
    
    print("\n=== Test Complete ===")

if __name__ == '__main__':
    test_views()
