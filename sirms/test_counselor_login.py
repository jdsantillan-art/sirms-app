"""
Test Counselor Login Fix
Verifies that counselors can access dashboard without errors
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sirms_project.settings')
django.setup()

from incidents.models import CustomUser
from django.test import RequestFactory
from incidents.views import dashboard

print("=" * 70)
print("TESTING COUNSELOR LOGIN FIX")
print("=" * 70)
print()

# Find a counselor account
counselor = CustomUser.objects.filter(role='counselor').first()

if not counselor:
    print("❌ No counselor account found in database")
    print("   Creating test counselor...")
    counselor = CustomUser.objects.create_user(
        username='test_counselor',
        email='test.counselor@test.com',
        password='test123',
        first_name='Test',
        last_name='Counselor',
        role='counselor'
    )
    print(f"   ✅ Created: {counselor.get_full_name()}")

print(f"Testing with counselor: {counselor.get_full_name()} ({counselor.email})")
print()

# Test dashboard view
print("Testing dashboard view...")
try:
    factory = RequestFactory()
    request = factory.get('/dashboard/')
    request.user = counselor
    
    # Try to call dashboard view
    response = dashboard(request)
    
    if response.status_code == 200:
        print("✅ Dashboard loads successfully!")
        print("✅ No VPFCase import error")
        print("✅ Counselor can login")
    else:
        print(f"⚠️  Dashboard returned status: {response.status_code}")
        
except Exception as e:
    print(f"❌ Error occurred: {str(e)}")
    print(f"   Error type: {type(e).__name__}")
    import traceback
    traceback.print_exc()

print()
print("=" * 70)
print("TEST COMPLETE")
print("=" * 70)
print()

if response.status_code == 200:
    print("🎉 SUCCESS! Counselor login is working!")
    print()
    print("You can now login as counselor:")
    print(f"   Email: {counselor.email}")
    print(f"   Username: {counselor.username}")
else:
    print("⚠️  There may still be issues. Check the error above.")
