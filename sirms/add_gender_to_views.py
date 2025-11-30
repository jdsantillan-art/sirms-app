"""
Script to add student_gender field to views.py
"""

# Read the file
with open('incidents/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find and replace the section where involved_students is set
old_text = """            # Set other fields
            report.involved_students = form.cleaned_data['involved_students']
            report.incident_date = form.cleaned_data['incident_date']"""

new_text = """            # Set other fields
            report.involved_students = form.cleaned_data['involved_students']
            report.student_gender = form.cleaned_data.get('student_gender', '')
            report.incident_date = form.cleaned_data['incident_date']"""

if old_text in content:
    content = content.replace(old_text, new_text)
    print("✓ Updated report_incident view")
else:
    print("✗ Could not find the text to replace in report_incident view")

# Write back
with open('incidents/views.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done!")
