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
    try:
        # Debug logging
        print(f"DEBUG: Callback received - Method: {request.method}")
        print(f"DEBUG: GET params: {request.GET}")
        print(f"DEBUG: Full path: {request.get_full_path()}")
        
        # Get authorization code from callback
        code = request.GET.get('code')
        error = request.GET.get('error')
        
        if error:
            print(f"DEBUG: OAuth error: {error}")
            messages.error(request, f'Google authentication failed: {error}')
            return render(request, 'oauth/no_access.html')
        
        if not code:
            print(f"DEBUG: No authorization code received")
            messages.error(request, 'No authorization code received.')
            return render(request, 'oauth/no_access.html')
    except Exception as e:
        print(f"DEBUG: Error in callback initial processing: {str(e)}")
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
                
                # Provide specific error message based on role
                if existing_user.role == 'student':
                    messages.error(
                        request,
                        f'Authentication failed. Please try again or contact administrator.'
                    )
                elif existing_user.role == 'teacher':
                    # Show expected email format for teacher
                    lastname = (existing_user.last_name or '').lower().replace(' ', '').replace('-', '')
                    first_letter = (existing_user.first_name[0] if existing_user.first_name else '').lower()
                    middle_initial = (existing_user.middle_name[0] if existing_user.middle_name else '').lower()
                    expected_email = f"{lastname}{first_letter}{middle_initial}dmlmhs.teacher@gmail.com"
                    messages.error(
                        request,
                        f'Email format mismatch. As a teacher, your email must be: {expected_email}'
                    )
                else:
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


def test_oauth(request):
    """
    Test endpoint to verify OAuth routing is working
    """
    from django.http import JsonResponse
    return JsonResponse({
        'status': 'ok',
        'message': 'OAuth routing is working',
        'client_id_set': bool(settings.GOOGLE_OAUTH_CLIENT_ID),
        'client_secret_set': bool(settings.GOOGLE_OAUTH_CLIENT_SECRET),
        'redirect_uri': settings.GOOGLE_OAUTH_REDIRECT_URI,
        'site_url': settings.SITE_URL
    })
