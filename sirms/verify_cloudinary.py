"""
Quick script to verify Cloudinary configuration
Run this to check if Cloudinary is properly configured
"""

import os
import sys

def verify_cloudinary():
    print("=" * 60)
    print("CLOUDINARY CONFIGURATION VERIFICATION")
    print("=" * 60)
    print()
    
    # Check if running in production
    is_production = 'RENDER' in os.environ or 'DATABASE_URL' in os.environ
    print(f"Environment: {'PRODUCTION (Render)' if is_production else 'LOCAL'}")
    print()
    
    # Check Cloudinary environment variables
    print("Checking Cloudinary Environment Variables:")
    print("-" * 60)
    
    cloud_name = os.environ.get('CLOUDINARY_CLOUD_NAME', '')
    api_key = os.environ.get('CLOUDINARY_API_KEY', '')
    api_secret = os.environ.get('CLOUDINARY_API_SECRET', '')
    
    if cloud_name:
        print(f"✅ CLOUDINARY_CLOUD_NAME: {cloud_name}")
    else:
        print("❌ CLOUDINARY_CLOUD_NAME: NOT SET")
    
    if api_key:
        print(f"✅ CLOUDINARY_API_KEY: {api_key[:5]}...{api_key[-5:] if len(api_key) > 10 else ''}")
    else:
        print("❌ CLOUDINARY_API_KEY: NOT SET")
    
    if api_secret:
        print(f"✅ CLOUDINARY_API_SECRET: {api_secret[:5]}...{api_secret[-5:] if len(api_secret) > 10 else ''}")
    else:
        print("❌ CLOUDINARY_API_SECRET: NOT SET")
    
    print()
    
    # Check if Cloudinary packages are installed
    print("Checking Cloudinary Packages:")
    print("-" * 60)
    
    try:
        import cloudinary
        print(f"✅ cloudinary: {cloudinary.__version__}")
    except ImportError:
        print("❌ cloudinary: NOT INSTALLED")
    
    try:
        import cloudinary_storage
        print("✅ django-cloudinary-storage: INSTALLED")
    except ImportError:
        print("❌ django-cloudinary-storage: NOT INSTALLED")
    
    print()
    
    # Check Django settings
    print("Checking Django Settings:")
    print("-" * 60)
    
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sirms_project.settings')
        import django
        django.setup()
        
        from django.conf import settings
        
        # Check INSTALLED_APPS
        if 'cloudinary_storage' in settings.INSTALLED_APPS:
            print("✅ cloudinary_storage in INSTALLED_APPS")
        else:
            print("❌ cloudinary_storage NOT in INSTALLED_APPS")
        
        if 'cloudinary' in settings.INSTALLED_APPS:
            print("✅ cloudinary in INSTALLED_APPS")
        else:
            print("❌ cloudinary NOT in INSTALLED_APPS")
        
        # Check DEFAULT_FILE_STORAGE
        storage = getattr(settings, 'DEFAULT_FILE_STORAGE', 'default')
        if 'cloudinary' in storage.lower():
            print(f"✅ DEFAULT_FILE_STORAGE: {storage}")
        else:
            print(f"⚠️  DEFAULT_FILE_STORAGE: {storage}")
            print("   (Cloudinary will only be used if CLOUDINARY_CLOUD_NAME is set)")
        
        # Check CLOUDINARY_STORAGE config
        cloudinary_config = getattr(settings, 'CLOUDINARY_STORAGE', {})
        if cloudinary_config:
            print(f"✅ CLOUDINARY_STORAGE configured")
        else:
            print("❌ CLOUDINARY_STORAGE not configured")
        
    except Exception as e:
        print(f"❌ Error checking Django settings: {e}")
    
    print()
    
    # Overall status
    print("=" * 60)
    print("OVERALL STATUS")
    print("=" * 60)
    
    all_set = cloud_name and api_key and api_secret
    
    if all_set:
        print("✅ Cloudinary is FULLY CONFIGURED and ACTIVE")
        print()
        print("Next steps:")
        print("1. Upload a test image in SIRMS")
        print("2. Check Cloudinary dashboard: https://cloudinary.com/console")
        print("3. Verify image URL starts with: https://res.cloudinary.com/")
    else:
        print("⚠️  Cloudinary is PARTIALLY CONFIGURED")
        print()
        print("Missing:")
        if not cloud_name:
            print("- CLOUDINARY_CLOUD_NAME environment variable")
        if not api_key:
            print("- CLOUDINARY_API_KEY environment variable")
        if not api_secret:
            print("- CLOUDINARY_API_SECRET environment variable")
        print()
        print("Action required:")
        print("1. Add missing environment variables in Render dashboard")
        print("2. Restart the service")
        print("3. Run this script again")
    
    print("=" * 60)

if __name__ == '__main__':
    verify_cloudinary()
