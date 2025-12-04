#!/usr/bin/env python
"""
Debug script to identify 500 errors in SIRMS views
"""
import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sirms_project.settings')
django.setup()

from django.test import RequestFactory, Client
from django.contrib.auth import get_user_model
from incidents.models import CustomUser

def test_views():
    """Test critical views that might be causing 500 errors"""
    
    # Create test client
    client = Client()
    
    # Create test user
    try:
        user = CustomUser.objects.get(email='dmlmhs.guidance@gmail.com')
        print(f"✅ Found guidance user: {user.username}")
    except CustomUser.DoesNotExist:
        print("❌ Guidance user not found")
        return
    
    # Test login
    login_success = client.login(username=user.username, password='dmlmhsguidance000')
    if login_success:
        print("✅ Login successful")
    else:
        print("❌ Login failed")
        return
    
    # Test dashboard
    try:
        response = client.get('/dashboard/')
        print(f"Dashboard status: {response.status_code}")
        if response.status_code == 500:
            print("❌ Dashboard returns 500 error")
        else:
            print("✅ Dashboard works")
    except Exception as e:
        print(f"❌ Dashboard error: {e}")
    
    # Test report incident
    try:
        response = client.get('/report-incident/')
        print(f"Report incident status: {response.status_code}")
        if response.status_code == 500:
            print("❌ Report incident returns 500 error")
        else:
            print("✅ Report incident works")
    except Exception as e:
        print(f"❌ Report incident error: {e}")
    
    # Test analytics dashboard
    try:
        response = client.get('/analytics/')
        print(f"Analytics dashboard status: {response.status_code}")
        if response.status_code == 500:
            print("❌ Analytics dashboard returns 500 error")
        else:
            print("✅ Analytics dashboard works")
    except Exception as e:
        print(f"❌ Analytics dashboard error: {e}")

if __name__ == '__main__':
    test_views()