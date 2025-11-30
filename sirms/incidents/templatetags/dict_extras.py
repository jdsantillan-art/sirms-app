from django import template
from django.utils.safestring import mark_safe
import re

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Get an item from a dictionary using a key"""
    if dictionary and key:
        return dictionary.get(key, {})
    return {}

@register.filter
def get_dict_value(dictionary, key):
    """Get a value from a nested dictionary"""
    if dictionary and key:
        return dictionary.get(key, 0)
    return 0

@register.filter
def split(value, delimiter):
    """Split a string by delimiter"""
    if value:
        return value.split(delimiter)
    return []

@register.filter
def extract_counselor_name(remarks):
    """Extract counselor name from remarks field"""
    if remarks and "Counselor:" in remarks:
        # Extract text after "Counselor: " and before newline
        lines = remarks.split('\n')
        for line in lines:
            if line.startswith('Counselor:'):
                return line.replace('Counselor:', '').strip()
    return "Not assigned"

@register.filter
def urlize_legal_refs(text):
    """Convert URLs in legal references to clickable links with small font"""
    if not text:
        return text
    
    # Pattern to match URLs
    url_pattern = r'(https?://[^\s]+)'
    
    def replace_url(match):
        url = match.group(1)
        # Create a small, clickable link
        return f'<br><a href="{url}" target="_blank" rel="noopener noreferrer" class="text-xs text-blue-600 hover:text-blue-800 underline"><i class="fas fa-external-link-alt mr-1"></i>View Reference</a>'
    
    # Replace URLs with clickable links
    result = re.sub(url_pattern, replace_url, text)
    
    # Convert newlines to <br> tags
    result = result.replace('\n', '<br>')
    
    return mark_safe(result)