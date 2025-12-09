"""
Google OAuth Authentication Backend for SIRMS
Handles Google OAuth 2.0 authentication with email validation
"""

from google.oauth2 import id_token
from google.auth.transport import requests
from django.conf import settings
from django.contrib.auth import get_user_model
import requests as http_requests

User = get_user_model()


class GoogleOAuthBackend:
    """
    Custom authentication backend for Google OAuth
    Only allows registered emails with DMLMHS format
    """
    
    def authenticate(self, request, token=None):
        """
        Authenticate user with Google OAuth token
        
        Args:
            request: Django request object
            token: Google OAuth ID token
            
        Returns:
            User object if authenticated, None otherwise
        """
        if not token:
            print("DEBUG AUTH: No token provided")
            return None
        
        try:
            # Verify the token with Google
            idinfo = id_token.verify_oauth2_token(
                token, 
                requests.Request(), 
                settings.GOOGLE_OAUTH_CLIENT_ID
            )
            
            # Get email from token
            email = idinfo.get('email')
            print(f"DEBUG AUTH: Email from Google token: {email}")
            
            if not email:
                print("DEBUG AUTH: No email in token")
                return None
            
            # Check if email is registered in database
            try:
                user = User.objects.get(email=email)
                print(f"DEBUG AUTH: User found in database: {user.username}, role: {user.role}")
                
                # Validate email format matches role (pass user object for teacher validation)
                is_valid = self.validate_email_format(email, user.role, user=user)
                print(f"DEBUG AUTH: Email format valid: {is_valid}")
                
                if is_valid:
                    print(f"DEBUG AUTH: Authentication successful for {email}")
                    return user
                else:
                    print(f"DEBUG AUTH: Email format validation failed for {email}")
                    # For teachers, show expected format
                    if user.role == 'teacher':
                        lastname = (user.last_name or '').lower().replace(' ', '').replace('-', '')
                        first_letter = (user.first_name[0] if user.first_name else '').lower()
                        middle_initial = (user.middle_name[0] if user.middle_name else '').lower()
                        expected_email = f"{lastname}{first_letter}{middle_initial}dmlmhs.teacher@gmail.com"
                        print(f"DEBUG AUTH: Expected email format for teacher: {expected_email}")
                    return None
                    
            except User.DoesNotExist:
                # Email not registered in database
                print(f"DEBUG AUTH: User not found in database: {email}")
                return None
                
        except ValueError as e:
            # Invalid token
            print(f"DEBUG AUTH: Invalid token: {e}")
            return None
        except Exception as e:
            print(f"DEBUG AUTH: Exception: {e}")
            return None
    
    def validate_email_format(self, email, role, user=None):
        """
        Validate that email format matches the user's role
        
        For students: Allow any email (no restriction)
        For teachers: Format must be: lastname + first_letter + middle_initial + dmlmhs.teacher@gmail.com
        Example: santillanjddmlmhs.teacher@gmail.com
        
        Args:
            email: Email address to validate
            role: User role from database
            user: User object (optional, needed for teacher validation)
            
        Returns:
            Boolean indicating if email format is valid
        """
        # Students can use any email - no restriction
        if role == 'student':
            return True
        
        # For teachers, validate specific format
        if role == 'teacher':
            if not email.endswith('dmlmhs.teacher@gmail.com'):
                return False
            
            # If user object is provided, validate against their name
            if user:
                # Get name components
                lastname = (user.last_name or '').lower().replace(' ', '').replace('-', '')
                first_letter = (user.first_name[0] if user.first_name else '').lower()
                middle_initial = (user.middle_name[0] if user.middle_name else '').lower()
                
                # Construct expected email pattern
                expected_local = f"{lastname}{first_letter}{middle_initial}dmlmhs.teacher"
                email_local = email.split('@')[0].lower()
                
                return email_local == expected_local
            else:
                # If no user object, just check the pattern exists
                email_local = email.split('@')[0].lower()
                return 'dmlmhs.teacher' in email_local
        
        # For other roles, use existing validation
        if not email.endswith(settings.DMLMHS_EMAIL_DOMAIN):
            return False
        
        # Map database roles to email patterns
        role_mapping = {
            'counselor': 'dmlmhsguidance',
            'guidance': 'dmlmhsguidance',
            'do': 'dmlmhsdo',
            'principal': 'dmlmhsprincipal',
        }
        
        expected_pattern = role_mapping.get(role)
        if not expected_pattern:
            return False
        
        # Check if email contains the expected pattern
        email_local = email.split('@')[0]  # Get part before @
        return expected_pattern in email_local.lower()
    
    def get_user(self, user_id):
        """
        Get user by ID for session management
        
        Args:
            user_id: User ID
            
        Returns:
            User object or None
        """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


def get_google_auth_url():
    """
    Generate Google OAuth authorization URL
    
    Returns:
        Google OAuth URL for user authorization
    """
    base_url = "https://accounts.google.com/o/oauth2/v2/auth"
    from urllib.parse import urlencode
    
    params = {
        'client_id': settings.GOOGLE_OAUTH_CLIENT_ID,
        'redirect_uri': settings.GOOGLE_OAUTH_REDIRECT_URI,
        'response_type': 'code',
        'scope': 'openid email profile',
        'access_type': 'offline',
        'prompt': 'select_account',
    }
    
    query_string = urlencode(params)
    return f"{base_url}?{query_string}"


def exchange_code_for_token(code):
    """
    Exchange authorization code for access token
    
    Args:
        code: Authorization code from Google
        
    Returns:
        Dictionary containing tokens or None
    """
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        'code': code,
        'client_id': settings.GOOGLE_OAUTH_CLIENT_ID,
        'client_secret': settings.GOOGLE_OAUTH_CLIENT_SECRET,
        'redirect_uri': settings.GOOGLE_OAUTH_REDIRECT_URI,
        'grant_type': 'authorization_code',
    }
    
    try:
        response = http_requests.post(token_url, data=data)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error exchanging code for token: {e}")
        return None


def generate_dmlmhs_email(lastname, role):
    """
    Helper function to generate standardized DMLMHS email
    
    Args:
        lastname: User's last name
        role: User role (student, teacher, counselor, do, principal)
        
    Returns:
        Formatted email address
        
    Example:
        generate_dmlmhs_email('Santillan', 'student')
        Returns: 'santillan.dmlmhsstudent@gmail.com'
    """
    role_patterns = {
        'student': 'dmlmhsstudent',
        'teacher': 'dmlmhsteacher',
        'counselor': 'dmlmhsguidance',
        'guidance': 'dmlmhsguidance',
        'do': 'dmlmhsdo',
        'principal': 'dmlmhsprincipal',
    }
    
    pattern = role_patterns.get(role.lower())
    if not pattern:
        raise ValueError(f"Invalid role: {role}")
    
    # Format: lastname.dmlmhs[role]@gmail.com
    email = f"{lastname.lower()}.{pattern}@gmail.com"
    return email
