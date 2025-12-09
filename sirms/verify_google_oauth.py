#!/usr/bin/env python
"""
Google OAuth Configuration Verification Script
Run this to check your Google OAuth setup
"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sirms_project.settings')
django.setup()

from django.conf import settings

def verify_oauth_config():
    """Verify Google OAuth configuration"""
    print("=" * 60)
    print("GOOGLE OAUTH CONFIGURATION VERIFICATION")
    print("=" * 60)
    print()
    
    # Check Client ID
    client_id = settings.GOOGLE_OAUTH_CLIENT_ID
    if client_id:
        print(f"✓ GOOGLE_OAUTH_CLIENT_ID: {client_id[:20]}...{client_id[-10:]}")
    else:
        print("✗ GOOGLE_OAUTH_CLIENT_ID: NOT SET")
        print("  → Set this in Render environment variables")
    print()
    
    # Check Client Secret
    client_secret = settings.GOOGLE_OAUTH_CLIENT_SECRET
    if client_secret:
        print(f"✓ GOOGLE_OAUTH_CLIENT_SECRET: {client_secret[:10]}...{client_secret[-5:]}")
    else:
        print("✗ GOOGLE_OAUTH_CLIENT_SECRET: NOT SET")
        print("  → Set this in Render environment variables")
    print()
    
    # Check Site URL
    site_url = settings.SITE_URL
    print(f"✓ SITE_URL: {site_url}")
    print()
    
    # Check Redirect URI
    redirect_uri = settings.GOOGLE_OAUTH_REDIRECT_URI
    print(f"✓ GOOGLE_OAUTH_REDIRECT_URI: {redirect_uri}")
    print()
    
    # Validation
    print("=" * 60)
    print("VALIDATION CHECKS")
    print("=" * 60)
    print()
    
    issues = []
    
    if not client_id:
        issues.append("Missing GOOGLE_OAUTH_CLIENT_ID")
    
    if not client_secret:
        issues.append("Missing GOOGLE_OAUTH_CLIENT_SECRET")
    
    if not redirect_uri.endswith('/'):
        issues.append(f"Redirect URI missing trailing slash: {redirect_uri}")
        print(f"✗ Redirect URI should end with /")
        print(f"  Current: {redirect_uri}")
        print(f"  Should be: {redirect_uri}/")
        print()
    else:
        print(f"✓ Redirect URI has trailing slash")
        print()
    
    if 'localhost' in redirect_uri and 'http://' not in redirect_uri:
        issues.append("Localhost should use http:// not https://")
    
    if 'onrender.com' in redirect_uri and 'https://' not in redirect_uri:
        issues.append("Render should use https:// not http://")
    
    # Summary
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print()
    
    if issues:
        print(f"✗ Found {len(issues)} issue(s):")
        for i, issue in enumerate(issues, 1):
            print(f"  {i}. {issue}")
        print()
        print("Fix these issues and try again.")
    else:
        print("✓ All checks passed!")
        print()
        print("Next steps:")
        print("1. Go to Google Cloud Console")
        print("2. Navigate to APIs & Services → Credentials")
        print("3. Add this redirect URI:")
        print(f"   {redirect_uri}")
        print()
        print("4. Wait 5-10 minutes for changes to propagate")
        print("5. Try logging in again")
    
    print()
    print("=" * 60)
    print("OAUTH URLS")
    print("=" * 60)
    print()
    print(f"Login URL: {site_url}/auth/google/")
    print(f"Callback URL: {redirect_uri}")
    print(f"Logout URL: {site_url}/auth/logout/")
    print()

if __name__ == '__main__':
    verify_oauth_config()
