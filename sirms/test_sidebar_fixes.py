"""
Test script to verify sidebar view fixes
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sirms_project.settings')
django.setup()

from django.test import RequestFactory
from incidents.models import CustomUser
from incidents import views

def test_views():
    """Test that all sidebar views can be accessed without errors"""
    factory = RequestFactory()
    
    print("Testing Guidance Sidebar Views...")
    print("=" * 50)
    
    # Create test users
    try:
        guidance_user = CustomUser.objects.filter(role='guidance').first()
        esp_teacher_user = CustomUser.objects.filter(role='esp_teacher').first()
        
        if not guidance_user:
            print("❌ No guidance user found. Please crer:
    cher_use esp_teaif not 
           rn
    ture         
   st.")fire  onate