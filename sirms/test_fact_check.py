#!/usr/bin/env python
"""
Test fact check functionality
"""
import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sirms_project.settings')
django.setup()

from django.test import Client
from incidents.models import CustomUser

def test_fact_check():
    """Test fact check functionality"""
    
    # Create test client
    client = Client()
    
    # Test with DO user
    try:
        do_user = CustomUser.objects.get(email='dmlmhs.do@gmail.com')
        print(f"✅ Found DO user: {do_user.username}")
    except CustomUser.DoesNotExist:
        print("❌ DO user not found")
        return
    
    # Test login
    login_success = client.login(username=do_user.username, password='dmlmhsdo000')
    if login_success:
        print("✅ DO login successful")
    else:
        print("❌ DO login failed")
        return
    
    # Test fact check page
    try:
        response = client.get('/fact-check-reports/')
        print(f"Fact check status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Fact check page works")
        else:
            print(f"❌ Fact check page error: {response.status_code}")
    except Exception as e:
        print(f"❌ Fact check page error: {e}")

if __name__ == '__main__':
    test_fact_check()