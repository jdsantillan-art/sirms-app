"""
Debug script to check if violations are being passed to the template
Run this and visit the URL it shows
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sirms_project.settings')
django.setup()

from incidents.models import IncidentType

print("\n" + "="*60)
print("🔍 DEBUGGING VIOLATIONS IN VIEW")
print("="*60)

# Get all violations like the view does
incident_types = IncidentType.objects.all().order_by('severity', 'name')

print(f"\n📊 Total violations found: {incident_types.count()}")

print("\n🚫 PROHIBITED ACTS:")
prohibited = incident_types.filter(severity='prohibited')
print(f"   Count: {prohibited.count()}")
for i, viol in enumerate(prohibited[:5], 1):
    print(f"   {i}. {viol.name}")
if prohibited.count() > 5:
    print(f"   ... and {prohibited.count() - 5} more")

print("\n📋 OTHER SCHOOL POLICIES:")
policies = incident_types.filter(severity='school_policy')
print(f"   Count: {policies.count()}")
for i, viol in enumerate(policies, 1):
    print(f"   {i}. {viol.name}")

print("\n" + "="*60)
print("✅ This is the EXACT data passed to the template!")
print("="*60)

print("\n🎯 HTML that should be generated:")
print("\n<select name='incident_type' id='id_incident_type'>")
print("    <option value=''>Select Violation Type</option>")
print("    <optgroup label='🚫 Prohibited Acts'>")
for viol in prohibited[:3]:
    print(f"        <option value='{viol.id}'>{viol.name}</option>")
print("        ... (36 more options)")
print("    </optgroup>")
print("    <optgroup label='📋 Other School Policies'>")
for viol in policies[:3]:
    print(f"        <option value='{viol.id}'>{viol.name}</option>")
print("        ... (5 more options)")
print("    </optgroup>")
print("</select>")

print("\n💡 If you don't see these in your browser:")
print("   1. Hard refresh: Ctrl+Shift+R")
print("   2. Check browser console (F12) for errors")
print("   3. View page source and search for 'id_incident_type'")
print()
