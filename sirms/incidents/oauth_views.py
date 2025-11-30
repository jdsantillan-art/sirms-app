"""
Google OAuth Views for SIRMS
Handles OAuth login flow and callbacks
"""

from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib import messages
from django.conf import settings
from .google_auth import (
    GoogleOAuthBackend, 
    get_google_auth_url, 
    exchange_code_for_token
)
from google.oauth2 import id_token
from google.auth.transport import requests


def google_login(request):
    """
    Initiate Google OAuth login
    Redirects directly to Google's authorization page
    """
    # If user is already logged in, redirect to dashboard
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    # Generate Google OAuth URL and redirect directly
    auth_url = get_google_auth_url()
    return redirect(auth_url)


def google_callback(request):
    """
    Handle Google OAuth callback
    Validates user and creates session
    """
    # Get authorization code from callback
    code = request.GET.get('code')
    error = request.GET.get('error')
    
    if error:
        messages.error(request, f'Google authentication failed: {error}')
        return render(request, 'oauth/no_access.html')
    
    if not code:
        messages.error(request, 'No authorization code received.')
        return render(request, 'oauth/no_access.html')
    
    # Exchange code for tokens
    token_data = exchange_code_for_token(code)
    
    if not token_data or 'id_token' not in token_data:
        messages.error(request, 'Failed to obtain access token.')
        return render(request, 'oauth/no_access.html')
    
    # Verify and decode ID token
    try:
        idinfo = id_token.verify_oauth2_token(
            token_data['id_token'],
            requests.Request(),
            settings.GOOGLE_OAUTH_CLIENT_ID
        )
        
        email = idinfo.get('email')
        name = idinfo.get('name', '')
        
        print(f"DEBUG: Email from Google: {email}")  # Debug log
        
        if not email:
            messages.error(request, 'Could not retrieve email from Google.')
            return render(request, 'oauth/no_access.html')
        
        # Authenticate user using custom backend
        backend = GoogleOAuthBackend()
        user = backend.authenticate(request, token=token_data['id_token'])
        
        print(f"DEBUG: User authenticated: {user}")  # Debug log
        
        if user:
            # User is registered and email format is valid
            # Login the user manually
            from django.contrib.auth import login as django_login
            django_login(request, user, backend='incidents.google_auth.GoogleOAuthBackend')
            
            # Store additional info in session
            request.session['google_email'] = email
            request.session['google_name'] = name
            request.session.save()
            
            print(f"DEBUG: User logged in successfully: {user.username}")  # Debug log
            
            messages.success(request, f'Welcome back, {user.get_full_name() or name}!')
            
            # Redirect to appropriate dashboard based on role
            return redirect('dashboard')
        else:
            # Check if email exists but format is wrong
            from .models import CustomUser
            try:
                existing_user = CustomUser.objects.get(email=email)
                print(f"DEBUG: User exists but auth failed. Role: {existing_user.role}")  # Debug log
                messages.error(
                    request,
                    f'Email format mismatch. Your email ({email}) should follow the format: '
                    f'lastname.dmlmhs{existing_user.role}@gmail.com'
                )
            except CustomUser.DoesNotExist:
                print(f"DEBUG: User does not exist: {email}")  # Debug log
                messages.error(
                    request,
                    f'Email not registered: {email}. Access denied. Please contact the administrator.'
                )
            
            return render(request, 'oauth/no_access.html')
            
    except ValueError as e:
        print(f"DEBUG: ValueError: {str(e)}")  # Debug log
        messages.error(request, f'Invalid token: {str(e)}')
        return render(request, 'oauth/no_access.html')
    except Exception as e:
        print(f"DEBUG: Exception: {str(e)}")  # Debug log
        messages.error(request, f'Authentication error: {str(e)}')
        return render(request, 'oauth/no_access.html')


def google_logout(request):
    """
    Logout user and clear session
    """
    auth_logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('google_login')


def no_access(request):
    """
    Display access denied page for unauthorized users
    """
    return render(request, 'oauth/no_access.html')
