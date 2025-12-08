"""
Teacher utility functions for email generation and name formatting
"""
import re


def generate_teacher_email(first_name, last_name):
    """
    Generate teacher email in format: first letter of first name + last name + dmlmhs.teacher@gmail.com
    Example: Juan Dela Cruz -> jdelacruzdmlmhs.teacher@gmail.com
    """
    # Get first letter of first name (lowercase)
    first_letter = first_name[0].lower() if first_name else ''
    
    # Get last name, remove spaces and convert to lowercase
    last_name_clean = re.sub(r'[^a-zA-Z]', '', last_name).lower() if last_name else ''
    
    # Combine: first letter + last name + domain
    email = f"{first_letter}{last_name_clean}dmlmhs.teacher@gmail.com"
    
    return email


def format_teacher_name(name):
    """
    Format teacher name from "Mr. Juan Dela Cruz" or "Ms. Maria Santos" to proper format
    Returns: (title, first_name, last_name)
    """
    # Remove common titles
    title = ''
    if name.startswith('Mr.'):
        title = 'Mr.'
        name = name.replace('Mr.', '').strip()
    elif name.startswith('Ms.'):
        title = 'Ms.'
        name = name.replace('Ms.', '').strip()
    elif name.startswith('Mrs.'):
        title = 'Mrs.'
        name = name.replace('Mrs.', '').strip()
    elif name.startswith('Dr.'):
        title = 'Dr.'
        name = name.replace('Dr.', '').strip()
    
    # Split name into parts
    name_parts = name.split()
    
    if len(name_parts) >= 2:
        first_name = name_parts[0]
        last_name = ' '.join(name_parts[1:])  # Handle compound last names like "Dela Cruz"
        return title, first_name, last_name
    elif len(name_parts) == 1:
        return title, name_parts[0], ''
    else:
        return title, '', ''

